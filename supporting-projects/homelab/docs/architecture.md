# Architecture

This HomeLab is built around a simple, modular design that’s easy to understand
and adjust over time. The focus is on keeping things organized and isolated so
individual services can be added, removed, or changed without affecting the
rest of the environment.

The lab can run in a simulated setup using local tools like Docker Desktop,
which keeps the architecture flexible and avoids reliance on dedicated hardware.

## High-level structure
At a high level, the HomeLab consists of:
- A single host system
- Containerized services
- An internal network for service-to-service communication
- Limited, controlled external access
- Basic monitoring and logging

This mirrors how a small personal or home server environment would typically be
set up.

## Host system
The host system acts as the central point of control. In practice, this may be a
personal computer running Docker Desktop.

It is responsible for:
- Running containers
- Managing storage volumes
- Enforcing basic access and firewall rules
- Serving as the main administration point

## Service isolation
Each service runs in its own container. This keeps workloads separated, makes
updates easier, and reduces the risk that one service can interfere with
another.

Using containers also makes the lab easier to reproduce on a different machine.

## Networking approach
Services communicate over an internal virtual network. Only services that
require user access are exposed outside the lab.

This keeps the attack surface small and makes traffic flow easier to reason
about. More detail is covered in `network-topology.md`.

## Monitoring and tradeoffs
Basic monitoring is included to provide visibility into system health and
resource usage.

The architecture favors simplicity and clarity over performance tuning or high
availability. This makes the lab easier to maintain and better suited for
learning and experimentation.
