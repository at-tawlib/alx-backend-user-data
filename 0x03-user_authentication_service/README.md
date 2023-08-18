# 0x03. User authentication service
### [0. User model](user.py)
SQLAlchemy model named  `User`  for a database table named  `users`  (by using the  [mapping declaration](https://intranet.alxswe.com/rltoken/-a69l-rGqoFdXnnu6qfKdA "mapping declaration")  of SQLAlchemy).
The model will have the following attributes:
-   `id`, the integer primary key
-   `email`, a non-nullable string
-   `hashed_password`, a non-nullable string
-   `session_id`, a nullable string
-   `reset_token`, a nullable string

```
bob@dylan:~$ python3 main1.py
users
users.id: INTEGER
users.email: VARCHAR(250)
users.hashed_password: VARCHAR(250)
users.session_id: VARCHAR(250)
users.reset_token: VARCHAR(250)
bob@dylan:~$ 
```
### [1. create user](main2.py)
```
bob@dylan:~$ python3 main2.py
1
2
bob@dylan:~$
```

### [2. Find user](main3.py)
SQLAlchemy’s  `NoResultFound`  and  `InvalidRequestError`  are raised when no results are found, or when wrong query arguments are passed, respectively.
```
bob@dylan:~$ python3 main3.py
1
1
Not found
Invalid
bob@dylan:~$ 
```

### [3. update user](main4.py)

The method will use  `find_user_by`  to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.

If an argument that does not correspond to a user attribute is passed, raise a  `ValueError`.

```
bob@dylan:~$ python3 main4.py
1
Password updated
bob@dylan:~$ 
```

### [4. Hash password](main5.py)

`_hash_password`  method that takes in a  `password`  string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with  `bcrypt.hashpw`.

```
bob@dylan:~$ python3 main3.py
b'$2b$12$eUDdeuBtrD41c8dXvzh95ehsWYCCAi4VH1JbESzgbgZT.eMMzi.G2'
bob@dylan:~$
```

### [5. Register user](main6.py)
If a user already exist with the passed email, raise a  `ValueError`  with the message  `User <user's email> already exists`.

If not, hash the password with  `_hash_password`, save the user to the database using  `self._db`  and return the  `User`  object.

```
bob@dylan:~$ python3 main6.py
successfully created a new user!
could not create a new user: User me@me.com already exists
bob@dylan:~$
```

### 7. Register user

implement the end-point to register a user. Define a  `users`  function that implements the  `POST /users`  route.

The end-point should expect two form data fields:  `"email"`  and  `"password"`. If the user does not exist, the end-point should register it and respond with the following JSON payload:

_Terminal 1:_

```
bob@dylan:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a prod http://0.0.0.0:5000/ (Press CTRL+C to quit)uction WSGI server instead.
 * Debug mode: off
 * Running on

```
_Terminal 2:_
```
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 52
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:18 GMT
< 
{"email":"bob@me.com","message":"user created"}

bob@dylan:~$
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 400 BAD REQUEST
< Content-Type: application/json
< Content-Length: 39
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:33 GMT
< 
{"message":"email already registered"}
bob@dylan:~$
```

### [8. Credentials validation](main7.py)

implement the  `Auth.valid_login`  method. It should expect  `email`  and  `password`  required arguments and return a boolean.

Try locating the user by email. If it exists, check the password with  `bcrypt.checkpw`. If it matches return  `True`. In any other case, return  `False`.
```
bob@dylan:~$ python3 main7.py
True
False
False
bob@dylan:~$ 
```

### [10. Get session ID](main8.py)

implement the  `Auth.create_session`  method. It takes an  `email`  string argument and returns the session ID as a string.

The method should find the user corresponding to the email, generate a new UUID and store it in the database as the user’s  `session_id`, then return the session ID.

```
bob@dylan:~$ python3 main8.py
5a006849-343e-4a48-ba4e-bbd523fcca58
None
bob@dylan:~$ 
```

### 11. Log in
implement a  `login`  function to respond to the  `POST /sessions`  route.

The request is expected to contain form data with  `"email"`  and a  `"password"`  fields.

If the login information is incorrect, use  `flask.abort`  to respond with a 401 HTTP status.

Otherwise, create a new session for the user, store it the session ID as a cookie with key  `"session_id"`  on the response and return a JSON payload of the form

_Terminal 1:_
```
bob@dylan:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a prod http://0.0.0.0:5000/ (Press CTRL+C to quit)uction WSGI server instead.
 * Debug mode: off
 * Running on

```
_Terminal 2:_
```
bob@dylan:~$ curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
{"email":"bob@bob.com","message":"user created"}
bob@dylan:~$ 
bob@dylan:~$  curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=163fe508-19a2-48ed-a7c8-d9c6e56fabd1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:34 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
bob@dylan:~$ 
bob@dylan:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=BlaBla' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 34
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 34 out of 34 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: text/html; charset=utf-8
< Content-Length: 338
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:45 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
* Closing connection 0
bob@dylan:~$ 
```
### 15. User profile

Implement a  `profile`  function to respond to the  `GET /profile`  route.

The request is expected to contain a  `session_id`  cookie. Use it to find the user. If the user exist, respond with a 200 HTTP status and the following JSON payload:
```
{"email": "<user email>"}
```
If the session ID is invalid or the user does not exist, respond with a 403 HTTP status.
_Terminal 1:_
```
bob@dylan:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```
_Terminal 2:_
```
bob@dylan:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=75c89af8-1729-44d9-a592-41b5e59de9a1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:15:57 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
bob@dylan:~$
bob@dylan:~$ curl -XGET localhost:5000/profile -b "session_id=75c89af8-1729-44d9-a592-41b5e59de9a1"
{"email": "bob@bob.com"}
bob@dylan:~$ 
bob@dylan:~$ curl -XGET localhost:5000/profile -b "session_id=nope" -v
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /profile HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Cookie: session_id=75c89af8-1729-44d9-a592-41b5e59de9a
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: text/html; charset=utf-8
< Content-Length: 234
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:16:43 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>403 Forbidden</title>
<h1>Forbidden</h1>
<p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>
* Closing connection 0

bob@dylan:~$ 
```
