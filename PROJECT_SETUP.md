# Project setup

Step-by-step setup instructions potentially useful for developers wanting to work with APIS.


## Setup with Poetry

Instructions on how to get a new APIS project up and running using [Poetry](https://python-poetry.org/).


### Set up a Python project with Poetry

If you are not starting from zero or want to fine-tune your project settings, skip ahead to [Create project interactively](#create-project-interactively), otherwise read on.


#### Create a new project from scratch

Use Poetry's [`new`](https://python-poetry.org/docs/cli/#new) command to instantaneously create a base set of files and folders for a new Python project:

```shell
$ poetry new YOUR_PROJECT_NAME --name apis_ontology
```

This will also make Poetry set the _package name_ (`name` value in `pyproject.toml`) to "apis-ontology" in addition to creating the required `apis_ontology` folder. You don't need to keep this name but can change it to your liking.

**ACDH-CH devs** may want to keep with the `apis-instance-PROJECT_NAME` convention for package and repository name used by [existing ACDH-CH projects](https://github.com/topics/apis-instance).


#### Create project interactively

If you already have files or infrastructure for your project in place – e.g. a project directory, virtual environment, Git repository – or want to be given the option to override initial project settings, use the [`init`](https://python-poetry.org/docs/cli/#init) command to interactively create only the `pyproject.toml` file for your project.

`pyproject.toml` needs to sit in the root of your project, so make sure to `cd` into the correct directory, then run:

```shell
$ poetry init
```

You'll subsequently have to manually add the required `apis_ontology` directory for your APIS app  (incl. `__init__.py`) or rename an existing project directory.


#### Install project dependencies

Make sure the Python version installed in the environment you will develop your app in matches `apis-core-rdf`'s [Python requirements](https://github.com/acdh-oeaw/apis-core-rdf/blob/main/pyproject.toml#L12) or the package won't install.

A **potential pitfall** is to try to install into the wrong environment due to e.g. the correct/intended virtual env not being activated or a competing virtual environment interfering with the targeted one. Example: You accidentally created/activated a Poetry virtual env on top of the intended virtual environment. Or: You didn't activate the intended virtual env and Poetry falls back to the system Python. Or: You run commands both from within your IDE and a terminal but use diverging settings.

To add `apis-core-rdf` as project dependency, look up the version number tag for its [latest release](https://github.com/acdh-oeaw/apis-core-rdf/releases/latest) and append it to its Git path:

```shell
$ poetry add git+https://github.com/acdh-oeaw/apis-core-rdf#RELEASE_VERSION
```

If you want to use a different Django version for your project than [whatever `apis-core-rdf` uses](https://github.com/acdh-oeaw/apis-core-rdf/blob/main/pyproject.toml#L13), add it to your dependencies as well. Examples:

```shell
$ poetry add django@latest
$ poetry add django@4.2
$ poetry add django@^4.2.0

```


### Create Django base files using Poetry

With Django installed, you can use Poetry for initial setup of your Django application.

Make sure you have your `apis_ontology` folder in place and that it's detectable by Django, i.e. contains an `__init__.py` file. Then run the [`startproject`](https://docs.djangoproject.com/en/4.2/ref/django-admin/#startproject) command to create the minimum necessary files to run a Django application:

```shell
$ poetry run django-admin startproject apis_ontology .
```

To start up your Django project locally, use the [`runserver`](https://docs.djangoproject.com/en/4.2/ref/django-admin/#runserver) command:
```shell
$ poetry run ./manage.py runserver
```
