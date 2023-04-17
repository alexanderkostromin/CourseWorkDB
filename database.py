import sqlite3

import config
from client import Client
from worker import Worker
from application import Application


def create_connection():
    db_connection = None
    try:
        db_connection = sqlite3.connect(config.db_name)
        # print(f"Connected to SQLite version {sqlite3.version}")
    except sqlite3.Error as e:
        print(e)
    return db_connection


def registrate_client(db_connection, new_client: Client) -> bool:
    if new_client.name == '' or new_client.surname == '' or new_client.surname == '' or new_client.password == '':
        return False
    insert_client(db_connection, new_client)

    return True


def insert_client(db_connection, new_client: Client):
    c = db_connection.cursor()
    c.execute("INSERT INTO Client (client_name, client_surname, client_email, "
              "client_phone, client_login, client_password) VALUES (?,?,?,?,?,?)",
              (new_client.name, new_client.surname, new_client.email,
               new_client.phone, new_client.login, new_client.password))
    db_connection.commit()


def select_client(db_connection, login, password):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Client WHERE client_login = ? AND client_password = ?", (login, password))
    client = c.fetchall()
    return client


def select_client_by_id(db_connection, client_id):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Client WHERE id = ?", str(client_id))
    client = c.fetchall()
    return client


def select_client_id(db_connection, login, password):
    c = db_connection.cursor()
    c.execute("SELECT id FROM Client WHERE client_login = ? AND client_password = ?", (login, password))
    client_id = c.fetchall()
    return client_id[0]


def select_client_name(db_connection, client_id):
    c = db_connection.cursor()
    c.execute("SELECT client_name FROM Client WHERE id = ?", client_id)
    name = c.fetchall()
    return name[0]


