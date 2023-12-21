# MBABackend

## Run

```sh
flask -A app run --reload
flask -A app routes
```

## Migrations

```sh
flask -A app db init
flask -A app db migrate -m "v1"
flask -A app db upgrade
```


## Tests

```sh
pytest
```
