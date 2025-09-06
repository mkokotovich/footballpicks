# footballpicks


## Development

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


## At the start of each season

To load a new season's schedule, first bring up the api locally.

Then test resetting the win/loss records:

```
python manage.py generate_schedule
python manage.py reset_team_records
```

Then run these in prod by first connecting to a prod instance:

```
fly ssh console
cd /code
```

And run those two commands again.

Later, if necessary, to reload the schedule (to update for flex games, etc):

```
python manage.py generate_schedule
```


## Live Updates

To update game records, hit:
<https://footballpicks.fly.dev/api/v1/update/records>

To update game times, hit:
<https://footballpicks.fly.dev/api/v1/update/schedule>
