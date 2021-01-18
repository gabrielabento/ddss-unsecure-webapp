#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template, g, request, redirect, url_for, make_response, escape
import logging, psycopg2
import bcrypt
import os
from bs4 import BeautifulSoup
import bleach

app = Flask(__name__)
app.secret_key = 'SlbM1FN50hVC3RD7Eywirg'

@app.route("/")
def home():
    return render_template("index.html");


@app.route("/part1.html", methods=['GET'])
def login():
    return render_template("part1.html");


@app.route("/part1_vulnerable", methods=['GET', 'POST'])
def part1_vulnerable():
    logger.info("---- part1_vulnerable ----")

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'GET':
        password = request.args.get('v_password') 
        username = request.args.get('v_username') 
        remember = request.args.get('v_remember') 
    else:
        password = request.form['v_password']
        username = request.form['v_username']
        remember = request.form['v_remember']
        
    logger.info("v_password  -> " + password);
    logger.info("v_username  -> " + username);
    logger.info("v_remember  -> " + remember);

    cur.execute("SELECT * FROM users WHERE username='" + username + "'" )
    row = cur.fetchall()
    
    if row:
        if(bcrypt.checkpw(password.encode('utf8'), row[0][1].encode('utf8'))):
            
            # session  
            session['username'] = username
            session['password'] = row[0][1]

            conn.close ()
            return render_template("part2.html");
        else:
            logger.info("Wrong credentials!")
    else:
        logger.info("No user found!")
        
    conn.close ()
    return render_template("part1.html");


@app.route("/part1_correct", methods=['GET', 'POST'])
def part1_correct():
    logger.info("---- part1_correct ----")

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'GET':
        password = request.args.get('c_password') 
        username = request.args.get('c_username') 
        remember = request.args.get('c_remember') 
    else:
        password = request.form['c_password']
        username = request.form['c_username']
        remember = request.form['c_remember']
    
    logger.info("c_password  -> " + password);
    logger.info("c_username  -> " + username);
    logger.info("c_remember  -> " + remember);

    cur.execute("SELECT * FROM users WHERE username=%(username)s", {'username' : username})
    row2 = cur.fetchall()

    if row2:
        if(bcrypt.checkpw(password.encode('utf8'), row2[0][1].encode('utf8'))):

            # session  
            session['username'] = username
            session['password'] = row2[0][1]

            conn.close ()
            return render_template("part2.html");
        else:
            logger.info("Wrong credentials!")

    else:
        logger.info("No user found!")

    conn.close ()
    return render_template("part1.html");



@app.route("/part2.html", methods=['GET'])
def part2():

    return render_template("part2.html");


@app.route("/part2_vulnerable", methods=['GET', 'POST'])
def part2_vulnerable():
    
    text = request.args.get('v_text') 

    logger.info(text)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'templates/part2.html')
    
    f = open(my_file,'r')
    indice = 0
    num = 0
    contents = f.readlines()
    for line in contents:
        indice += 1
        l = line.strip()
        if(l == '</tbody>'):
            num += 1
            if (num == 3):
                t = '<tr><td>Vulnerable: '+text+'</td></tr>'
                contents.insert(indice, t)
                ff = open(my_file,'w')
                contents = "".join(contents)
                ff.write(contents)
                ff.close()
                logger.info(t)

    f.close()

    return render_template("part2.html");


@app.route("/part2_correct", methods=['GET', 'POST'])
def part2_correct():
    
    text2 = request.args.get('c_text') 
    logger.info(text2)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'templates/part2.html')
    
    f = open(my_file,'r')
    indice = 0
    contents = f.readlines()
    num = 0
    for line in contents:
        indice += 1
        l = line.strip()
        if(l == '</tbody>'):
            num += 1
            if(num == 3):
                t = '<tr><td>Correct: '+bleach.clean(text2)+'</td></tr>'
                contents.insert(indice, t)
                ff = open(my_file,'w')
                contents = "".join(contents)
                ff.write(contents)
                ff.close()
                logger.info(t)

    f.close()

    return render_template("part2.html");



@app.route("/part3.html", methods=['GET'])
def part3():


    return render_template("part3.html");


@app.route("/part3_vulnerable", methods=['GET', 'POST'])
def part3_vulnerable():
    
   

    return "/part3_vulnerable"


@app.route("/part3_correct", methods=['GET', 'POST'])
def part3_correct():
    

    return "/part3_correct"


@app.route("/demo", methods=['GET', 'POST'])
def demo():
    logger.info("\n DEMO \n");   

    conn = get_db()
    cur = conn.cursor()

    logger.info("---- users  ----")
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    for row in rows:
        logger.info(row)

    for row in rows:
        logger.info(row)

    logger.info("---- messages ----")
    cur.execute("SELECT * FROM messages")
    rows = cur.fetchall()
 
    for row in rows:
        logger.info(row)

    logger.info("---- books ----")
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
 
    for row in rows:
        logger.info(row)

    conn.close ()
    logger.info("\n---------------------\n\n") 

    return "/demo"

##########################################################
## HASHING FUNCTIONS
##########################################################

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return [hashed, salt]

##########################################################
## DATABASE ACCESS
##########################################################

def get_db():
    db = psycopg2.connect(user = "ddss-database-assignment-2",
                password = "ddss-database-assignment-2",
                host = "db",
                port = "5432",
                database = "ddss-database-assignment-2")
    return db





##########################################################
## MAIN
##########################################################
if __name__ == "__main__":
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'logs\log_file.log')

    logging.basicConfig(filename=my_file)

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s:  %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    logger.info("\n---------------------\n\n")

    app.run(host="0.0.0.0", debug=True, threaded=True)