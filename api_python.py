import flask
from flask import request, jsonify
import json

import sqlite3
from sqlite3 import Error

app = flask.Flask(__name__)
app.config["DEBUG"] = True
i = 0


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection("users.db")

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(32) PRIMARY KEY  NOT NULL,
  nickname VARCHAR(11) NOT NULL, 
  username VARCHAR(50)  NOT NULL,
  password  VARCHAR(200) NOT NULL,
  create_time TIMESTAMP(80) NOT NULL,
  status TINYINT(4) NOT NULL 
);
"""
execute_query(connection, create_users_table)  


	


@app.route('/api/admin/users', methods=['GET'])
def get_users():
    # return all users
    conn = sqlite3.connect('users.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM users;').fetchall()
    return jsonify(all_users)



@app.route('/api/users', methods=['POST'])
def create_new_user():
    # add user to DB
	u = json.load(open("new_user.json"))
	user_id = u.pop('id')
	nickname = u.pop('nickname')
	username = u.pop('username')
	password = u.pop('password')
	status = u.pop('status')
	create_user = """
	INSERT INTO
	users (id, nickname, username,password,create_time,status)
	VALUES
	('$user_id', '$nickname','$username','$password', 'CURRENT_TIME()','$status');
	"""
	execute_query(connection,create_user)
	return jsonify({'Success':True}),201

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()