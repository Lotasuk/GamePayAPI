dev:
	python3.12 -m poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000