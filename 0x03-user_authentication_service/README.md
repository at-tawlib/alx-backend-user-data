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
