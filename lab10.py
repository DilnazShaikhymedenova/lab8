import psycopg2 
 
 
conn = psycopg2.connect( 
    host="localhost",  
    dbname="postgres",  
    user="postgres", 
    password="4232", 
    port="5432") 
cur = conn.cursor() 
 
cur.execute("""CREATE TABLE IF NOT EXISTS PhoneBook ( 
    id INTEGER PRIMARY KEY, 
    first_name varchar(255), 
    phone_number varchar, 
    gender char 
)""") 
 
cur.execute("""INSERT INTO PhoneBook 
            (id, first_name, phone_number, gender) VALUES 
            (1, 'Aboo', '87782243451', 'm'), 
            (2, 'N.B', '87752326514', 'm'), 
            (3, 'Qozzy', '87782244444', 'm'), 
            (4, 'Dark', '87777777777', 'm'),
            (5, 'AII', '87788567575', 'w' ) 
            """) 
  
 
 
conn.commit() 
cur.close() 
conn.close()