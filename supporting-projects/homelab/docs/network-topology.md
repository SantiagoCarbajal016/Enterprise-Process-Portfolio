# Network Topology

The network setup for this HomeLab is intentionally simple. The main idea is to
separate internal services from anything that needs to be accessed directly,
so it’s always clear what’s exposed and what isn’t.

Rather than modeling physical switches or complex routing, the focus is on how
services talk to each other and where boundaries should exist.

## Internal traffic
All services run on a private, internal network created by the container
runtime. This network is used only for communication between services and is not
reachable from outside the lab.

Keeping internal traffic private helps reduce risk and keeps things easier to
understand when something goes wrong.

## User-facing access
Only a small number of services are meant to be accessed directly, such as a web
interface or a management dashboard. Anything that doesn’t need user access
stays on the internal network.

This makes it obvious which services are exposed and avoids opening access where
it isn’t necessary.

## How traffic flows
In practice, traffic follows a simple pattern:
- A request comes in through a defined entry point
- The request is routed to the appropriate service
- Any follow-up communication stays on the internal network

## Why it’s set up this way
The network design favors simplicity and clarity. It’s easier to maintain,
easier to troubleshoot, and closer to how a small home or personal server setup
would realistically be run.
