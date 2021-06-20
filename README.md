# Course Manager Web

[Try it online](https://course-manager-server-seg-3.herokuapp.com/) 

[Also checkout the android app](https://github.com/SEG-Group-3/CourseManager)

![Heroku](https://heroku-badge.herokuapp.com/?app=course-manager-server-seg-3
)

Todos:

- General
  - [ ] Implement realtime updates with sockeio
- Authentication
  - [x] Login screen
  - [ ] User type based interface
  - [ ] Require user access level for certain functions (eg: Delete, Modify, Create, Subscribe)
- Users
  - [x] See users
  - [x] Edit users
  - [ ] Create users
- Courses
  - [x] See courses
  - [x] Edit courses
  - [ ] Create courses
- Students
  - [ ] Enter/Leave courses
  - [ ] Query search courses
- Instructors
  - [ ] Edit course schedule
  - [ ] Assign/Unassign from courses
- API
  - [ ] Create delete auth tokens
  - [x] Validate token/user-roles
  
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
