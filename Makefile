ENV_PATH?=.env


.PHONY: env-setup
env-setup:
	@virtualenv -q -p python3 $(ENV_PATH);
	@. $(ENV_PATH)/bin/activate && pip3 install --upgrade pip
	@$(MAKE) env-update

.PHONY: env-update
env-update:
	@. $(ENV_PATH)/bin/activate && pip3 -q install -r requirements.txt

.PHONY: env-py-shell
env-py-shell:
	@. $(ENV_PATH)/bin/activate && ipython3

.PHONY: clean-py
clean-py:
	@find . -name "*.pyc" -exec rm -rf {} \; -prune -print
	@find . -name "__pycache__" -exec rm -rf {} \; -prune -print

.PHONY: clean-build
clean-build:
	@rm -rf .build

.PHONY: clean
clean:
	@rm -rf $(ENV_PATH)
	@$(MAKE) clean-py
	@$(MAKE) clean-build


.PHONY: run
run:
	@. $(ENV_PATH)/bin/activate && python src/sshs.py ${HOST}
