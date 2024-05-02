import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="4232",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS PhoneBook ( 
        id INTEGER PRIMARY KEY, 
        first_name varchar(255), 
        phone_number varchar(20), 
        gender char 
    )""")

    # Execute the sample data insertion
    cur.execute("""INSERT INTO PhoneBook 
                (id, first_name, phone_number, gender) VALUES 
                (1, 'Aboo', '87782243451', 'm'), 
                (2, 'N.B', '87752326514', 'm'), 
                (3, 'Qozzy', '87782244444', 'm'), 
                (4, 'Dark', '87777777777', 'm'),
                (5, 'ACE', '87788567575', 'w' ) 
                """)
    
    def update_contact(conn):
        cur_update = conn.cursor()

        # Display current data
        cur_update.execute("SELECT * FROM PhoneBook")
        rows = cur_update.fetchall()
        print("Current data:")
        for row in rows:
            print(row)

        # Ask for details
        id_number = input("Enter the ID number of the contact you want to update: ")
        field = input("Which field do you want to update (name, phone number)? ")
        new_value = input(f"How do you want to change the {field}? ")

        # Update the contact
        try:
            if field.lower() == "name":
                cur_update.execute("UPDATE PhoneBook SET first_name = %s WHERE id = %s", (new_value, id_number))
            elif field.lower() == "phone number":
                cur_update.execute("UPDATE PhoneBook SET phone_number = %s WHERE id = %s", (new_value, id_number))
            else:
                print("Invalid field.")
                return

            conn.commit()
            print("Contact updated successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error updating contact:", e)
        finally:
            cur_update.close()

    update_contact(conn)
except psycopg2.Error as e:
    print("Error connecting to the database:", e)
finally:
    if conn is not None:
        conn.close()
