# Services

The HomeLab is built around a small set of services that cover common use cases
in a personal or home server environment. Each service is chosen to serve a
specific purpose and to keep the overall setup easy to manage.

Services are intended to run in containers, which keeps them isolated and makes
it easier to start, stop, or replace individual components without affecting
the rest of the system.

## Core services

### Container management
A container management tool (such as Docker and Docker Compose) is used to run
and organize all services. This provides a consistent way to manage
configuration, networking, and storage across the lab.

### Management dashboard
A lightweight dashboard or admin interface (for example, Portainer) can be
used to view running containers, check their status, and perform basic
maintenance tasks.

This makes it easier to understand what’s running at any given time without
needing to rely entirely on the command line.

### Network services
Basic network-related services may be included, such as:
- DNS filtering or local name resolution
- Internal service discovery
- Simple routing or reverse proxy behavior

These services help simulate how traffic would normally be handled in a small
self-hosted environment.

### Media or application services (optional)
Optional application-level services can be added depending on needs, such as:
- A media server
- A simple web application
- A personal utility or dashboard

These services are not required for the lab to function but help demonstrate
how user-facing applications fit into the overall setup.

## Service boundaries
Each service runs independently and communicates only when necessary. This
keeps responsibilities clear and limits the impact of failures.

If a service is no longer needed, it can be removed without requiring major
changes to the rest of the environment.

## Why this approach
This service layout favors simplicity and flexibility. It reflects how a
realistic home lab would evolve over time, starting small and growing only as
new needs arise.
