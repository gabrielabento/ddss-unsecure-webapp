/* schema */
DROP TABLE IF EXISTS user;
CREATE TABLE user(
   account_id  INTEGER PRIMARY KEY,
   email VARCHAR (50) UNIQUE NOT NULL,
   name VARCHAR (50) NOT NULL,
   hashed_password VARCHAR (512) NOT NULL,
   -- Should be not null, however we start with unsecure authentication
   salt VARCHAR (512)   
);

DROP TABLE IF EXISTS user_session;
CREATE TABLE user_session(
   session_id INTEGER PRIMARY KEY,
   account_id VARCHAR (50) NOT NULL,
   -- it will be used as Unix time ( seconds since the Epoch ). For more information (https://en.wikipedia.org/wiki/Unix_time)
   timestamp_creation INTEGER NOT NULL
);

DROP TABLE IF EXISTS movement;
CREATE TABLE movement(
   movement_id  INTEGER PRIMARY KEY,
   from_account_id INTEGER NOT NULL,
   to_account_id INTEGER NOT NULL,
   amount REAL NOT NULL,
   description VARCHAR (512) NOT NULL
);

DROP TABLE IF EXISTS comment;
CREATE TABLE comment(
   comment_id INTEGER PRIMARY KEY NOT NULL,
   user_email VARCHAR (50) NOT NULL,
   user_name VARCHAR (50) NOT NULL,
   comment VARCHAR (512) NOT NULL
);

/* seeds */
/* Some users */
INSERT INTO user(email, hashed_password, name)
VALUES ('jcfa@dei.uc.pt', '123456', 'João');
INSERT INTO user(email, hashed_password, name)
VALUES ('maria@dei.uc.pt', '123456', 'Maria');
INSERT INTO user(email, hashed_password, name)
VALUES ('ddss@dei.uc.pt', '123456', 'DDSS');

/* Some fake movements */
INSERT INTO movement(from_account_id, to_account_id, amount, description)
VALUES (1, 2, 50, 'Paying the dinner');
INSERT INTO movement(from_account_id, to_account_id, amount, description)
VALUES (1, 3, 30, 'Sharing expenses');
INSERT INTO movement(from_account_id, to_account_id, amount, description)
VALUES (2, 3, 30, 'A gift');
INSERT INTO movement(from_account_id, to_account_id, amount, description)
VALUES (2, 1, 200, 'Rent');

/* Some comments on the Forum */
INSERT INTO comment(user_email, user_name, comment)
VALUES ('jcfa@dei.uc.pt', 'João', 'Show me the money');
INSERT INTO comment(user_email, user_name, comment)
VALUES ('jcfa@dei.uc.pt', 'João', 'This application is great, except for the design and security :)');