# ==============================================================================
# Corp++ (corp) Enterprise Makefile
# "Automating Enterprise Value Delivery Since Q3"
# ==============================================================================

.PHONY: all test build package run-examples repl clean audit docs docs-dev help

PYTHON ?= python3

all: test package

help:
	@echo "Corp++ Enterprise Build Automation Menu:"
	@echo "  make test          - Run full unit test suite"
	@echo "  make package       - Build standalone dist/corp executable binary"
	@echo "  make run-examples  - Execute all example deliverable scripts"
	@echo "  make repl          - Launch 'The Boardroom' interactive REPL"
	@echo "  make audit         - Run static compliance check on all examples"
	@echo "  make docs          - Build Astro Starlight documentation site"
	@echo "  make docs-dev      - Run Astro Starlight docs local dev server"
	@echo "  make clean         - Remove build artifacts & cache files"

test:
	@echo "==> Running Corp++ Enterprise Quality Assurance Suite..."
	@$(PYTHON) tests/run_tests.py

package:
	@echo "==> Building Standalone Corp++ Binary..."
	@$(PYTHON) scripts/build_binary.py

run-examples: package
	@echo "==> Executing Corp++ Deliverable Example Suite..."
	@./dist/corp run examples/01_onboarding.corp
	@echo ""
	@./dist/corp run examples/02_risk_mitigation.corp
	@echo ""
	@./dist/corp run examples/03_org_restructure.corp
	@echo ""
	@./dist/corp run examples/04_cross_functional.corp
	@echo ""
	@./dist/corp run examples/05_q3_financials.corp
	@echo ""
	@./dist/corp run examples/06_fizzbuzz_kpi.corp

audit:
	@echo "==> Executing Enterprise Compliance Audits..."
	@./dist/corp audit examples/01_onboarding.corp
	@./dist/corp audit examples/05_q3_financials.corp

docs:
	@echo "==> Building Astro Starlight Documentation Site in docs/..."
	@cd docs && npm run build

docs-dev:
	@echo "==> Launching Astro Starlight Documentation Server..."
	@cd docs && npm run dev

repl:
	@./dist/corp repl

clean:
	@echo "==> Restructuring workspace footprint..."
	@rm -rf dist/ build/ *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "==> Headcount optimized."
