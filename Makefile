path := ./

define Comment
	- Run `make help` to see all the available options.
	- Run `make setup` to run first-time project setup.
	- Run `make lint` to run the linter.
	- Run `make lint-check` to check linter conformity.
endef


.PHONY: lint
lint:  ## Apply all the linters
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@poetry run black --fast $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo
	@echo "Applying isort..."
	@echo "================="
	@echo
	@poetry run isort $(path) --skip="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@poetry run flake8 $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@poetry run mypy $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo


.PHONY: lint-check
lint-check: ## Check whether the codebase satisfies the linter rules
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@poetry run black --fast --check $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@poetry run isort --check $(path) --skip="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@poetry run flake8 $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@poetry run mypy $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo


.PHONY: black
black: ## Apply black
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@poetry run black --fast $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"
	@echo


.PHONY: isort
isort: ## Apply isort
	@echo "Applying isort..."
	@echo "================="
	@echo
	@poetry run isort $(path) --skip="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"


.PHONY: flake
flake: ## Apply flake8
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@poetry run flake8 $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"


.PHONY: mypy
mypy: ## Apply mypy
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@poetry run mypy $(path) --exclude="myenv,.venv,.git,.vscode,.pytest_cache,.mypy_cache,__pycache__"

.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: test
test: ## Run the tests against the current version of Python
	@echo "Resetting test database..."
	@edgedb query "drop database edgedb_test" > /dev/null 2>&1 || true && edgedb query "create database edgedb_test" > /dev/null 2>&1 && edgedb migrate -d edgedb_test && edgedb query -d edgedb_test -f tests/fixture.edgeql
	@poetry run pytest --disable-warnings -v


.PHONY: dep-install
dep-install: ## Install latest versions of prod dependencies
	@echo
	@echo "Installing dependencies..."
	@echo "=========================="
	@poetry add edgedb fastapi uvicorn


.PHONY: dep-install-dev
dep-install-dev: ## Install latest versions of dev dependencies
	@echo
	@echo "Installing dev dependencies..."
	@echo "=============================="
	@poetry add 'httpx[cli]' black flake8 isort mypy pytest pytest-mock pre-commit


.PHONY: install-edgedb
install-edgedb: ## Install the EdgeDB CLI
	@echo
	@echo "Installing EdgeDB..."
	@echo "===================="
	@which edgedb > /dev/null 2>&1 || (curl --proto '=https' --tlsv1.2 -sSf https://sh.edgedb.com | sh -s -- -y)


.PHONY: init-project
init-project: ## Initialize EdgeDB project
	@echo
	@echo "Initializing EdgeDB project..."
	@echo "=============================="
	@cp .env_sample .env
	@(edgedb project init --non-interactive || echo "Failed to initialize EdgeDB project")


.PHONY: dev-server
dev-server: ## Spin up local dev server
	@poetry run uvicorn app.main:fast_api --port 5001 --reload


.PHONY: health-check
health-check: ## Perform health check on the uvicorn server
	@chmod +x ./scripts/health_check
	@./scripts/health_check


.PHONY: generate
generate: ## Generate code from .edgeql files
	@echo
	@echo "Generating code..."
	@echo "=================="
	@poetry run edgedb-py


.PHONY: create-venv
create-venv: ## Create a virtual environment for the project
	@echo "Creating virtual environment..."
	@poetry install


.PHONY: activate-venv
activate-venv: ## Activate the project's virtual environment
	@echo "This cannot be done from Make. Run \`poetry shell\` in your shell to activate."


.PHONY: setup
setup: create-venv dep-install dep-install-dev install-edgedb init-project generate  ## Run first-time setup
	@echo
	@echo "${Green}All set!${NC} Run \`make dev-server\` to start a uvicorn dev server on port 5001."
