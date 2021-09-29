import sqlite3

con = sqlite3.connect("secret/vt.db")
cursor = con.cursor()

def cr_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS passs (id INTEGER NOT NULL, service TEXT NOT NULL, passw TEXT NOT NULL, CONSTRAINT pk PRIMARY KEY (id))")
    con.commit()
    return True

def add_data(service, password):
    cursor.execute("INSERT INTO passs (service, passw) VALUES(?,?)",("{}".format(service),"{}".format(password)))
    con.commit()

def get_data(service):
    cursor.execute("SELECT * FROM passs WHERE service = '{}'".format(service))
    data = cursor.fetchall()
    return data

def get_all_data():
    cursor.execute("SELECT id, service FROM passs")
    data = cursor.fetchall()
    return data

def mod_data(id:int, newservice, newpassword):
    cursor.execute("UPDATE passs SET passw=? , service=? WHERE id = ?", ("{}".format(newpassword), "{}".format(newservice), "{}".format(id)))
    con.commit()
    return True

def del_data(id:int):
    cursor.execute("DELETE FROM passs WHERE id={}".format(id))
    return True


