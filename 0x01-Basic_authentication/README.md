# 0x01. Basic authentication

## Files
### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints
- `auth/auth.py`:  used to manage api authentication


### Setup
#### Setup and start server
```
$ pip3 install -r requirements.txt
$
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Serving Flask app "app" (lazy loading)
...
$
```

### Routes
- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `GET /api/v1/forbidden`:  raises a 403 error by using `abort` - `GET /api/v1/unauthorized`: raises a 401 error
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

#### Use the API  _(in another tab or in your browser)_
```
$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/status HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 16
< Access-Control-Allow-Origin: *
< Server: Werkzeug/1.0.1 Python/3.7.5
< Date: Mon, 18 May 2020 20:29:21 GMT
< 
{"status":"OK"}
* Closing connection 0
bob@dylan:~$
```

### 1. Error handler: Unauthorized
In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/unauthorized HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:50:40 GMT
< 
{
  "error": "Unauthorized"
}
* Closing connection 0
bob@dylan:~$
```

### 2. Error handler: Forbidden
In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden"
{
  "error": "Forbidden"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/forbidden HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:54:22 GMT
< 
{
  "error": "Forbidden"
}
* Closing connection 0
bob@dylan:~$
```
### 3. Auth class

File: [main_0.py](main_0.py) , [api/v1/auth/auth.py](api/v1/auth/auth.py)

This class is the template for all authentication system you will implement.
```
bob@dylan:~$ 
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_0.py
False
None
None
bob@dylan:~$
```
### 4. Define which routes don't need authentication

File: [main_1.py](main_0.py) , [api/v1/auth/auth.py](api/v1/auth/auth.py)
 `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:`  in  `Auth`  that returns  `True`  if the  `path`  is not in the list of strings  `excluded_paths`:

-   Returns  `True`  if  `path`  is  `None`
-   Returns  `True`  if  `excluded_paths`  is  `None`  or empty
-   Returns  `False`  if  `path`  is in  `excluded_paths`
-   You can assume  `excluded_paths`  contains string path always ending by a  `/`
-   This method must be slash tolerant:  `path=/api/v1/status`  and  `path=/api/v1/status/`  must be returned  `False`  if  `excluded_paths`  contains  `/api/v1/status/`
```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_1.py
True
True
True
False
False
True
True
bob@dylan:~$
```

### 5. Request validation!

[api/v1/auth/auth.py](api/v1/auth/auth.py) , [api/v1/app.py](api/v1/app.py)

method  `def authorization_header(self, request=None) -> str:`  in  `api/v1/auth/auth.py`:
-   If  `request`  is  `None`, returns  `None`
-   If  `request`  doesn’t contain the header key  `Authorization`, returns  `None`
-   Otherwise, return the value of the header request  `Authorization`

In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

### 6. Basic auth
In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

### 7. Basic - Base64 part

[api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) , [main_2.py](main_2.py)

extract_base64_authorization_header(self, authorization_header: str) -> str:`  in the class  `BasicAuth`  that returns the Base64 part of the  `Authorization`  header for a Basic Authentication:
-   Return  `None`  if  `authorization_header`  is  `None`
-   Return  `None`  if  `authorization_header`  is not a string
-   Return  `None`  if  `authorization_header`  doesn’t start by  `Basic`  (with a space at the end)
-   Otherwise, return the value after  `Basic`  (after the space)
-   You can assume  `authorization_header`  contains only one  `Basic`
```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_2.py
None
None
None
Holberton
SG9sYmVydG9u
SG9sYmVydG9uIFNjaG9vbA==
None
bob@dylan:~$
```

### 8. Basic - Base64 decode

[main_3.py](main_3.py)

`def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:`  in the class  `BasicAuth`  that returns the decoded value of a Base64 string  `base64_authorization_header`:

-   Return  `None`  if  `base64_authorization_header`  is  `None`
-   Return  `None`  if  `base64_authorization_header`  is not a string
-   Return  `None`  if  `base64_authorization_header`  is not a valid Base64 - you can use  `try/except`
-   Otherwise, return the decoded value as UTF8 string - you can use  `decode('utf-8')`

```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_3.py
None
None
None
Holberton
Holberton School
Holberton School
bob@dylan:~$
```

### 9. Basic - User credentials

[main_4.py](main_4.py)

`def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)`  in the class  `BasicAuth`  that returns the user email and password from the Base64 decoded value.
-   This method must return 2 values
-   Return  `None, None`  if  `decoded_base64_authorization_header`  is  `None`
-   Return  `None, None`  if  `decoded_base64_authorization_header`  is not a string
-   Return  `None, None`  if  `decoded_base64_authorization_header`  doesn’t contain  `:`
-   Otherwise, return the user email and the user password - these 2 values must be separated by a  `:`
-   You can assume  `decoded_base64_authorization_header`  will contain only one  `:`
```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_4.py
(None, None)
(None, None)
(None, None)
('Holberton', 'School')
('bob@gmail.com', 'toto1234')
bob@dylan:~$
```

### 10. Basic - User object

[main_5.py](main_5.py)

`def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):`  in the class  `BasicAuth`  that returns the  `User`  instance based on his email and password.
-   Return  `None`  if  `user_email`  is  `None`  or not a string
-   Return  `None`  if  `user_pwd`  is  `None`  or not a string
-   Return  `None`  if your database (file) doesn’t contain any  `User`  instance with email equal to  `user_email`  - you should use the class method  `search`  of the  `User`  to lookup the list of users based on their email. Don’t forget to test all cases: “what if there is no user in DB?”, etc.
-   Return  `None`  if  `user_pwd`  is not the password of the  `User`  instance found - you must use the method  `is_valid_password`  of  `User`
-   Otherwise, return the  `User`  instance

```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_5.py 
New user: Bob Dylan
None
None
None
None
Bob Dylan
bob@dylan:~$
```

### 11. Basic - Overload current_user - and BOOM!

[main_6.py](main_6.py)
 `def current_user(self, request=None) -> TypeVar('User')`  in the class  `BasicAuth`  that overloads  `Auth`  and retrieves the  `User`  instance for a request:

-   You must use  `authorization_header`
-   You must use  `extract_base64_authorization_header`
-   You must use  `decode_base64_authorization_header`
-   You must use  `extract_user_credentials`
-   You must use  `user_object_from_credentials`

In the first terminal:
```
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_6.py 
New user: 9375973a-68c7-46aa-b135-29f79e837495 / bob@hbtn.io
Basic Base64: Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic test"
{
  "error": "Forbidden"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh"
[
  {
    "created_at": "2017-09-25 01:55:17", 
    "email": "bob@hbtn.io", 
    "first_name": null, 
    "id": "9375973a-68c7-46aa-b135-29f79e837495", 
    "last_name": null, 
    "updated_at": "2017-09-25 01:55:17"
  }
]
bob@dylan:~$ 
```
