
# SMTPlease

## Description

"Send My Text - Please" or SMTPlease is a small python project that can receive emails and retrieve the list of emails using SMTP and IMAP interface (stored in PostgreSQL database). It also provides a REST API interface for both function.

## Project Structure
```
smtplease/
├── alembic/
│   ├── (omitted, alembic related stuff)
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── smtp_handler.py
│   └── worker.py
├── .gitignore
├── alembic.ini
├── nixpacks.toml
├── Pipfile
├── Pipfile.lock
├── Procfile
└── README.md

```

## Environment Setup

### Prerequisites

- Python 3.11
- PostgreSQL
- Redis

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo.git
    cd your-repo
    ```

2. Create and activate the pipenv environment:
    ```bash
    pipenv --python 3.11
    pipenv install
    pipenv shell
    ```

3. Set up the PostgreSQL database and update the DATABASE_URL in database.py:
    ```python
    DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
    ```

4. Run database migrations:
    ```bash
    pipenv run alembic upgrade head
    ```

5. Run the application:
    ```
    pipenv run uvicorn app.main:app --reload
    ```

### Running Celery Worker
In a separate terminal, run the Celery worker:
```bash
pipenv run celery -A app.worker.celery_app worker --loglevel=info
```

## API Endpoints

- `POST /emails`: Manually add a new email to the queue.
    ```json
    # example request body
    {
        "sender": "sender@email.com",
        "receiver": "receiver@email.com",
        "subject": "Test mail Subject",
        "body": "Test mail body"
    }
    ```
- `GET /emails?limit=1&skip=0`: Retrieve all emails in the queue, skipping `skip` value and limiting `limit` total data.
- `GET /emails/{email_id}`: Retrieve a specific email by its ID.

## Performance
The system is designed to handle receiving 1000 emails per minute without failure.

## Notes
- Ensure that your PostgreSQL and Redis servers are running.
- The SMTP server listens on port 8025.
