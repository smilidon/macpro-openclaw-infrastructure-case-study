.PHONY: verify test

verify:
	bash scripts/verify-docs.sh

test: verify
	bash test/test-public-pack.sh
