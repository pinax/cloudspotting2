# cloudspotting2

## Getting Started

Ensure you have `pipenv` installed and working.

```shell
$ mkdir cloudspotting2
$ git clone https://github.com/pinax/cloudspotting2.git
$ cd cloudspotting2
$ pipenv --three  # create Python 3 virtualenv
$ pipenv shell  # activate virtualenv
$ pipenv install  # install requirements from Pipfile.lock
$ npm install  # install requirements from package-lock.json
$ ./manage.py migrate
$ ./manage.py loaddata sites
$ npm run dev
```

Browse to http://localhost:3000/
