# List of supported languages
LANGUAGES := en fr zh es de sw vi tl th

# Path to the translations directory
TRANSLATIONS_DIR := translations

# Path to the messages.pot file
POT_FILE := messages.pot



# Init command for initializing .po files
babelInit:
	@for lang in $(LANGUAGES); do \
		if [ ! -f $(TRANSLATIONS_DIR)/$$lang/LC_MESSAGES/$(POT_FILE:.pot=.po) ]; then \
			pybabel init -i $(POT_FILE) -d $(TRANSLATIONS_DIR) -l $$lang; \
		else \
			echo "$$lang already initialized"; \
		fi \
	done

# Update command for updating .po files
babelUpdate:
	pybabel extract -F babel.cfg -o messages.pot .
	for lang in $(LANGUAGES); do \
		pybabel update -d $(TRANSLATIONS_DIR) -i $(POT_FILE) -l $$lang; \
	done
	pybabel compile -d $(TRANSLATIONS_DIR)


initFlask:
	pip install -q -r requirements.txt
	flask db init
	flask db migrate
	flask db upgrade

upgradeDatabase:
	flask db migrate
	flask db upgrade







