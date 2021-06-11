# Course Manager API

[Try it online](https://course-manager-server-seg-3.herokuapp.com/) (See examples bellow)

![Heroku](https://heroku-badge.herokuapp.com/?app=course-manager-server-seg-3
)

## How to run locally

### Setting up your keys

Download the keys key from

```
Firebase Project settings
- Service accounts
- - Firebase Admin SDK
- - - Generate new private key
```

Place it on the root folder and rename it to `keys.json`

### Running the app

```sh
pip install -r requirements.txt


flask run
# or
# waitress-serve --port=8000 --host=localhost main:app
# or
# heroku local web -f Procfile.local
```

Using a virtual enviroment with `virtualenv` is recommended

## API Specification

The list of wired urls and their functions

### `/courses`

Displays the list of courses.

You can filter by passing `name` and `code` parameters as filters.

eg: `http://localhost:5000/courses?name=Calculus&code=MAT`

### `/register`

Registers an account to users

Requires `name` and `password` but can take an optional `type` paremeter for student or instructor

eg: `http://localhost:5000/register?name=Jeff&password=p4ssw0rd`
