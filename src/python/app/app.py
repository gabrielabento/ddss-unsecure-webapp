#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gabriela Bento Costa <gcosta@student.dei.uc.pt>

import logging, psycopg2
from psycopg2 import sql
import os
from flask import Flask, session, render_template, g, request, redirect, url_for, make_response, escape
import bcrypt
import bleach

app = Flask(__name__)
app.secret_key = 'SlbM1FN50hVC3RD7Eywirg'

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/part1.html", methods=['GET'])
def login():
    return render_template("part1.html")


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

    logger.info("v_password  -> " + password)
    logger.info("v_username  -> " + username)
    logger.info("v_remember  -> " + remember)

    cur.execute("SELECT * FROM users WHERE username='" + username + "'" )
    row = cur.fetchall()

    if row:
        if bcrypt.checkpw(password.encode('utf8'), row[0][1].encode('utf8')):

            # session
            session['username'] = username
            session['password'] = row[0][1]

            conn.close()
            return render_template("part2.html")
        else:
            logger.info("Wrong credentials!")
    else:
        logger.info("No user found!")

    conn.close()
    return render_template("part1.html")


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

    logger.info("c_password  -> " + password)
    logger.info("c_username  -> " + username)
    logger.info("c_remember  -> " + remember)

    cur.execute("SELECT * FROM users WHERE username=%(username)s", {'username' : username})
    row2 = cur.fetchall()

    if row2:
        if bcrypt.checkpw(password.encode('utf8'), row2[0][1].encode('utf8')):

            # session
            session['username'] = username
            session['password'] = row2[0][1]

            conn.close()
            return render_template("part2.html")
        else:
            logger.info("Wrong credentials!")

    else:
        logger.info("No user found!")

    conn.close()
    return render_template("part1.html")



@app.route("/part2.html", methods=['GET'])
def part2():

    return render_template("part2.html")


@app.route("/part2_vulnerable", methods=['GET', 'POST'])
def part2_vulnerable():

    text = request.args.get('v_text')

    logger.info(text)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'templates/part2.html')

    f = open(my_file, 'r')
    indice = 0
    num = 0
    contents = f.readlines()
    for line in contents:
        indice += 1
        l = line.strip()
        if l == '</tbody>':
            num += 1
            if num == 3:
                t = '<tr><td>Vulnerable: '+text+'</td></tr>'
                contents.insert(indice, t)
                ff = open(my_file, 'w')
                contents = "".join(contents)
                ff.write(contents)
                ff.close()
                logger.info(t)

    f.close()

    return render_template("part2.html")


@app.route("/part2_correct", methods=['GET', 'POST'])
def part2_correct():

    text2 = request.args.get('c_text')
    logger.info(text2)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'templates/part2.html')

    f = open(my_file, 'r')
    indice = 0
    contents = f.readlines()
    num = 0
    for line in contents:
        indice += 1
        l = line.strip()
        if l == '</tbody>':
            num += 1
            if num == 3:
                t = '<tr><td>Correct: '+bleach.clean(text2)+'</td></tr>'
                contents.insert(indice, t)
                ff = open(my_file, 'w')
                contents = "".join(contents)
                ff.write(contents)
                ff.close()
                logger.info(t)

    f.close()

    return render_template("part2.html")



@app.route("/part3.html", methods=['GET'])
def part3():


    return render_template("part3.html")


