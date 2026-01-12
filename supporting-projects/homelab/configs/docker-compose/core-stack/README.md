# HomeLab Core Stack

This folder contains the initial “real lab” implementation using Docker Compose.

## Services
- Portainer (container management UI)
- Nginx Proxy Manager (reverse proxy + optional HTTPS)
- Uptime Kuma (simple monitoring)

## Setup
1. Copy `.env.example` to `.env`
2. Start the stack:

```bash
docker compose up -d
