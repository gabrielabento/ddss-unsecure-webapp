# DDSS - Unsecure web app

The following repository is the code regarding a server side rendering web application to be used during subject of Design and Development of Secure Software for Masters in Informatics Security of University of Coimbra.

Here the student will find a code with flaws to be discovered and solved during the semester.

**Disclaimer**:
A SQLite database is used here to facilitate the setup, that way, there is no need to install a database server, however this is just as an example and **it is not recommended to use SQLite on any software in production**.

## Pre-requisites

- [node v12.13.1+](https://nodejs.org/);
- [npm v6.13.4](https://www.npmjs.com/);

**Note**: npm is installed with node. You should only need to install node.

## IDE - VScode (highly recommended)

We recommend you to install [VSCode](https://code.visualstudio.com/) and [Pretter extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).

You can open this project by double clicking **unsecure-webapp.code-workspace**. With that and, assuming you have installed Prettier extension, you will have your environment formatting the code when you save any file.

## Getting started

Open the terminal. We can even use the integrated terminal on VSCode. For that got to "Terminal" and select "New Terminal" option.

### Install dependencies

It should only be needed the first time or if you remove your node_modules folder of dependencies.

Execute

```
npm install
```

### Start web application server

Execute

```sh
npm start
```

or

```sh
npm start:watch
```

The last command will update your server everytime you do change on your code.

Once you execute the start command the web application should be available at:
http://localhost:8080

## REPL

If you do not want to install those dependencies on your machine you can use the free IDE in browser [REPL](https://repl.it/): "Code and collaborate, without friction.".

You just go to the site, select "Start coding" option and "Import from Github". You could use this repository directly, or fork it to your account.

It is recommend you fork this github repository for your account, because this way we ca do your changes and push those changes to your repository.

## Folders structure

- src/index.js (file to intercept server requests)
- src/utils (helpers to manage database requests, manage cookies and generate html)
  - src/utils/db.js (functions to communicate with database)
  - src/utils/view.js (functions to generate the html to send to user for each case)
  - src/utils/cookie.js (functions to manage cookies)

## SQLite

At **db** folder you will find the initial sql script and the database file (**baking.db**). To solve some of the problems you will need to do some changes on the database.

As graphic user interface you could use the following [application](https://github.com/sqlitebrowser/sqlitebrowser).

To learn how to use SQLite3 on your code you can use the following tutorials [here](https://www.sqlitetutorial.net/sqlite-nodejs).

The inital database contains three users for you to login, with some movements already done:
**jcfa@dei.uc.pt / 123456**
**maria@dei.uc.pt / 123456**
**ddss@dei.uc.pt / 123456**

## Features

This is a simple web application with following features to transfer money:

- Sign Up;
- Login;
- Search for your movements;
- Transfer money;
- Fórum for comments;

## Implementations

This project uses javascript and nodejs with no external libraries or frameworks on purpose, so the code could look more verbose and difficult, however this due to the fact some of the frameworks solve some of the problems of unsecure applications, by default and the point here is to show some of thoses problems.

We prefer to show those problems for you to understand them instead of having some solved by magic.

Having said that, you are allowed, and even encouraged, to redo all the code and use a Framework, like [express](https://expressjs.com/) for example, and change the database engine. However, choose wisely and understand the why for your choice.

## Exercise

Discover flaws and try to solve them. Some of the flaws we are looking for are or related to:

- Authentication and Authorization (some possible improvements):
  - Hash password;
  - Checked hashed password on login;
  - Session Management: no sequential ids;
  - Check strength of password;
  - Expiration date for session cookie;
  - Check authentication and authorization of route (which pages the user are allowed to use);
  - Do not allow hacker manage url to his/her benefit;
- SQL Injection;
- Cross Site Scripting (XSS);
- Cross-site request forgery (CSRF);
- Among others;

## Articles, Tutorials, Tools

Here we leave some resources you can check to help you.

- [Bcrypt lib](https://www.npmjs.com/package/bcrypt);
- [Building your own password hasher in Node.js](https://blog.logrocket.com/building-a-password-hasher-in-node-js/);
- [Implementing two-factor authentication](https://blog.logrocket.com/implementing-two-factor-authentication-using-speakeasy/);

# Authors

- João Antunes <jcfa@dei.uc.pt>
- Nuno Antunes <nmsa@dei.uc.pt>
