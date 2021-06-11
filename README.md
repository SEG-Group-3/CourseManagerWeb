# Course Manager API

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

```
pip install -r requirements.txt
flask run
```

Using a virtual enviroment with `virtualenv` is recommended

## API

The list of wired urls and their functions

### `/courses`

Displays the list of courses.

You can filter by passing `name` and `code` parameters as filters.

eg: `http://localhost:5000/courses?name=Calculus&code=MAT`

### `/register`

Registers an account to users

Requires `name` and `password` but can take an optional `type` paremeter for student or instructor

eg: `http://localhost:5000/register?name=Jeff&password=p4ssw0rd`
