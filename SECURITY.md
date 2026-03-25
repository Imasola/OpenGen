# Security policy

## Reporting a vulnerability

If you discover a security vulnerability in OpenGen, **do not open a public issue.** Public disclosure gives attackers a head start.

**Contact the founders directly** with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)

We will acknowledge your report within 48 hours and provide a timeline for a fix. We will credit you in the security advisory unless you prefer to remain anonymous.

## Scope

This policy applies to:

- The open-source worker client (this repository)
- The shared data models and API client
- The opengen.live web platform (once deployed)

For suspected vulnerabilities in the closed-source Master Agent or the knowledge graph infrastructure, contact the founders directly. We take all reports seriously regardless of which component is affected.

## Security design

OpenGen's security architecture is documented in [docs/architecture.md](docs/architecture.md). Key principles:

- TLS/HTTPS on all connections
- Docker sandboxes for worker task execution
- mTLS certificates for worker authentication
- Input/output scanning for prompt injection and malware
- SHA-256 hash verification on every result
- GDPR compliant, hosted in Germany
- Worker API keys stay local and are never transmitted to the Master Agent

## Supported versions

| Version | Supported |
|---------|-----------|
| Current development (main branch) | Yes |
| Older commits | Best effort |
