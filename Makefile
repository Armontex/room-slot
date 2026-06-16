.PHONY: install-hooks

BACKEND = cd backend &&
ALEMBIC = $(BACKEND) uv run alembic

install-hooks:
	chmod +x .githooks/commit-msg
	$(BACKEND) uv sync --all-groups
	$(BACKEND) uv run pre-commit install --config ../.pre-commit-config.yaml --hook-type pre-commit --hook-type pre-push --hook-type commit-msg

revision:
	$(ALEMBIC) revision --autogenerate -m $(name)

migrate:
	$(ALEMBIC) upgrade head
