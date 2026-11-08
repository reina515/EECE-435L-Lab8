import sqlite3


# opens a connection to the database file so we can run queries
def connect_to_db():
    conn = sqlite3.connect('database.db')
    # this lets us read each row like a dictionary, using the column names
    conn.row_factory = sqlite3.Row
    return conn


# creates the users table if it doesn't already exist
def create_db_table():
    conn = connect_to_db()
    try:
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
        print("User table ready")
    except Exception as e:
        print("User table creation failed:", e)
    finally:
        # always close the connection, even if something went wrong
        conn.close()


# saves a new user in the table and returns the user that got added
def insert_user(user):
    inserted_user = {}
    new_id = None
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        # the ? marks keep the query safe from sql injection
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        # remember the id the database gave the new user
        new_id = cur.lastrowid
    except Exception:
        # if the insert fails, undo it
        conn.rollback()
    finally:
        conn.close()

    # look the user up again so we return exactly what was saved
    if new_id is not None:
        inserted_user = get_user_by_id(new_id)
    return inserted_user


# grabs all the users from the table and returns them as a list
def get_users():
    users = []
    conn = connect_to_db()
    try:
        rows = conn.execute("SELECT * FROM users").fetchall()
        # turn each row into a normal dictionary so it can be sent as json
        users = [dict(row) for row in rows]
    except Exception:
        users = []
    finally:
        conn.close()
    return users


# looks up a single user using their id
def get_user_by_id(user_id):
    user = {}
    conn = connect_to_db()
    try:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        # only fill in the user if we actually found one
        if row:
            user = dict(row)
    except Exception:
        user = {}
    finally:
        conn.close()
    return user


# changes a user's details and returns the updated version
def update_user(user):
    updated_user = {}
    ok = False
    conn = connect_to_db()
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        ok = True
    except Exception:
        # if the update fails, undo it
        conn.rollback()
    finally:
        conn.close()

    # if it worked, fetch the user again to send back the new info
    if ok:
        updated_user = get_user_by_id(user["user_id"])
    return updated_user


# removes a user from the table and says whether it worked
def delete_user(user_id):
    message = {}
    conn = connect_to_db()
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception:
        # if the delete fails, undo it and say so
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message


# running this file on its own just sets up the users table
if __name__ == "__main__":
    create_db_table()
