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

.PHONY: clean
clean:
	@rm -rf $(ENV_PATH)
	@$(MAKE) clean-py
	@$(MAKE) dev-clean


.PHONY: run
run:
	@. $(ENV_PATH)/bin/activate && python src/sshs/sshs.py ${ARGS}


# develop

.PHONY: dev-%
dev-%:
	@. $(ENV_PATH)/bin/activate && python setup.py $* ${ARGS}


.PHONY: dev-help
dev-help:
	@. $(ENV_PATH)/bin/activate && python setup.py --help-commands


.PHONY: dev-install
dev-install:
	@. $(ENV_PATH)/bin/activate && python setup.py install


.PHONY: dev-uninstall
dev-uninstall:
	@. $(ENV_PATH)/bin/activate && pip3 uninstall -y sshs


.PHONY: dev-clean
dev-clean:
	@rm -rf build dist src/sshs.egg-info


.PHONY: dev-sshs
dev-sshs:
	@. $(ENV_PATH)/bin/activate && sshs ${HOST}


# system install/remove

.PHONY: install
install:
	@python3 setup.py install


.PHONY: uninstall
uninstall:
	@pip3 uninstall -y sshs
