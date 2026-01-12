# HomeLab

This project documents a personal, ops-focused home lab designed to demonstrate practical
infrastructure and systems skills, including networking, service hosting, security,
monitoring, and backup planning.

The goal of this lab is not to run a production environment 24/7, but to show how a
realistic home lab *would* be designed, operated, and secured using best practices.

> This home lab is implemented using a simulated setup that can run locally (for example,
> with Docker Desktop on a personal machine). No dedicated hardware is required to
> understand or reproduce the architecture.

## Why this HomeLab exists
Many real-world infrastructure skills are hard to demonstrate through code alone.
This project focuses on:
- System and network design
- Operational decision-making
- Security and reliability considerations
- Clear documentation of tradeoffs and lessons learned

## What’s included
- **docs/** — Detailed write-ups covering architecture, networking, services, security,
  monitoring, and backups
- **configs/** — Example configuration patterns (such as Docker Compose templates)
- **diagrams/** — Architecture and network diagrams

## Scope
This lab prioritizes clarity and reproducibility over complexity. Components are documented
as if they were part of a real home lab environment, even when simulated locally.

## Getting started (optional)
If you want to experiment with a simulated version of this lab:
1. Install Docker Desktop
2. Review `docs/services.md`
3. Use or adapt sample configurations under `configs/docker-compose/`

## License
MIT
