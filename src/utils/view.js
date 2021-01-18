function generateHtmlFromTemplateWithContent(content, user) {
  function renderNavbarForUser() {
    return user
      ? `<nav class="navbar navbar-dark bg-dark fixed-top">
          <a class="navbar-brand" href="/">
            <img src="https://picsum.photos/30/30" width="30" height="30" class="d-inline-block align-top" alt="random image" loading="lazy">
            ${user.name || "DDSS"}
          </a>
          <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
            <li class="nav-item active">
              <a class="nav-link" href="/forum">Forum</a>
            </li>
          </ul>
          <form class="form-inline" action="/logout" method="POST">
            <button class="btn btn-light my-2 my-sm-0">Logout</button>
          </form>    
      </nav>`
      : "";
  }

  return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8" />
          <meta http-equiv="X-UA-Compatible" content="IE=edge" />
          <title>DDSS Unsecure Web App</title>
          <meta name="viewport" content="width=device-width, initial-scale=1" />

          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

          <style>
            html,
            body {
              height: 100%;
            }

            html {
              box-sizing: border-box;
            }
            *, *:before, *:after {
              box-sizing: inherit;
            }
            
            body {
              background-color: #f5f5f5;
              padding-top: 120px;
            }

            form .form-control {
              position: relative;
              height: auto;
              padding: 10px;
              font-size: 16px;
              margin-bottom: 16px;
            }

            form.main {
              width: 100%;
              max-width: 460px;
              padding: 15px;
              margin: auto;
            }
          </style>

        </head>
        <body class="text-center">        
          ${renderNavbarForUser()}
          <main class="wrapper" style="max-width: 980px; margin: 0 auto; text-align:center">
            ${content}
          </main>
        </body>
      </html>
    `;
}

function loginFormPage() {
  return generateHtmlFromTemplateWithContent(`
      <form class="main" action="/sessions" method="POST">
        <img class="mb-4" src="https://picsum.photos/96/96" alt="" width="96" height="96">
        <h1 class="h3 mb-4 font-weight-normal">Login</h1>

        <label for="email" class="sr-only">Email</label>
        <input id="email" name="email" type="email" class="form-control" placeholder="Your email" required>

        <label for="password" class="sr-only">Password</label>
        <input id="password" type="password" name="password" class="form-control" placeholder="Create a password" required>      

        <button class="btn btn-lg btn-primary btn-block" type="submit">Login</button>            
        <a class="btn btn-lg btn-secondary btn-block" href="/sign_up">Register</a>            
      </form>
    `);
}

function signUpFormPage() {
  return generateHtmlFromTemplateWithContent(`
    <form class="main" action="/users" method="POST">
      <img class="mb-4" src="https://picsum.photos/96/96" alt="" width="96" height="96">
      <h1 class="h3 mb-4 font-weight-normal">Register your acccount</h1>

      <label for="name" class="sr-only">Name</label>
      <input id="name" name="name" class="form-control" placeholder="Your name" required autofocus>
      
      <label for="email" class="sr-only">Email</label>
      <input id="email" name="email" type="email" class="form-control" placeholder="Your email" required>

      <label for="password" class="sr-only">Password</label>
      <input id="password" name="password" type="password" class="form-control" placeholder="Create a password" required>      

      <button class="btn btn-lg btn-primary btn-block" type="submit">Register</button>   
      <a class="btn btn-lg btn-secondary btn-block" href="/login">Login</a>               
    </form>
  `);
}

function userPage({ user, queryParams }) {
  return generateHtmlFromTemplateWithContent(
    `
    ${
      queryParams && queryParams.successMessage
        ? `<div class="alert alert-success" role="alert">${queryParams.successMessage}</div>`
        : ""
    }

    <h1 class="h3 mb-4 font-weight-normal">Movements ${
      queryParams.search ? `for ${queryParams.search}` : ""
    }</h1>

    <form class="mb-4" action="/users/${user.id}" method="GET">
      <div class="form-row align-items-center justify-content-center">
        <div class="col-auto">
          <label for="search" class="sr-only">Search by</label>
          <input class="form-control mb-2" id="search" name="search" placeholder="Search by description">
        </div>

        <button type="submit" class="btn btn-primary mb-2">Search</button>  
      </div>         
    </form>

    ${
      queryParams.search
        ? `<ul class="list-group mt-4 mb-4">
        ${user.movements
          .map(function movementHtml(m) {
            return `<li class="list-group-item">${m.description} - ${m.amount}€</li>`;
          })
          .join("")}
       </ul>
      `
        : ""
    }

    <h2 class="h3 mb-4 font-weight-normal">Transfer Money</h2>

    <form class="main" action="/movements" method="GET">
      <label for="to_account_id" class="sr-only">Transfer to</label>
      <input id="to_account_id" name="to_account_id" class="form-control" placeholder="User id to receive amount" required>

      <label for="amount" class="sr-only">Amount</label>
      <input id="amount" name="amount" type="number" class="form-control" placeholder="Amount" required>

      <label for="description" class="sr-only">Description</label>
      <input id="description" name="description" class="form-control" placeholder="Description of movement" required>
          
      <button type="submit" class="btn btn-primary btn-block">Transfer</button>  
    </form>  
  `,
    user
  );
}

function forumPage({ comments = [], queryParams, user }) {
  return generateHtmlFromTemplateWithContent(
    `
    <h1 class="h3 mb-4 font-weight-normal">Add your comment</h1>    
    ${
      queryParams && queryParams.successMessage
        ? `<div class="alert alert-success" role="alert">${queryParams.successMessage}</div>`
        : ""
    }
    <form class="main" action="/comments" method="POST">
      <label for="email" class="sr-only">Email</label>
      <input id="email" name="email" type="email" class="form-control" placeholder="Your email">

      <label for="name" class="sr-only">Name</label>
      <input id="name" name="name" class="form-control" placeholder="Your name" required>

      <label for="comment" class="sr-only">Your comment</label>
      <input id="comment" name="comment" class="form-control" placeholder="Your comment" required>
  
      <button class="btn btn-lg btn-primary btn-block" type="submit">Comment</button>            
    </form>

    <h2 class="h3 mb-4 font-weight-normal">Last comments</h2>

    <ul class="list-group">
      ${comments
        .map(function commentHtml(c) {
          return `<li class="list-group-item">${c.name}<${c.email}>: ${c.comment}</li>`;
        })
        .join("")}
    </ul>       
  `,
    user
  );
}

function errorPage({ errorMessage }) {
  return generateHtmlFromTemplateWithContent(
    `<h1>Error</h1><h2>${errorMessage}</h2>`
  );
}

function notFoundPage(user) {
  return generateHtmlFromTemplateWithContent(
    '<h1>Not Found</h1><a href="/">Go home</a>',
    user
  );
}

exports.loginFormPage = loginFormPage;
exports.signUpFormPage = signUpFormPage;
exports.errorPage = errorPage;
exports.notFoundPage = notFoundPage;
exports.userPage = userPage;
exports.forumPage = forumPage;
