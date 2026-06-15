.PHONY: install-hooks

install-hooks:
	chmod +x .githooks/commit-msg
	cd backend && uv sync --all-groups
	cd backend && uv run pre-commit install --config ../.pre-commit-config.yaml --hook-type pre-commit --hook-type pre-push --hook-type commit-msg
