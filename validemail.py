from database.database import  connect_to_mysql,data_search_email,insert_data_db

conn = connect_to_mysql(
    host='localhost',
    username='root',
    password='',
    database='test'
)

data_search_email(data='example@email.com',connection=conn,table='message')