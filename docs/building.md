# Building and Verification

This repository is a documentation-first portfolio packet. It does not build or
run an agent environment from source.

## Verify the Published Files

```sh
make verify
```

The command checks:

- local Markdown links;
- the required public files; and
- obvious private-path or secret-like text in the Markdown pack.

It is intentionally narrow. It does not run inference, contact providers,
measure hardware, validate Mermaid rendering, or prove any operational claim.

## What Can Be Reproduced Here

- The documented architecture and decision record.
- The qualification method as a framework for another environment.
- The public-pack verification check.

For the full repository contract, run:

```sh
make test
```

## What Cannot Be Reproduced Here

- Exact host behavior, driver state, kernel logs, thermals, or model results.
- The private OpenClaw configuration and provider-routing state.
- Any provider availability, latency, cost, or service-level outcome.

## Adding Future Evidence

Do not add raw host exports. Add a sanitized, reviewable test bundle with
versions, configuration, structured results, relevant log windows, and a short
note explaining the result. Update [evidence.md](evidence.md) at the same time.
