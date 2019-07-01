## backend - favorite_things

```
 structure
    this projects structure is the following:
    .
    ├── api
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   └── schemas.py
    ├── README.md
    ├── requirements.txt
    ├── run.py
    └── tests.py
```

## concept

* ranking readjustments
    cases:
        1.  first time entry , only adjust desired rank to the last rank
        2.  old record updates, ascending or descending , adjust desired rank to previous rank (up or down)

* testing
    1. test the Item routes for now

* audit log :
    1. request log: is printed for now by @app.before_request
    2. db change log, sqlalchemy has a event listen decorator that can do the log collection for db change and add it to the db

## install requirements

> assuming that mysql is added in the system

```python

pip install -r requirements

```

## run

```python

python run.py

```

>server runs at `http://localhost:5000/`
