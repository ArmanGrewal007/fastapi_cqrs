```bash
python -m venv venv
poetry install
python app/cli.py init_db
uvicorn app.main:app --reload
```