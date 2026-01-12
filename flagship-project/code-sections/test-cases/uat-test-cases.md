# UAT Test Cases

TC-001: Confirm system health summary displays correctly for an operations user.
TC-002: Confirm release documentation is present before approving deployment.
TC-003: Confirm reviewers can verify testing and risk mitigation before approval.
User Story: As an operations user, I want to quickly see whether services are healthy so I can respond faster.
User Story: As a team member, I want release expectations clearly documented so deployments are predictable.
User Story: As a reviewer, I want to verify testing and risk mitigation were completed before approving release.


## UAT-003 — Release expectations are clearly documented
**User Story:** As a team member, I want release expectations clearly documented so deployments are predictable.

**Preconditions:**
- The docs folder exists and is up to date.

**Steps:**
1. Open `docs/requirements.md` and confirm business + technical requirements are present.
2. Open `docs/test-plan.md` and confirm scope, test types, and acceptance criteria are defined.
3. Open `docs/risk-mitigation.md` and confirm risks + mitigations are listed.
4. Open `docs/release-notes.md` and confirm release version + summary + included changes exist.

**Expected Result:**
- A team member can understand what is being released, how it’s tested, and what risks are managed without asking for extra clarification.