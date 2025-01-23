bot:
	pipenv run uvicorn src.main:app --log-level debug

test:
	uvicorn test:app

production:
	uvicorn src.main:app --host 0.0.0.0 --port 8000