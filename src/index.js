/* External dependencies */
const http = require("http");
const { resolve } = require("path");
const { parse } = require("url");
const querystring = require("querystring");

/* Database helpers */
const Db = require("./utils/db");

/* View helpers */
const View = require("./utils/view");

/* Cookie helpers */
const Cookie = require("./utils/cookie");

const requestListener = function (req, res) {
  let path = parse(req.url).pathname;

  /* Handle routes */
  /* FIXME: protect route for not authenticated or not authorized users */
  if (path === "/sign_up" && req.method === "GET") {
    handleSignUpRoute(req, res);
  } else if (path === "/login" && req.method === "GET") {
    handleLoginRoute(req, res);
  } else if (path === "/logout" && req.method === "POST") {
    handleLogoutRoute(req, res);
  } else if (path.startsWith("/movements") && req.method === "GET") {
    handleMovementCreationRoute(req, res);
  } else if (path.startsWith("/users") && req.method === "POST") {
    handleAccountCreationRoute(req, res);
  } else if (path === "/sessions" && req.method === "POST") {
    handleLoginValidationRoute(req, res);
  } else if (path === "/" && req.method === "GET") {
    handleHomeRoute(req, res);
  } else if (path.startsWith("/users/") && req.method === "GET") {
    handleUserPageRoute(req, res);
  } else if (path.startsWith("/forum") && req.method === "GET") {
    handleForumPageRoute(req, res);
  } else if (path.startsWith("/comments") && req.method === "POST") {
    handleCommentCreationRoute(req, res);
  } else {
    handleNotFoundPageRoute(req, res);
  }
};

const server = http.createServer(requestListener);
server.listen(8080);

function handleSignUpRoute(req, res) {
  res.writeHead(200, { "Content-Type": "text/html" });
  res.write(View.signUpFormPage());
  res.end();
}

function handleLoginRoute(req, res) {
  res.writeHead(200, { "Content-Type": "text/html" });
  res.write(View.loginFormPage());
  res.end();
}

function handleLogoutRoute(req, res) {
  const sessionId = Cookie.parse(req.headers.cookie).ddss_session;

  Db.deleteSessionById({
    sessionId,
    onSuccess: function onSuccess() {
      res.writeHead(302, {
        Location: "/login",
        "Set-Cookie": "ddss_session=; expires=Thu, 01 Jan 1970 00:00:00 GMT",
      });
      res.end();
    },
    onError: function onError(errorMessage) {
      handleErrorPageRoute(errorMessage, res);
    },
  });
}

function handleAccountCreationRoute(req, res) {
  processPostData(req, res, function createUser(userData) {
    // FIXME: Should I validate password strength?
    // FIXME: create salt and hashed_password, is it needed?
    Db.createUser({
      user: userData,
      onSuccess: function onSuccess(result) {
        res.writeHead(302, { Location: "/login" });
        res.end();
      },
      onError: function onError(errorMessage) {
        handleErrorPageRoute(errorMessage, res);
      },
    });
  });
}

function handleLoginValidationRoute(req, res) {
  processPostData(req, res, function createUser(userAuthData) {
    Db.loginUser({
      userAuth: userAuthData,
      onSuccess: function onSuccess(result) {
        /* FIXME: No expiry date defined for session cookie? Should I? */
        res.writeHead(302, {
          Location: `users/${result.accountId}`,
          "Set-Cookie": `ddss_session=${result.sessionId}`,
        });
        res.end();
      },
      onError: function onError(errorMessage) {
        handleErrorPageRoute(errorMessage, res);
      },
    });
  });
}

