# Reusing a 2013 Mac Pro for a Practical OpenClaw Agent

I repurposed a 2013 Mac Pro 6,1 running Nobara Linux as the durable host and orchestrator for Thumbo, a career-support OpenClaw agent. Thumbo supports preparation, research, organization, and drafting under human review. The machine has one Intel Xeon E5-2697 v2 and two AMD FirePro D700 GPUs with 6 GiB VRAM each—capable hardware for its era, but an intentionally difficult platform for modern local inference.

The goal was practical reuse, not to force a “works on my machine” demo or an all-local design. The Mac provides a durable home, workflow, and control plane; qualified hosted inference is intentional. Local Vulkan qualification determines only which work may enter that subsystem.

## The problem

Agent workloads bring long contexts, structured output, tool use, and sustained inference pressure. In the historic approximately 32 GiB environment, local Vulkan experiments triggered AMDGPU ring-timeout/device-loss failures under moderate context pressure. Those failures were below the configured thermal limits, so treating them as a simple cooling problem would have been wishful thinking. A later 64 GB upgrade and bounded post-upgrade runs add capacity and runtime evidence but do not prove causation or a Vulkan fix.

## The qualification approach

I created a staged validation framework rather than judging models from one good-looking response:

- Syntax repair: validate exact structural output.
- Long-context extraction: retrieve a planted key from a large document.
- Reasoning and safe refusal: verify both a correct result and a required refusal behavior.
- Tool use: validate schema-conformant function calls.

The environment also used one-model/one-request limits, non-display-GPU isolation for guarded experiments, thermal monitoring, and kernel-log monitoring. A failure at any stage stopped promotion.

## The decision

The result was clear: the tested local generative routes did not meet their gates for automatic routing on this platform. The operating architecture therefore uses qualified hosted models by specialist role, while local generation is restricted to a deliberately narrow offline lane.

One small local model remains permitted only for explicit, zero-tool, bounded tasks such as supplied-text summarization, rewriting, extraction, classification, and formatting. It is not an automatic fallback, command generator, or decision-maker.

That distinction matters. Reliability work is not about proving that every available resource can be used. It is about defining the safe operating envelope, enforcing it, and making the system fail in a controlled way.

## What this demonstrates

- Designing repeatable validation instead of relying on anecdotes.
- Isolating a fault domain and separating thermal symptoms from driver/runtime failure modes.
- Building policy guardrails around model routing, tool exposure, and fallback behavior.
- Choosing a routed architecture based on measured reliability rather than ideology.
- Documenting a decision trail that can be audited and revised as conditions change.

The useful outcome was not a claim that legacy GPUs became a modern inference cluster. It was a durable host and human-supervised agent workflow with a documented local boundary, qualified hosted routes, and clear safety rules.

See [Hardware Upgrade and Current State](hardware-upgrade-and-current-state.md)
and [Post-upgrade Local Qualification](../evidence/post-upgrade-local-qualification-2026-08-20.md)
for the later chronology and exact bounded dispositions.
