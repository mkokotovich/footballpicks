# footballpicks


Please install and use the flake8 pre-commit hook, this will help PRs stay focused on the important things:

```
pre-commit install --install-hooks
```

To deploy to fly.io:

```
flyctl deploy
```

To restart DB on fly.io:

```
fly pg restart -a fbpickspg --skip-health-checks --force
```
