# ClearMacro

The ClearMacro Python library provides convenient access to the ClearMacro API from applications written in the Python language.

## Getting Started

The library can be easily developed using pipenv. The easiest way to start working with the library is to develop inside a Docker container, running the following command:

```
docker run -it -v `pwd`:/work pypy:3 /bin/bash
```

This will create a Pypy container and attach it to your terminal. Once you navigate to `/work` you can begin to develop.

The first commands to run are:

```
pip install pipenv
pipenv install --dev
```

### Linting

We use `flake8` to ensure coding style is enforced across developers. This process also runs in CI/CD so be sure to lint any changes before committing your code.

To lint your code: `pipenv run flake8 .`

### Testing

We use `pytest` throughout. This process also runs in CI/CD so ensure all the tests are passing before pushing your changes.

To run unit tests: `pipenv run pytest`

### Integration Tests

To run integration tests against the [Mock API](), run the following command. The `API_URL` assumes a reachable location for the mock API container.

```
API_URL=http://host.docker.internal:2345 API_USERNAME=test@clearmacro.com API_PASSWORD=test1234 pipenv run pytest tests/integration_client.py
```

## Examples

```
>>> from core.cmapi import CmApi
>>> api_session = CmApi(username, password)
>>> api_session.get_signal_timeseries("Inflation Surprise Score", "Australia", research_type="Back-test Level")
                  dateTimes     values
0    1999-01-31T23:59:59.99  10.000000
1    1999-02-28T23:59:59.99  10.000000
2    1999-03-31T23:59:59.99  10.000000
3    1999-04-30T23:59:59.99   1.000000
4    1999-05-31T23:59:59.99   3.250000
..                      ...        ...
255  2020-04-30T23:59:59.99   9.435294
256  2020-05-31T23:59:59.99   9.191406
257  2020-06-30T23:59:59.99   8.914397
258  2020-07-31T23:59:59.99   9.511628
259  2020-08-31T23:59:59.99   6.733591
```
