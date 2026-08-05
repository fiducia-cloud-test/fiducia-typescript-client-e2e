# Fiducia TypeScript client hardening

This offline contract turns the highest-risk distributed-systems behavior into executable acceptance criteria before live cluster credentials are introduced.

Coverage includes stale fencing tokens, `Retry-After` and idempotency reuse, cross-origin redirect refusal, leader failover safety, resumable WebSocket cursors, and idempotent NATS dead-letter replay.

Run locally:

```bash
python3 -m unittest -v hardening/test_scenarios.py
```

The scenarios contain no service credentials, lock values, or production endpoints.
