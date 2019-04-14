Table of contents

- [Requirements](#requirements)
  - [Python](#python)
  - [Pipenv](#pipenv)
- [Install](#install)
- [Generate data](#generate-data)
- [Run code](#run-code)

## Requirements

### Python

Python **3.7**

### Pipenv

[Pipenv](https://pipenv.readthedocs.io/) is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

[Instructions to install](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Install

```bash
pipenv install
```

## Generate data

```bash
pipenv run generate_data
pipenv run generate_data 200
```

By default `generate_data` will generate 50 JSONs.

## Run code

```bash
pipenv run exec
```
