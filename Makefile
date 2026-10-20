run:
	cd backend && uv run uvicorn main:app --reload --port 8091

test:
	cd backend && uv run pytest
