import sqlite3
from flask import Flask, jsonify

# create the flask app
app = Flask(__name__)

# the database file that holds our users
DB = "database.db"


# opens a connection to the database file so we can run queries
def connect_to_db():
    conn = sqlite3.connect(DB)
    # this lets us read each row like a dictionary, using the column names
    conn.row_factory = sqlite3.Row
    return conn


# creates the users table if it doesn't already exist
def create_db_table():
    conn = connect_to_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


# returns a list with just the names of all the users
@app.route('/get_users', methods=['GET'])
def get_users():
    conn = connect_to_db()
    # we only need the name column, not the whole row
    rows = conn.execute("SELECT name FROM users").fetchall()
    conn.close()
    # pull the name out of each row and send the list back as json
    return jsonify([row["name"] for row in rows])


# make sure the users table exists, then start the server on port 3000
if __name__ == "__main__":
    create_db_table()
    app.run(host="0.0.0.0", port=3000)