@app.route("/part3_vulnerable", methods=['GET', 'POST'])
def part3_vulnerable():
    conn = get_db()
    cur = conn.cursor()

    # Load inputs
    titulo = request.args.get('v_name')
    autor = request.args.get('v_author')
    categoria = request.args.get('v_category_id') # "" - All, 2 - Databases, 3 - HTML & Web design, 1 - Programming
    price_min = request.args.get('v_pricemin')
    price_max = request.args.get('v_pricemax')
    search = request.args.get('v_search_input')
    search_where = request.args.get('v_search_field') # any - Anywhere, title - Title, authors - Authors, desc - Description, keys - Keywords, notes - Notes
    match = request.args.get('v_radio_match') # any - Any word, all - All words, phrase - Exact phrase
    checkRangeOrFromTo = request.args.get('v_sp_d') # specific - FromTo, custom - Range
    dateRange = request.args.get('v_sp_date_range') # -1 - Anytime, 7 - Within the last week, 14 - Within the last 2 weeks, 30 - Within the last 30 days, 60 - Within the last 60 days, 90 - Within the last 90 days, 180 - Within the last 180 days, 365 - Within the last year, 730 - Within the last two years
    FromMonth = request.args.get('v_sp_start_month') # 0 - Null, 1 - January, 2 - February, 3 - March, 4 - April, 5 - May, 6 - June, 7 - July, 8 - August, 9 - September, 10 - October, 11 - November, 12 - December
    FromDay = request.args.get('v_sp_start_day') # 1 - 31
    FromYear = request.args.get('v_sp_start_year')
    toMonth = request.args.get('v_sp_end_month') # 0 - Null, 1 - January, 2 - February, 3 - March, 4 - April, 5 - May, 6 - June, 7 - July, 8 - August, 9 - September, 10 - October, 11 - November, 12 - December
    toDay = request.args.get('v_sp_end_day') # 1 - 31
    toYear = request.args.get('v_sp_end_year')
    numberOfResultsPerPage = request.args.get('v_sp_c') # 5, 10, 25, 50, 100
    showHideSummaries = request.args.get('v_sp_m') # 1 - with, 0 - without
    sortby = request.args.get('v_sp_s') # 0 - relevance, 1 - date

    flag = 0

    if showHideSummaries == "1": # with summaries
        query = "SELECT * FROM books "
    elif showHideSummaries == "0": # without summaries
        query = "SELECT title FROM books "

    if titulo:
        flag = 1
        query = query + "WHERE title = '"+ titulo + "' "

    if autor:
        if flag != 0:
            query = query + "AND authors = '"+ autor + "' "
        else:
            query = query + "WHERE authors = '"+ autor + "' "
            flag = 1

    if categoria:
        if categoria == "1": # Programming
            if flag != 0:
                query = query + "AND category = 'Programming' "
            else:
                query = query + "WHERE category = 'Programming' "
                flag = 1
        if categoria == "2": # Databases
            if flag != 0:
                query = query + "AND category = 'Databases' "
            else:
                query = query + "WHERE category = 'Databases' "
                flag = 1
        if categoria == "3": # HTML & Web design
            if flag != 0:
                query = query + "AND category = 'HTML & Web design' "
            else:
                query = query + "WHERE category = 'HTML & Web design' "
                flag = 1

    if price_min and price_max:
        if flag != 0:
            query = query + "AND price BETWEEN "+ price_min + " AND " + price_max +" "
        else:
            query = query + "WHERE price BETWEEN "+ price_min + " AND " + price_max + " "
            flag = 1
    if price_min and not price_max:
        if flag != 0:
            query = query + "AND price > "+ price_min + " "
        else:
            query = query + "WHERE price > "+ price_min + " "
            flag = 1
    if price_max and not price_min:
        if flag != 0:
            query = query + "AND price < "+ price_max + " "
        else:
            query = query + "WHERE price < "+ price_max + " "
            flag = 1

    if search:
        if search_where == "any": # Anywhere
            if flag != 0: #
                if match == "any": # Any word
                    query = query + "AND (title LIKE '%"+search+"%' OR authors LIKE '%"+search+"%' OR description LIKE '%"+search+"%' OR keywords LIKE '%"+search+"%' OR notes LIKE '%"+search+"%') "
                else: # All words, Exact phrase
                    query = query + "AND (title = '"+search+"' OR authors = '"+search+"' OR description = '"+search+"' OR keywords = '"+search+"' OR notes = '"+search+"') "
            else:
                if match == "any": # Any word
                    query = query + "WHERE (title LIKE '%"+search+"%' OR authors LIKE '%"+search+"%' OR description LIKE '%"+search+"%' OR keywords LIKE '%"+search+"%' OR notes LIKE '%"+search+"%') "
                else: # All words, Exact phrase
                    query = query + "WHERE (title = '"+search+"' OR authors = '"+search+"' OR description = '"+search+"' OR keywords = '"+search+"' OR notes = '"+search+"') "
                flag = 1

        if search_where == "title": # Title
            if flag != 0:
                if match == "any": # Any word
                    query = query + "AND title LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "AND title = '"+search+"' "
            else:
                if match == "any": # Any word
                    query = query + "WHERE title LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "WHERE title = '"+search+"' "
                flag = 1
        if search_where == "authors": # Authors
            if flag != 0:
                if match == "any": # Any word
                    query = query + "AND authors LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "AND authors = '"+search+"' "
            else:
                if match == "any": # Any word
                    query = query + "WHERE authors LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "WHERE authors = '"+search+"' "
                flag = 1
        if search_where == "desc": # Description
            if flag != 0:
                if match == "any": # Any word
                    query = query + "AND description LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "AND description = '"+search+"' "
            else:
                if match == "any": # Any word
                    query = query + "WHERE description LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "WHERE description = '"+search+"' "
                flag = 1
        if search_where == "keys": # Keywords
            if flag != 0:
                if match == "any": # Any word
                    query = query + "AND keywords LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "AND keywords = '"+search+"' "
            else:
                if match == "any": # Any word
                    query = query + "WHERE keywords LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "WHERE keywords = '"+search+"' "

                flag = 1
        if search_where == "notes": # Notes
            if flag != 0:
                if match == "any": # Any word
                    query = query + "AND notes LIKE '%"+search+"%' "
                else: # All words, Exact phrase 
                    query = query + "AND notes = '"+search+"' "

            else:
                if match == "any": # Any word
                    query = query + "WHERE notes LIKE '%"+search+"%' "
                else: # All words, Exact phrase
                    query = query + "WHERE notes = '"+search+"' "
                flag = 1

    if checkRangeOrFromTo == "custom":
        if dateRange != "-1":
            if flag != 0:
                query = query + "AND book_date BETWEEN CURRENT_DATE-"+dateRange+" AND CURRENT_DATE "
            else:
                query = query + "WHERE book_date BETWEEN CURRENT_DATE-"+dateRange+" AND CURRENT_DATE "
                flag = 1
    else: # specific
        if FromMonth != "0" and FromDay != "0" and FromYear and toMonth != "0" and toDay != "0" and toYear:
            if flag != 0:
                query = query + "AND book_date BETWEEN to_date('"+FromYear+"-"+FromMonth+"-"+FromDay+"','yyyy-mm-dd') AND to_date('"+toYear+"-"+toMonth+"-"+toDay+"','yyyy-mm-dd') "
            else:
                query = query + "WHERE book_date BETWEEN to_date('"+FromYear+"-"+FromMonth+"-"+FromDay+"','yyyy-mm-dd') AND to_date('"+toYear+"-"+toMonth+"-"+toDay+"','yyyy-mm-dd') "
                flag = 1

    #sortBy
    if sortby == 0: # relevance / recomendation
        query = query + "ORDER BY recomendation "
    if sortby == 1: # date
        query = query + "ORDER BY book_date "

    query = query + "LIMIT "+numberOfResultsPerPage+";"

    cur.execute(query)
    resultado = list(cur.fetchall())
    
    # OUTPUT
    out = ""
    num = 0
    for row in resultado:
        i = 0
        num += 1
        for txt in row:
            i += 1
            if i != len(row):
                out = out + str(txt) + ", "
            else:
                out = out + str(txt) + " "

        if num != len(resultado):
            out = out + " ------------------------- "

    logger.info(resultado)

    return out


