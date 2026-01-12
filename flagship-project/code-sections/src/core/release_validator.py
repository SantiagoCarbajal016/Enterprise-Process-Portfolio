"""
Release Readiness Validator (Flagship Project)

Purpose:
- Enforces that release artifacts exist and meet a minimum quality bar.
- Treats user stories as acceptance criteria that must be covered by UAT test cases.
- Produces a PASS/FAIL report and exit codes for CI use.

Usage (run from repo root or inside flagship-project/code-sections):
    python flagship-project/code-sections/src/core/release_validator.py
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


# ----------------------------
# Data models
# ----------------------------

@dataclass
class CheckResult:
    name: str
    passed: bool
    details: str = ""


# ----------------------------
# Helpers
# ----------------------------

def has_heading(text: str, heading: str) -> bool:
    """
    Regex-free heading check.
    Normalizes whitespace and compares headings line-by-line.
    Accepts: # Heading, ## Heading, ### Heading, etc.
    """
    target = heading.strip().lower()

    for line in text.splitlines():
        raw = line.strip()

        # Must start with 1-6 #'s then a space
        if not raw.startswith("#"):
            continue

        # Count leading #'s
        i = 0
        while i < len(raw) and raw[i] == "#":
            i += 1
        if i < 1 or i > 6:
            continue

        # Require at least one space after #'s
        if i >= len(raw) or raw[i] != " ":
            continue

        # Extract heading text after "#... "
        heading_text = raw[i+1:].strip().lower()

        if heading_text == target:
            return True

    return False


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Normalize common invisible characters that break regex checks
    text = text.replace("\u00A0", " ")  # non-breaking space -> normal space
    text = text.replace("\u200B", "")   # zero-width space
    text = text.replace("\u200C", "")   # zero-width non-joiner
    text = text.replace("\u200D", "")   # zero-width joiner
    text = text.replace("\u2060", "")   # word joiner

    return text


def file_exists_and_not_empty(path: Path) -> Tuple[bool, str]:
    if not path.exists():
        return False, f"Missing file (looked here: {path})"
    text = read_text(path).strip()
    if not text:
        return False, "File is empty"
    return True, "OK"


def require_headings(path: Path, required_headings: List[str]) -> CheckResult:
    ok, msg = file_exists_and_not_empty(path)
    if not ok:
        return CheckResult(name=f"Headings check: {path.name}", passed=False, details=msg)

    text = read_text(path)

    missing = [h for h in required_headings if not has_heading(text, h)]

    if missing:
        # Debug preview: show the first 15 lines so you can visually confirm
        preview_lines = "\n".join(
            f"{i+1:02d}: {line}"
            for i, line in enumerate(text.splitlines()[:15])
        )
        return CheckResult(
            name=f"Headings check: {path.name}",
            passed=False,
            details=(
                f"Missing headings: {', '.join(missing)}\n"
                f"--- file preview (first 15 lines) ---\n{preview_lines}"
            ),
        )

    return CheckResult(name=f"Headings check: {path.name}", passed=True, details="OK")



def extract_user_stories(user_stories_md: str) -> List[str]:
    """
    Extracts user stories from bullet list lines.

    Expected:
    - As a ...
    - As an ...
    """
    stories = []
    for line in user_stories_md.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            story = line[2:].strip()
            if story:
                stories.append(story)
    return stories


def extract_uat_story_refs(uat_md: str) -> List[str]:
    """
    Extracts explicit story references from UAT file.

    Supported:
    - User Story: As a ...
    - **User Story:** As a ...
    """
    refs: List[str] = []
    patterns = [
        r"^\s*User Story:\s*(As\s+.+)$",
        r"^\s*\*\*User Story:\*\*\s*(As\s+.+)$",
    ]
    for p in patterns:
        refs.extend([m.group(1).strip() for m in re.finditer(p, uat_md, flags=re.MULTILINE)])
    return refs


def extract_ua_test_cases(uat_md: str) -> List[str]:
    """
    Parses UAT test cases from markdown.

    Supported formats:
    - "TC-001: ..."
    - "- [ ] TC-001: ..."
    - "- TC-001: ..."

    Returns the text after the ":" if present; otherwise the line.
    """
    cases = []
    for line in uat_md.splitlines():
        raw = line.strip()

        # Checkbox bullet: - [ ] ...
        raw = re.sub(r"^\-\s*\[\s*\]\s*", "", raw)
        raw = re.sub(r"^\-\s*\[\s*x\s*\]\s*", "", raw, flags=re.IGNORECASE)

        if raw.startswith("TC-") or raw.startswith("- TC-") or raw.startswith("* TC-"):
            raw = raw.lstrip("-* ").strip()

        if raw.startswith("TC-"):
            parts = raw.split(":", 1)
            if len(parts) == 2:
                cases.append(parts[1].strip())
            else:
                cases.append(raw.strip())

    return [c for c in cases if c]


def story_coverage_check(user_stories_path: Path, uat_cases_path: Path) -> CheckResult:
    ok1, msg1 = file_exists_and_not_empty(user_stories_path)
    if not ok1:
        return CheckResult("User story coverage", False, f"{user_stories_path.name}: {msg1}")

    ok2, msg2 = file_exists_and_not_empty(uat_cases_path)
    if not ok2:
        return CheckResult("User story coverage", False, f"{uat_cases_path.name}: {msg2}")

    stories = extract_user_stories(read_text(user_stories_path))
    uat_text = read_text(uat_cases_path)
    uat_story_refs = extract_uat_story_refs(uat_text)
    cases = extract_ua_test_cases(uat_text)

    if not stories:
        return CheckResult("User story coverage", False, "No user stories found (expected bullet list).")

    # Prefer explicit traceability if present
    if uat_story_refs:
        missing = [s for s in stories if s not in uat_story_refs]
        if missing:
            preview = "\n".join([f"- {m}" for m in missing[:5]])
            more = "" if len(missing) <= 5 else f"\n...and {len(missing) - 5} more"
            return CheckResult(
                "User story coverage",
                False,
                "Some user stories are not referenced in UAT via `User Story:` lines:\n"
                + preview
                + more
                + "\n\nTip: Add lines like:\nUser Story: <exact story text>",
            )
        return CheckResult(
            "User story coverage",
            True,
            f"All {len(stories)} user stories referenced in UAT (explicit traceability).",
        )

    # Fallback: heuristic matching using test case text
    if not cases:
        return CheckResult("User story coverage", False, "No UAT test cases found (expected TC-### lines).")

    uncovered = []
    for s in stories:
        s_lower = s.lower()
        hit = False
        for c in cases:
            c_lower = c.lower()

            if s_lower in c_lower or c_lower in s_lower:
                hit = True
                break

            s_words = {w for w in re.findall(r"[a-zA-Z]{4,}", s_lower)}
            c_words = {w for w in re.findall(r"[a-zA-Z]{4,}", c_lower)}
            if len(s_words.intersection(c_words)) >= 2:
                hit = True
                break

        if not hit:
            uncovered.append(s)

    if uncovered:
        preview = "\n".join([f"- {u}" for u in uncovered[:5]])
        more = "" if len(uncovered) <= 5 else f"\n...and {len(uncovered) - 5} more"
        return CheckResult(
            "User story coverage",
            False,
            "Some user stories are not covered by UAT cases:\n" + preview + more
            + "\n\nTip: Add `User Story: <exact story text>` lines for explicit mapping.",
        )

    return CheckResult("User story coverage", True, f"All {len(stories)} user stories covered by UAT cases.")


def basic_file_check(name: str, path: Path) -> CheckResult:
    ok, msg = file_exists_and_not_empty(path)
    return CheckResult(name=name, passed=ok, details=msg)


def print_report(results: List[CheckResult]) -> int:
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    for r in results:
        icon = "✔" if r.passed else "✖"
        print(f"{icon} {r.name} — {r.details}")

    print("\n" + "-" * 60)
    if failed:
        print(f"Release Status: BLOCKED ❌  ({len(failed)} failing checks)")
        return 1
    print(f"Release Status: READY ✅  ({len(passed)} checks passed)")
    return 0


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Release Readiness Validator")
    parser.add_argument(
        "--base",
        default="flagship-project/code-sections",
        help="Base path to code-sections folder (default: flagship-project/code-sections)",
    )
    args = parser.parse_args()

    base = Path(args.base).resolve()
    docs = base / "docs"
    test_cases = base / "test-cases"

    # Required docs
    project_overview = docs / "project-overview.md"
    requirements = docs / "requirements.md"
    functional_requirements = docs / "functional-requirements.md"
    process_flows = docs / "process-flows.md"
    risk_mitigation = docs / "risk-mitigation.md"
    test_plan = docs / "test-plan.md"
    uat_plan = docs / "uat-plan.md"
    user_stories = docs / "user-stories.md"
    release_notes = docs / "release-notes.md"

    # Test case artifacts
    unit_tests = test_cases / "unit-tests.md"
    regression_tests = test_cases / "regression-tests.md"
    uat_test_cases = test_cases / "uat-test-cases.md"

    results: List[CheckResult] = []

    # Existence + non-empty checks (docs)
    results.append(basic_file_check("Doc: project-overview.md", project_overview))
    results.append(basic_file_check("Doc: requirements.md", requirements))
    results.append(basic_file_check("Doc: functional-requirements.md", functional_requirements))
    results.append(basic_file_check("Doc: process-flows.md", process_flows))
    results.append(basic_file_check("Doc: risk-mitigation.md", risk_mitigation))
    results.append(basic_file_check("Doc: test-plan.md", test_plan))
    results.append(basic_file_check("Doc: uat-plan.md", uat_plan))
    results.append(basic_file_check("Doc: user-stories.md", user_stories))
    results.append(basic_file_check("Doc: release-notes.md", release_notes))

    # Existence + non-empty checks (test artifacts)
    results.append(basic_file_check("Test cases: unit-tests.md", unit_tests))
    results.append(basic_file_check("Test cases: regression-tests.md", regression_tests))
    results.append(basic_file_check("Test cases: uat-test-cases.md", uat_test_cases))

    # Minimum heading requirements
    results.append(require_headings(requirements, ["Business Requirements", "Technical Requirements"]))
    results.append(require_headings(test_plan, ["Test Scope", "Test Types", "Acceptance Criteria"]))
    results.append(require_headings(risk_mitigation, ["Identified Risks", "Mitigation Strategies"]))
    results.append(require_headings(release_notes, ["Release Version", "Summary", "Included Changes"]))

    # Treat user stories as acceptance criteria that must be covered by UAT test cases
    results.append(story_coverage_check(user_stories, uat_test_cases))

    return print_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
