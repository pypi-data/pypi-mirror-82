# Caribbean Outbreak Tracker

[![forthebadge made-with-python][1]](https://www.python.org/)

![python][2] [![MIT license][3]](https://lbesson.mit-license.org/)

## Introduction

Django package for tracking pandemic outbreaks in the Caribbean. Based on previous project for tracking COVID-19 across the Caribbean (<https://github.com/obikag/caribbean-virus-tracker/>).

Website based on this project can be found here: <https://caribbeanvirustracker.com/>

## Installation

### Pip

Use the Python package manager [pip](https://pypi.org/project/pip/) to install the package and dependencies.

```bash
pip install caribbean-outbreak-tracker
```

### GitHub Repo

Clone the repo and navigate to the working directory.

```bash
git clone https://github.com/obikag/caribbean-outbreak-tracker.git
cd caribbean-outbreak-tracker
```

Using [setuptools](https://pypi.org/project/setuptools/) install the package and dependencies.

```bash
python setup.py install
```

## Usage

Create a [Django](https://www.djangoproject.com/) project and navigate to working directory.

```bash
django-admin startproject example-site
cd example-site
```

Add the outbreak tracker app to you settings.py file

```python
INSTALLED_APPS = [
    ...,
    'outbreak_tracker',
]
```

Make migrations and migrate changes to the database

```bash
python manage.py makemigrations
python manage.py migrate
```

Navigate to the project's admin site to access the models and enter the relevant information.

## Documentation

Comming Soon

## Testing

Comming Soon

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

[1]: https://forthebadge.com/images/badges/made-with-python.svg
[2]: https://img.shields.io/badge/python-3.6-blue
[3]: https://img.shields.io/badge/License-MIT-blue.svg