@app.route("/part3_correct", methods=['GET', 'POST'])
def part3_correct():
    conn = get_db()
    cur = conn.cursor()

    # Load inputs
    titulo = request.args.get('c_name')
    autor = request.args.get('c_author')
    categoria = request.args.get('c_category_id')
    price_min = request.args.get('c_pricemin')
    price_max = request.args.get('c_pricemax')
    search = request.args.get('c_search_input')
    search_where = request.args.get('c_search_field') # any - Anywhere, title - Title, authors - Authors, desc - Description, keys - Keywords, notes - Notes
    match = request.args.get('c_radio_match') # any - Any word, all - All words, phrase - Exact phrase
    checkRangeOrFromTo = request.args.get('c_sp_d') # specific - FromTo, custom - Range
    dateRange = request.args.get('c_sp_date_range') # -1 - Anytime, 7 - Within the last week, 14 - Within the last 2 weeks, 30 - Within the last 30 days, 60 - Within the last 60 days, 90 - Within the last 90 days, 180 - Within the last 180 days, 365 - Within the last year, 730 - Within the last two years
    FromMonth = request.args.get('c_sp_start_month') # 0 - Null, 1 - January, 2 - February, 3 - March, 4 - April, 5 - May, 6 - June, 7 - July, 8 - August, 9 - September, 10 - October, 11 - November, 12 - December
    FromDay = request.args.get('c_sp_start_day') # 1 - 31
    FromYear = request.args.get('c_sp_start_year')
    toMonth = request.args.get('c_sp_end_month') # 0 - Null, 1 - January, 2 - February, 3 - March, 4 - April, 5 - May, 6 - June, 7 - July, 8 - August, 9 - September, 10 - October, 11 - November, 12 - December
    toDay = request.args.get('c_sp_end_day') # 1 - 31
    toYear = request.args.get('c_sp_end_year')
    numberOfResultsPerPage = request.args.get('c_sp_c') # 5, 10, 25, 50, 100
    showHideSummaries = request.args.get('c_sp_m') # 1 - with, 2 - without
    sortby = request.args.get('c_sp_s') # 0 - relevance, 1 - date

    flag = 0

    if showHideSummaries == "1": # with summaries
        query = "SELECT * FROM books "
    elif showHideSummaries == "0": # without summaries
        query = "SELECT title FROM books "

    if titulo:
        flag = 1
        query = query + "WHERE title = %(title)s"

    if autor:
        if flag != 0:
            query = query + "AND authors = %(autor)s "
        else:
            query = query + "WHERE authors = %(autor)s "
            flag = 1

    if categoria:
        if categoria == "1": # Programming
            if flag != 0:
                query = query + "AND category = 'Programming' "
            else:
                query = query + "WHERE category = 'Programming' "
                flag = 1
        if categoria == "2": # Databases
            if flag != 0:
                query = query + "AND category = 'Databases' "
            else:
                query = query + "WHERE category = 'Databases' "
                flag = 1
        if categoria == "3": # HTML & Web design
            if flag != 0:
                query = query + "AND category = 'HTML & Web design' "
            else:
                query = query + "WHERE category = 'HTML & Web design' "
                flag = 1

    if price_min and price_max:
        if flag != 0:
            try:
                query = query + ("AND price BETWEEN %d AND %d " %(int(price_min), int(price_max),))
            except:
                query = query + "AND price = -1 "
                logger.info("Can't parse "+price_min+" and "+price_max)
        else:
            try:
                query = query + ("WHERE price BETWEEN %d AND %d " %(int(price_min), int(price_max),))
            except:
                query = query + "WHERE price = -1 "
                logger.info("Can't parse "+price_min+" and "+price_max)
            flag = 1
    if price_min and not price_max:
        if flag != 0:
            try:
                query = query + ("AND price > %d " %(int(price_min),))
            except:
                query = query + "AND price = -1 "
                logger.info("Can't parse "+price_min)
        else:
            try:
                query = query + ("WHERE price > %d " %(int(price_min),))
            except:
                query = query + "WHERE price = -1 "
                logger.info("Can't parse "+price_min)
            flag = 1
    if price_max and not price_min:
        if flag != 0:
            try:
                query = query + ("AND price < %d " %(int(price_max),))
            except:
                query = query + "AND price = -1 "
                logger.info("Can't parse "+price_max)
        else:
            try:
                query = query + ("WHERE price < %d " %(int(price_max),))
            except:
                query = query + "WHERE price = -1 "
                logger.info("Can't parse "+price_max)
            flag = 1

    if search:
        if search_where == "any": # Anywhere
            if flag != 0: #
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND (title LIKE %(search)s OR authors = %(search)s OR description = %(search)s OR keywords = %(search)s OR notes = %(search)s) "
                else: # All words, Exact phrase
                    query = query + "AND (title = %(search)s OR authors = %(search)s OR description = %(search)s OR keywords = %(search)s OR notes = %(search)s) "

            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE (title LIKE %(search)s OR authors = %(search)s OR description = %(search)s OR keywords = %(search)s OR notes = %(search)s) "
                else: # All words, Exact phrase
                    query = query + "WHERE (title = %(search)s OR authors = %(search)s OR description = %(search)s OR keywords = %(search)s OR notes = %(search)s) "
                flag = 1
        if search_where == "title": # Title
            if flag != 0:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND title LIKE %(search)s "
                else: # All words, Exact phrase
                    query = query + "AND title = %(search)s "
            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE title LIKE %(search)s "
                else: # All words, Exact phrase
                    query = query + "WHERE title = %(search)s "
                flag = 1 
        if search_where == "authors": # Authors
            if flag != 0:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND authors LIKE %(search)s "
                else: # All words, Exact phrase
                    query = query + "AND authors = %(search)s "
            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE authors LIKE %(search)s "
                else: # All words, Exact phrase
                    query = query + "WHERE authors = %(search)s "
                flag = 1
        if search_where == "desc": # Description
            if flag != 0:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND description LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "AND description = %(search)s "
            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE description LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "WHERE description = %(search)s "
                flag = 1
        if search_where == "keys": # Keywords
            if flag != 0:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND keywords LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "AND keywords = %(search)s "
            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE keywords LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "WHERE keywords = %(search)s "

                flag = 1
        if search_where == "notes": # Notes
            if flag != 0:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "AND notes LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "AND notes = %(search)s "

            else:
                if match == "any": # Any word
                    search = "%" + search + "%"
                    query = query + "WHERE notes LIKE %(search)s "
                else: # All words, Exact phrase 
                    query = query + "WHERE notes = %(search)s "
                flag = 1

    if checkRangeOrFromTo == "custom":
        if dateRange != "-1":
            if flag != 0:
                query = query + "AND book_date BETWEEN CURRENT_DATE-"+dateRange+" AND CURRENT_DATE "
            else:
                query = query + "WHERE book_date BETWEEN CURRENT_DATE-"+dateRange+" AND CURRENT_DATE "
                flag = 1
    else: # specific
        if FromMonth != "0" and FromDay != "0" and FromYear and toMonth != "0" and toDay != "0" and toYear:
            if flag != 0:
                query = query + "AND book_date BETWEEN to_date('%(FromYear)s-%(FromMonth)s-%(FromDay)s','yyyy-mm-dd') AND to_date('%(toYear)s-%(toMonth)s-%(toDay)s','yyyy-mm-dd') " %{'FromYear' : FromYear, 'FromMonth' : FromMonth, 'FromDay' : FromDay, 'toYear' : toYear, 'toMonth' : toMonth, 'toDay' : toDay}
            else:
                query = query + "WHERE book_date BETWEEN to_date('%(FromYear)s-%(FromMonth)s-%(FromDay)s','yyyy-mm-dd') AND to_date('%(toYear)s-%(toMonth)s-%(toDay)s','yyyy-mm-dd') " %{'FromYear' : FromYear, 'FromMonth' : FromMonth, 'FromDay' : FromDay, 'toYear' : toYear, 'toMonth' : toMonth, 'toDay' : toDay}
                flag = 1

    #sortBy        
    if sortby == 0: # relevance / recomendation
        query = query + "ORDER BY recomendation "
    if sortby == 1: # date
        query = query + "ORDER BY book_date "

    query = query + "LIMIT "+numberOfResultsPerPage+";"
    
    cur.execute(query,{"title" : titulo, "autor" : autor, "search" : search})
    resultado = cur.fetchall()

    # OUTPUT
    out = ""
    num = 0
    for row in resultado:
        i = 0
        num += 1
        for txt in row:
            i += 1
            if i != len(row):
                out = out + str(txt) + ", "
            else:
                out = out + str(txt) + " "
            
        if num != len(resultado):
            out = out + " ------------------------- "

    logger.info(resultado)

    return out


@app.route("/demo", methods=['GET', 'POST'])
def demo():
    logger.info("\n DEMO \n")

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

    conn.close()
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
    db = psycopg2.connect(user="ddss-database-assignment-2",
    password="ddss-database-assignment-2",
    host="db",
    port="5432",
    database="ddss-database-assignment-2")
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
