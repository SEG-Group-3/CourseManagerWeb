# Course Manager API

[Try it online](https://course-manager-server-seg-3.herokuapp.com/) (See examples bellow)

![Heroku](https://heroku-badge.herokuapp.com/?app=course-manager-server-seg-3
)

Todos:

- Authentication
  - [x] Have login requirements
  - [ ] Require user access level for certain functions (eg: Delete, Modify, Create fields)
- Users
  - [x] See users
  - [x] Create users
- Courses
  - [x] See courses
  - [x] Create courses

## How to run locally

### Setting up your keys

Download the keys key from:
Firebase Project settings → Service accounts → Firebase Admin →  Generate new private key

Place the key on the root folder and rename it to `keys.json`

### Running locally

```console
pip install -r requirements.txt
flask run
```

Using a virtual enviroment is recommended.
