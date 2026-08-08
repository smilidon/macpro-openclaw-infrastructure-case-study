# Qualification Method

## Principle

No model, routing change, or local runtime configuration is promoted from a promising demo. It must pass the capabilities and safety boundaries required for its intended role.

## Stages

1. **Structured output** — validate exact syntax and repair behavior.
2. **Long-context retrieval** — confirm a planted key can be recovered from supplied material.
3. **Reasoning and safe refusal** — test both a correct answer and adherence to an explicit refusal constraint.
4. **Tool use** — validate schema-conformant invocation when the role is permitted to use tools.
5. **Operational behavior** — observe resource constraints, thermal state, and kernel logs during guarded local tests.

## Promotion rule

A failure at any stage stops promotion. The route may be narrowed, re-tested after a specific corrective change, or excluded from automatic production use.

## Why this is useful

The method separates a system that can generate a convincing response once from a system that can be trusted with a defined operational role. It also makes the final architecture explainable: every boundary has a reason.
