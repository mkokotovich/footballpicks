# footballpicks


Please install and use the flake8 pre-commit hook, this will help PRs stay focused on the important things:

```
pre-commit install --install-hooks
```

To set up local environment

```
docker compose down && docker compose build && docker compose up
./docker/first_run_init.sh
```

To deploy to fly.io:

```
flyctl deploy
```

To restart DB on fly.io:

```
fly pg restart -a fbpickspg --skip-health-checks --force
```

To load a new season's schedule, and reset the win/loss records, run:

```
python manage.py generate_schedule
python manage.py reset_team_records
```

To reload the schedule (to update for flex games, etc)

```
python manage.py generate_schedule
```

To run these in prod, first connect to the server:

```
fly ssh console
cd /code
```
