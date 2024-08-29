import sqlite3

import requests

db = sqlite3.connect('data.db')

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# table structures
cursor.execute("CREATE TABLE IF NOT EXISTS settings (name VARCHAR, value VARCHAR)")
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,emp_no VARCHAR, name VARCHAR, "
               "email VARCHAR)")


def send_emails():
    print("Include the email sending")


def manage_users():
    values = Values(cursor)
    progress = values.get("progress")
    if progress == "":
        print("1. View all")
        print("2. Add user")
        print("3. Search user")
        v = input("Your choice: ")
        values.set("progress", v)
        manage_users()
    else:
        chars = progress.split("*")
        if chars[0] == "1":
            cursor.execute("SELECT * FROM users")
            for row in cursor.fetchall():
                print("Name: " + row[2])
                print("Email: " + row[3])
                print("Emp#: " + row[1] + "\n\n")
            # print all users
        elif chars[0] == "2":
            print("Adding user:\n")
            name = input("Enter name: ")
            email = input("Enter email: ")
            empno = input("Enter emp_no: ")

            cursor.execute("INSERT INTO users (id,emp_no,name,email) VALUES (NULL, ?,?,?)", (empno, name, email))
            db.commit()
            values.set("progress", "")
            print("User added")


def implode(glue, pieces):
    result = ""

    for piece in pieces:
        if result == "":
            result = piece
        else:
            result += glue + piece
    return result


class Values:
    def __init__(self, db):
        self.db: sqlite3.Cursor = db

    def get(self, name):
        value = ""

        self.db.execute("SELECT * FROM settings WHERE name = ?", (name,))
        rows = self.db.fetchall()
        if len(rows) > 0:
            value = rows[0][1]

        return value

    def set(self, name, value):
        self.db.execute("SELECT * FROM settings WHERE name = ?", (name,))
        rows = self.db.fetchall()
        if len(rows) > 0:
            DB.db_update("settings", {"value": value}, {"name": name})
        else:
            db.execute("INSERT INTO settings (name, value) VALUES (?, ?)", (name, value))
        db.commit()


class DB:
    @staticmethod
    def get_data(table: str, where: dict):
        global cursor
        wheres = []
        for key in where.keys():
            wheres.append(key + " = ?")

        cursor.execute("SELECT * FROM " + table + " WHERE " + implode(" AND ", wheres), where.values())

    @staticmethod
    def db_update(table: str, values: dict, where: dict):
        global cursor
        sets = []
        params = []
        for key in values.keys():
            sets.append(key + " = ?")
            params.append(values.get(key))

        wheres = []
        for key in where.keys():
            wheres.append(key + " = ?")
            params.append(where.get(key))

        print("UPDATE " + table + " SET " + implode(", ", sets) + " WHERE " + implode(" AND ", wheres))

        cursor.execute(
            "UPDATE " + table + " SET " + implode(", ", sets) + " WHERE " + implode(" AND ", wheres),
            params
        )
        db.commit()


def http_send(to, heading, message, file_path):
    file = open(file_path, 'rb');

    response = requests.post("https://wikimalawi.com/samples/send_email.php", {
        "to": to,
        "subject": heading,
        "message": message
    }, files={'file':file})

    res = response.json()

    if res['status'] is not None:
        return True
    else:
        print(response)
        return False