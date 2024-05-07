import mysql.connector
from datetime import datetime,timedelta

def connect_to_mysql(host, username, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Berhasil terhubung ke database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def insert_data_db(connection, table, data):
    try:
        cursor = connection.cursor()

        tablelist = searchtable(connection,table= table)

        sql_insert_query = f"""INSERT INTO {table} ({', '.join(tablelist)}) 
                             VALUES ({', '.join(['%s'] * len(tablelist))})"""
        
        record_to_insert = data

        cursor.executemany(sql_insert_query, record_to_insert)

        connection.commit()
        print("Data berhasil dimasukkan ke database")
    except mysql.connector.Error as err:
        print(f"Error: {err}") 

def searchtable(connection, table):
    cursor = connection.cursor()
    cursor.execute(f"show columns from {table}")
    columns = cursor.fetchall()
    nama_kolom_list = [column[0] for column in columns]

    return nama_kolom_list

def data_search_email(connection,data,table):

    cursor = connection.cursor()
    cursor.execute(f"SELECT email FROM {table} WHERE email = '{data}'")
    results = cursor.fetchall()
    return results

def delete_data(connection,data,table):

    cursor = connection.cursor()
    cursor.execute(f"SELECT email FROM {table} WHERE email = '{data}'")
    results = cursor.fetchall()
    return results

def delete_expired_data(connection):
    cursor = connection.cursor()
    waktu_sekarang = datetime.now()
    batas_waktu = waktu_sekarang - timedelta(hours=2)
    sql_delete_query = f"DELETE FROM message WHERE date < '{batas_waktu}'"
    cursor.execute(sql_delete_query)