def select_clients(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Client")
    clients = c.fetchall()
    return clients


def insert_application(db_connection, new_application: Application):
    c = db_connection.cursor()
    c.execute("INSERT INTO Application (client_id, application_status_id, reply_type_id, "
              "urgency_id, service_id, application_data, date) VALUES (?,?,?,?,?,?,?)",
              (new_application.client_id, new_application.status_id, new_application.reply_type_id,
               new_application.urgency_id, new_application.service_id, new_application.application_data,
               new_application.date))
    db_connection.commit()


def delete_application(db_connection, application_id):
    c = db_connection.cursor()
    c.execute("DELETE FROM Application WHERE id = ?", (application_id, ))
    db_connection.commit()



def select_applications(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Application")
    applications = c.fetchall()
    return applications


def set_application_status(db_connection, application_id, status_id):
    c = db_connection.cursor()
    c.execute("UPDATE Application "
              "SET application_status_id = ? "
              "WHERE id = ?", (status_id, application_id))
    db_connection.commit()


def insert_worker(db_connection, new_worker: Worker):
    c = db_connection.cursor()
    c.execute("INSERT INTO Worker (worker_role_id, worker_name, worker_surname, worker_email, "
              "worker_phone, worker_login, worker_password, worker_experience) VALUES (?,?,?,?,?,?,?,?)",
              (new_worker.role_id, new_worker.name, new_worker.surname, new_worker.email,
               new_worker.phone, new_worker.login, new_worker.password, new_worker.experience))
    db_connection.commit()


def select_worker(db_connection, login, password):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Worker WHERE worker_login = ? AND worker_password = ?", (login, password))
    worker = c.fetchall()
    return worker


def select_workers(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Worker")
    workers = c.fetchall()
    return workers


def select_works(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Worker")
    works = c.fetchall()
    return works


def insert_work(db_connection, worker_id, client_id, service_id, work_status, work_address):
    c = db_connection.cursor()
    c.execute("INSERT INTO Work (worker_id, client_id, work_status_id, work_address) "
              "VALUES (?,?,?,?,?,?,?)", (worker_id, client_id, service_id, work_status, work_address))
    db_connection.commit()


def select_services(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Service")
    services = c.fetchall()
    return services


def select_urgencies(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Urgency")
    urgencies = c.fetchall()
    return urgencies


def select_roles(db_connection):
    c = db_connection.cursor()
    c.execute("SELECT * FROM Role")
    roles = c.fetchall()
    return roles


def create_db_tables(db_connection):
    create_table_urgency(db_connection)
    create_table_application_status(db_connection)
    create_table_reply_type(db_connection)
    create_table_client(db_connection)
    create_table_service(db_connection)
    create_table_application(db_connection)
    create_table_work_status(db_connection)
    create_table_role(db_connection)
    create_table_worker(db_connection)
    create_table_work(db_connection)


def create_table_urgency(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Urgency ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "urgency_name TEXT)")


def create_table_application_status(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Application_status ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "application_status_name TEXT)")


def create_table_reply_type(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Reply_type ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "reply_type_name TEXT)")


def create_table_client(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Client ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_name TEXT, "
              "client_surname TEXT, "
              "client_email TEXT, "
              "client_phone TEXT, "
              "client_login TEXT, "
              "client_password TEXT)")


def create_table_service(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Service ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "service_name TEXT, "
              "collection_name TEXT)")


def create_table_application(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Application ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "client_id INTEGER, "
              "application_status_id INTEGER, "
              "reply_type_id INTEGER, "
              "urgency_id INTEGER, "
              "service_id INTEGER, "
              "application_data TEXT"
              "date TEXT)")


def create_table_work_status(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Work_status ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "work_status_name TEXT)")


def create_table_role(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Role ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "role_name TEXT)")


def create_table_worker(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Worker ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "worker_role_id INTEGER, "
              "worker_name TEXT, "
              "worker_surname TEXT, "
              "worker_email TEXT, "
              "worker_phone TEXT, "
              "worker_login TEXT, "
              "worker_password TEXT, "          
              "worker_experience INTEGER)")


def create_table_work(db_connection):
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Work ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "worker_id INTEGER, "
              "client_id INTEGER, "
              "service_id INTEGER, "
              "work_status_id INTEGER"
              "work_address TEXT)")

# def create_table_wall_material(db_connection):
#     c = db_connection.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS Wall_material ("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "name TEXT, "
#               "description TEXT, "
#               "material_id INTEGER, "
#               "price INTEGER)")
#
#
# def create_table_material(db_connection):
#     c = db_connection.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS Material_type ("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "name TEXT, "
#               "description TEXT, "
#               "price TEXT)")
#
#
# def create_table_foundation_type(db_connection):
#     c = db_connection.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS Foundation_type ("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "name TEXT, "
#               "material_id INTEGER, "
#               "price INTEGER)")
#
#
# def create_table_house_type(db_connection):
#     c = db_connection.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS House_type ("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "type_name TEXT, "
#               "material_id INTEGER, "
#               "price INTEGER)")
#
#
# def create_table_fence_type(db_connection):
#     c = db_connection.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS Fence_type ("
#               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#               "fence_name TEXT, "
#               "description TEXT, "
#               "wall_material_id INTEGER, "
#               "price INTEGER)")

# def select_materials(db_connection):
#     c = db_connection.cursor()
#     c.execute("SELECT * FROM Material_type")
#     materials = c.fetchall()
#     return materials
#
#
# def select_wall_materials(db_connection):
#     c = db_connection.cursor()
#     c.execute("SELECT * FROM Wall_Material")
#     wall_materials = c.fetchall()
#     return wall_materials
#
#
# def select_foundations(db_connection):
#     c = db_connection.cursor()
#     c.execute("SELECT * FROM Foundation")
#     foundations = c.fetchall()
#     return foundations
#
#
# def select_houses(db_connection):
#     c = db_connection.cursor()
#     c.execute("SELECT * FROM House_type")
#     houses = c.fetchall()
#     return houses
#
#
# def select_fences(db_connection):
#     c = db_connection.cursor()
#     c.execute("SELECT * FROM Fence_type")
#     fences = c.fetchall()
#     return fences
