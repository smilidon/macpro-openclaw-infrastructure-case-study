# Bounded Local-Lane Test Method

This suite follows three simple evaluation principles:

1. Test a defined capability with a fixed expected result.
2. Fix decoding and runtime settings so results can be compared.
3. Retain raw response text, API timing fields, and kernel-fault observations.

The test set measures only the admitted local lane at a 4K context: exact
retrieval, scope classification, strict JSON formatting, and a source-grounded
incident-note summary. Exact-match cases are scored automatically. JSON is
parsed before it is scored. The incident-note result is explicitly marked for
human review: it must stay grounded in the supplied note, use the requested
three-bullet structure, and avoid operational advice. A failed JSON case is
evidence that downstream structured consumers need validation; it is not
repaired by prompt interpretation.

The suite deliberately excludes tools, commands, autonomous actions, safety
claims beyond the narrow lane, high-context stress, and every rejected model.
Those tests have a different risk profile and require a separately approved
plan.

References:

- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Ollama API usage metrics](https://docs.ollama.com/api/usage)
- [MLCommons test-specification schema](https://mlcommons.org/2024/05/ai-safety-test-spec-schema/)