function handleUserPageRoute(req, res) {
  const urlParsed = parse(req.url);
  const userId = urlParsed.pathname.split("/")[2];
  const queryParams = querystring.parse(urlParsed.query);

  // FIXME: Is it safe to use the userId from url? Could I exploit the user authentication using url as an access control?
  if (userId) {
    Db.fetchUserById({
      userId,
      onSuccess: function (userFromDatabase) {
        const userForView = { id: userId };
        userForView.name = userFromDatabase.name;

        if (queryParams && queryParams.search) {
          Db.userMovements({
            user: { id: userId },
            queryParams,
            onSuccess: function (userMovements) {
              userForView.movements = userMovements;

              res.writeHead(200, { "Content-Type": "text/html" });
              res.write(View.userPage({ user: userForView, queryParams }));
              res.end();
            },
            onError: function (errorMessage) {
              handleErrorPageRoute(errorMessage, res);
            },
          });
        } else {
          res.writeHead(200, { "Content-Type": "text/html" });
          res.write(View.userPage({ user: userForView, queryParams }));
          res.end();
        }
      },
      onError: function (errorMessage) {
        handleErrorPageRoute(errorMessage, res);
      },
    });
  } else {
    handleErrorPageRoute("No user defined", res);
  }
}

function handleMovementCreationRoute(req, res) {
  const urlParsed = parse(req.url);
  const sessionId = Cookie.parse(req.headers.cookie).ddss_session;
  const movementData = querystring.parse(urlParsed.query);

  Db.fetchUserBySessionId({
    sessionId,
    onSuccess: function onSuccess(user) {
      // FIXME: Should I allow the movement if I have no user logged in?
      const userId = user.account_id;
      movementData.from_account_id = userId;

      Db.createMovement({
        movement: movementData,
        onSuccess: function onSuccess(result) {
          res.writeHead(302, {
            Location: `users/${userId}?successMessage=Movement with code ${result.id} was successful`,
          });
          res.end();
        },
        onError: function onError(errorMessage) {
          handleErrorPageRoute(errorMessage, res);
        },
      });
    },
    onError: function onError(errorMessage) {
      handleErrorPageRoute(errorMessage, res);
    },
  });
}

function handleForumPageRoute(req, res) {
  const urlParsed = parse(req.url);
  const sessionId = Cookie.parse(req.headers.cookie).ddss_session;
  const queryParams = querystring.parse(urlParsed.query);

  Db.allPublicComments({
    onSuccess: function (comments) {
      Db.fetchUserBySessionId({
        sessionId,
        onSuccess: function onSuccess(user) {
          res.writeHead(200, { "Content-Type": "text/html" });
          res.write(
            View.forumPage({
              comments,
              queryParams,
              user,
            })
          );
          res.end();
        },
        onError: function onError(errorMessage) {
          handleErrorPageRoute(errorMessage, res);
        },
      });
    },
    onError: function (errorMessage) {
      handleErrorPageRoute(errorMessage, res);
    },
  });
}

function handleCommentCreationRoute(req, res) {
  processPostData(req, res, function createComment(commentData) {
    Db.createComment({
      comment: commentData,
      onSuccess: function onSuccess(result) {
        res.writeHead(302, {
          Location: `/forum?successMessage=Your comment was added`,
        });
        res.end();
      },
      onError: function onError(errorMessage) {
        handleErrorPageRoute(errorMessage, res);
      },
    });
  });
}

function handleHomeRoute(req, res) {
  const sessionId = Cookie.parse(req.headers.cookie).ddss_session;
  Db.fetchUserBySessionId({
    sessionId,
    onSuccess: function onSuccess(user) {
      res.writeHead(302, {
        Location: user ? `/users/${user.account_id}` : "/login",
      });
      res.end();
    },
    onError: function onError(errorMessage) {
      handleErrorPageRoute(errorMessage, res);
    },
  });
}

function handleErrorPageRoute(errorMessage, res) {
  res.writeHead(500, { "Content-Type": "text/html" });
  res.write(View.errorPage({ errorMessage }));
  res.end();
}

function handleNotFoundPageRoute(req, res) {
  res.writeHead(404, { "Content-Type": "text/html" });
  res.write(View.notFoundPage());
  res.end();
}

/* Helper */
function processPostData(req, res, onDataProcessed) {
  let queryData = "";
  req.on("data", function (data) {
    queryData += data;
    if (queryData.length > 1e6) {
      queryData = "";
      res.writeHead(413, { "Content-Type": "text/plain" }).end();
      req.connection.destroy();
    }
  });

  req.on("end", function () {
    const postForm = querystring.parse(queryData);
    onDataProcessed(postForm);
  });
}
