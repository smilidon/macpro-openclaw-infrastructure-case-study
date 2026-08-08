# Building a Safe Operating Envelope for AI Agents on Legacy Hardware

This case study documents how I qualified an OpenClaw agent environment on a 2013 Mac Pro 6,1 running Nobara Linux.

The goal was not to force an impressive demo from aging GPUs. It was to determine which workloads the platform could safely support, document the evidence, and design the production architecture around that result.

## The outcome

Modern local generative inference using Vulkan GPU offload was not reliable enough for automatic production routing on this hardware. Rather than hide that failure mode, I treated it as an engineering decision:

- use a staged validation framework instead of one-off demos;
- isolate experimental fault domains and monitor thermal and kernel signals;
- stop promotion when a model or configuration fails qualification;
- use qualified hosted models by specialist role for production work; and
- retain a narrowly bounded local lane only for explicit, zero-tool text tasks.

The result is a dependable hybrid agent platform with documented operating boundaries and controlled failure behavior.

## Why it matters

This project demonstrates practical systems engineering and ML-infrastructure judgment:

- repeatable validation and evidence-based promotion decisions;
- driver/runtime fault isolation under sustained load;
- guardrails for model routing, tool exposure, and fallback behavior;
- risk-aware use of constrained and legacy hardware; and
- clear technical documentation for an auditable decision trail.

## Contents

- [Case study](docs/case-study.md)
- [Qualification method](docs/qualification-method.md)
- [Architecture overview](docs/architecture.md)

## Scope and privacy

This is a deliberately sanitized portfolio artifact. It does not include credentials, host paths, private configuration, account limits, security-audit details, or internal session records. It also does not claim that the AMDGPU/Vulkan reliability issue was fixed.

## Contact

I am open to systems engineering, ML infrastructure, and platform-reliability opportunities where practical engineering judgment matters.
