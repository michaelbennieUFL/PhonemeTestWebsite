initFlask:
	pip install -q -r requirements.txt
	flask db init
	flask db migrate
	flask db upgrade

upgradeDatabase:
	flask db migrate
	flask db upgrade