# 0x00. Personal data
### 0. Regex-ing

[filtered_logger.py](filtered_logger.py) , [0-main.py](0-main.py)

Write a function called  `filter_datum`  that returns the log message obfuscated:

-   Arguments:
    -   `fields`: a list of strings representing all fields to obfuscate
    -   `redaction`: a string representing by what the field will be obfuscated
    -   `message`: a string representing the log line
    -   `separator`: a string representing by which character is separating all fields in the log line (`message`)
-   The function should use a regex to replace occurrences of certain field values.
-   `filter_datum`  should be less than 5 lines long and use  `re.sub`  to perform the substitution with a single regex.
```
bob@dylan:~$
bob@dylan:~$ ./0-main.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
bob@dylan:~$
```

### 1. Log formatter

[filtered_logger.py](filtered_logger.py) , [1-main.py](1-main.py)

Update  `filtered_logger.py`. with `RedactingFormatter` class

Implement the  `format`  method to filter values in incoming log records using  `filter_datum`. Values for fields in  `fields`  should be filtered.

DO NOT extrapolate  `FORMAT`  manually. The  `format`  method should be less than 5 lines long.
```
bob@dylan:~$
bob@dylan:~$ ./1-main.py
[HOLBERTON] my_logger INFO 2019-11-19 18:24:25,105: name=Bob; email=***; ssn=***; password=***;
bob@dylan:~$
```


### 2. Create logger

[filtered_logger.py](filtered_logger.py) , [2-main.py](2-main.py), [user_data.csv](user_data.csv)

Implement a  `get_logger`  function that takes no arguments and returns a  `logging.Logger`  object.

The logger should be named  `"user_data"`  and only log up to  `logging.INFO`  level. It should not propagate messages to other loggers. It should have a  `StreamHandler`  with  `RedactingFormatter`  as formatter.

Create a tuple  `PII_FIELDS`  constant at the root of the module containing the fields from  `user_data.csv`  that are considered PII.  `PII_FIELDS`  can contain only 5 fields - choose the right list of fields that can are considered as “important” PIIs or information that you  **must hide**  in your logs. Use it to parameterize the formatter.
```
bob@dylan:~$
bob@dylan:~$ ./2-main.py
<class 'logging.Logger'>
PII_FIELDS: 5
bob@dylan:~$
```

### 3. Connect to secure database

[filtered_logger.py](filtered_logger.py) , [3-main.py](3-main.py),  [3-main.sql](3-main.sql), 

Database credentials should NEVER be stored in code or checked into version control. One secure option is to store them as environment variable on the application server.

In this task, you will connect to a secure  `holberton`  database to read a  `users`  table. The database is protected by a username and password that are set as environment variables on the server named  `PERSONAL_DATA_DB_USERNAME`  (set the default as “root”),  `PERSONAL_DATA_DB_PASSWORD`  (set the default as an empty string) and  `PERSONAL_DATA_DB_HOST`  (set the default as “localhost”).

The database name is stored in  `PERSONAL_DATA_DB_NAME`.

Implement a  `get_db`  function that returns a connector to the database (`mysql.connector.connection.MySQLConnection`  object).

-   Use the  `os`  module to obtain credentials from the environment
-   Use the module  `mysql-connector-python`  to connect to the MySQL database (`pip3 install mysql-connector-python`)

```
bob@dylan:~$ 
bob@dylan:~$ cat 3-main.sql | mysql -uroot -p
Enter password: 
bob@dylan:~$ 
bob@dylan:~$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
bob@dylan:~$ 
bob@dylan:~$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./3-main.py
2
bob@dylan:~$
```

### 4. Read and filter data

[filtered_logger.py](filtered_logger.py) , [4-main.sql](4-main.sql)

Implement a  `main`  function that takes no arguments and returns nothing.

The function will obtain a database connection using  `get_db`  and retrieve all rows in the  `users`  table and display each row under a filtered format like this:

```
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);
```

Filtered fields:
-   name
-   email
-   phone
-   ssn
-   password

Only your  `main`  function should run when the module is executed.
```
bob@dylan:~$ 
bob@dylan:~$ cat 4-main.sql | mysql -uroot -p
Enter password: 
bob@dylan:~$ 
bob@dylan:~$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
bob@dylan:~$ 
bob@dylan:~$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./filtered_logger.py
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=60ed:c396:2ff:244:bbd0:9208:26f2:93ea; last_login=2019-11-14 06:14:24; user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36;
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,621: name=***; email=***; phone=***; ssn=***; password=***; ip=f724:c5d1:a14d:c4c5:bae2:9457:3769:1969; last_login=2019-11-14 06:16:19; user_agent=Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;
bob@dylan:~$
```
