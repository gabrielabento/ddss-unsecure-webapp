const sqlite3 = require("sqlite3");
const DB_PATH = "./db/baking.db";

function openDbConnection() {
  return new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, function (err) {
    if (err) {
      console.error(err.message);
    }
  });
}

function closeDbConnection(dbConn) {
  dbConn.close(function (err) {
    if (err) {
      console.error(err.message);
    }
  });
}

function createUser({ user, onSuccess, onError }) {
  const db = openDbConnection();

  // insert one row into the user table
  db.run(
    `INSERT INTO user(email, hashed_password, name)
  VALUES ('${user.email}', '${user.password}', '${user.name}')`,
    function (err) {
      if (err) {
        onError(err.message);
      }

      onSuccess({ id: this.lastID });
    }
  );

  // close the database connection
  db.close();
}

function fetchUserBySessionId({ sessionId, onSuccess, onError }) {
  const db = openDbConnection();

  const sqlQuery = `SELECT user.account_id, user.name from user, user_session where user.account_id = user_session.account_id AND user_session.session_id = "${sessionId}"`;
  db.all(sqlQuery, function (err, rows) {
    if (err) {
      onError(err.message);
      return;
    }

    onSuccess(rows.length > 0 ? rows[0] : undefined);
  });

  // close the database connection
  db.close();
}

function fetchUserById({ userId, onSuccess, onError }) {
  const db = openDbConnection();
  const sqlQuery = `SELECT account_id, name from user where account_id =  "${userId}"`;

  db.all(sqlQuery, function (err, rows) {
    if (err) {
      onError(err.message);
      return;
    }

    onSuccess(rows.length > 0 ? rows[0] : undefined);
  });

  // close the database connection
  db.close();
}

function deleteSessionById({ sessionId, onSuccess, onError }) {
  const db = openDbConnection();

  // insert one row into the user table
  db.run(
    `DELETE FROM user_session where user_session.session_id = "${sessionId}"`,
    function (err) {
      if (err) {
        onError(err.message);
      }

      onSuccess();
    }
  );

  // close the database connection
  db.close();
}

function loginUser({ userAuth, onSuccess, onError }) {
  const db = openDbConnection();

  // FIXME: compare it with hashed_password. Need to generate hashed password first.

  // Get user from database with email
  // Compare passwords
  const sqlQuery = `SELECT account_id from user WHERE email="${userAuth.email}" AND hashed_password="${userAuth.password}"`;
  db.all(sqlQuery, function (err, rows) {
    if (err) {
      onError(err.message);
      return;
    }

    if (rows.length > 0) {
      const accountId = rows[0].account_id;

      // create session
      // FIXME: this will create a sequential session id. Is it right? Think about session management best practices
      const insertQuery = `INSERT INTO user_session(account_id, timestamp_creation)
      VALUES (${accountId}, ${Date.now()})`;

      db.run(insertQuery, function (err) {
        if (err) {
          onError(err.message);
        }

        onSuccess({ accountId, sessionId: this.lastID });
      });
    } else {
      onError("Not possible to login");
    }
  });

  // close the database connection
  db.close();
}

function userMovements({ user, queryParams, onSuccess, onError }) {
  const db = openDbConnection();

  const sqlQuery = `SELECT description, amount, to_account_id, from_account_id 
    from movement 
    WHERE description LIKE "%${queryParams.search}%" AND (to_account_id=${user.id} OR from_account_id="${user.id}")`;

  db.all(sqlQuery, function (err, rows) {
    if (err) {
      onError(err.message);
      return;
    }

    const movements = rows.map(function copyMovement(row) {
      return {
        amount: row.amount,
        description: row.description,
        to: row.to_account_id,
        from: row.from_account_id,
      };
    });

    onSuccess(movements);
  });

  // close the database connection
  db.close();
}

function createMovement({ movement, onSuccess, onError }) {
  const db = openDbConnection();

  // insert one row into the movement table
  const insertQuery = `INSERT INTO movement(from_account_id, to_account_id, amount, description)
  VALUES (${movement.from_account_id}, ${movement.to_account_id}, ${movement.amount}, '${movement.description}')`;

  db.run(insertQuery, function (err) {
    if (err) {
      onError(err.message);
    }

    onSuccess({ id: this.lastID });
  });

  // close the database connection
  db.close();
}

function allPublicComments({ onSuccess, onError }) {
  const db = openDbConnection();

  const sqlQuery = `SELECT comment_id, user_email, user_name, comment 
    from comment`;

  db.all(sqlQuery, function (err, rows) {
    if (err) {
      onError(err.message);
      return;
    }

    const comments = rows.map(function copyMovement(row) {
      return {
        id: row.comment_id,
        email: row.user_email,
        name: row.user_name,
        comment: row.comment,
      };
    });

    onSuccess(comments);
  });

  // close the database connection
  db.close();
}

function createComment({ comment, onSuccess, onError }) {
  const db = openDbConnection();

  // insert one row into the movement table
  const insertQuery = `INSERT INTO comment(user_email, user_name, comment)
  VALUES ('${comment.email}', '${comment.name}', '${comment.comment}')`;

  db.run(insertQuery, function (err) {
    if (err) {
      onError(err.message);
    }

    onSuccess({ id: this.lastID });
  });

  // close the database connection
  db.close();
}

exports.createUser = createUser;
exports.fetchUserBySessionId = fetchUserBySessionId;
exports.fetchUserById = fetchUserById;
exports.deleteSessionById = deleteSessionById;
exports.loginUser = loginUser;
exports.userMovements = userMovements;
exports.createMovement = createMovement;
exports.allPublicComments = allPublicComments;
exports.createComment = createComment;
