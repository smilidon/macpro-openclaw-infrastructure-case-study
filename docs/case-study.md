# What I Learned Qualifying AI Infrastructure on a 2013 Mac Pro

I built and qualified an OpenClaw agent environment on a 2013 Mac Pro 6,1 running Nobara Linux. The machine has dual AMD FirePro D700 GPUs—capable hardware for its era, but an intentionally difficult platform for modern local inference.

The goal was not to force a “works on my machine” demo. It was to determine whether the platform could safely carry automated agent workloads, then make the routing decision the evidence supported.

## The problem

Agent workloads bring long contexts, structured output, tool use, and sustained inference pressure. On this hardware, larger local models using Vulkan GPU offload repeatedly triggered AMDGPU ring-timeout/device-loss failures under moderate context pressure. Those failures were below the configured thermal limits, so treating them as a simple cooling problem would have been wishful thinking.

## The qualification approach

I created a staged validation framework rather than judging models from one good-looking response:

- Syntax repair: validate exact structural output.
- Long-context extraction: retrieve a planted key from a large document.
- Reasoning and safe refusal: verify both a correct result and a required refusal behavior.
- Tool use: validate schema-conformant function calls.

The environment also used one-model/one-request limits, non-display-GPU isolation for guarded experiments, thermal monitoring, and kernel-log monitoring. A failure at any stage stopped promotion.

## The decision

The result was clear: normal local generative inference was not reliable enough for automatic production routing on this platform. The production architecture therefore uses qualified hosted models by specialist role, while local generation is restricted to a deliberately narrow offline lane.

One small local model remains permitted only for explicit, zero-tool, bounded tasks such as supplied-text summarization, rewriting, extraction, classification, and formatting. It is not an automatic fallback, command generator, or decision-maker.

That distinction matters. Reliability work is not about proving that every available resource can be used. It is about defining the safe operating envelope, enforcing it, and making the system fail in a controlled way.

## What this demonstrates

- Designing repeatable validation instead of relying on anecdotes.
- Isolating a fault domain and separating thermal symptoms from driver/runtime failure modes.
- Building policy guardrails around model routing, tool exposure, and fallback behavior.
- Choosing a hybrid architecture based on measured reliability rather than ideology.
- Documenting a decision trail that can be audited and revised as conditions change.

The useful outcome was not a claim that legacy GPUs became a modern inference cluster. It was a dependable agent platform with a documented local boundary, qualified hosted routes, and clear safety rules.
