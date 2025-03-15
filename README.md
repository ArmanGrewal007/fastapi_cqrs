<div align="center"><h1>CQRS template for FastAPI app</h1></div>

## Steps to run
```bash
python -m venv venv
poetry install
python app/cli.py init_db
uvicorn app.main:app --reload
# In another tab
./start.sh # to generate users, which will automatically be synced between read and write tables
```

## About CQRS (Command Query Request Segregation)
- **Commands** &rarr; Operations such as INSERT, UPDATE, DELETE in a DB.
- **Queries** &rarr; GET operations in a DB.

It is based on Command Query Separation (CQS) principle that the operations that change data (commands) should be separeted from operations that return data (queries). We utilize this in APIs by following the CRUD pattern, but using CQRS we can go one step further and add this segregation on DB level.

## Further improvements
- Currently we are using FastAPI's own `BackgroundTasks` to create asynchronous tasks to sync two DBs, but in production some king of message queue would be better.
