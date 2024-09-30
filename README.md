# Points Tracker API

## Prerequisites

- Python 3 installed.
- Pip (Python package installer).

## Tech Stack

- Backend: Django
- API Framework: Django REST Framework (DRF)
- Database: SQLite (default for Django)

## Cloning the Repository

```bash
git clone [<repository-url>](https://github.com/rahil0707/Fetch-Backend.git)
```

## Setup

1. Install Django:
   ```bash
   pip3 install django
   ```
2. Clone the repository and navigate to the project directory:
   ```bash
   cd points_tracker
   ```
3. Apply migrations:
   ```bash
   python3 manage.py migrate
   ```
4. Run the server:
   ```bash
   python manage.py runserver 8000
   ```


## Endpoints

1. Add Points (POST): `/add`
Request Body:
```json
{
  "payer": "DANNON",
  "points": 300,
  "timestamp": "2022-10-31T10:00:00Z"
}
```

2. Spend Points (POST): `/spend`
Request Body:
```json
{
  "points": 5000
}
```
Response:
```json
[
  { "payer": "DANNON", "points": -100 },
  { "payer": "UNILEVER", "points": -200 },
  { "payer": "MILLER COORS", "points": -4,700 }
]

```

3. Get Balance (GET): `/balance`
Response:
```json
{
  "DANNON": 1000,
  "UNILEVER": 0,
  "MILLER COORS": 5300
}
```
