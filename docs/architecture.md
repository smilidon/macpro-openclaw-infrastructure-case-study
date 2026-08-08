# Architecture Overview

```mermaid
flowchart TD
    R[User request] --> M[Main agent]
    M --> S[Qualified specialist route]
    S --> H[Qualified hosted model]
    M -. explicit bounded text task only .-> O[Local offline lane]
    O --> L[Small local model\nzero tools]
    L -. never automatic fallback .-> X[No command generation or decisions]
    T[Thermal and kernel-log monitoring] --> O
    V[Staged validation] --> S
    V --> O
```

The production path is based on qualified hosted routes selected for specialist roles. The local lane is intentionally narrow: it handles only explicit, bounded, zero-tool text tasks and is never used as an automatic fallback or decision-making route.

The design reflects the platform’s measured reliability boundary rather than a preference for local inference at any cost.
