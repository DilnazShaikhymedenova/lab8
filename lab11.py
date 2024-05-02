import psycopg2

try:
    with psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="4232",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS PhoneBook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255),
                phone_number VARCHAR(20),
                gender CHAR
            )""")
  #cur.execute - used to execute sql to create table.
            # Execute the sample data insertion
            cur.execute("""INSERT INTO PhoneBook 
                        (first_name, phone_number, gender) VALUES 
                        ('Aboo', '87782243451', 'm'), 
                        ('N.B', '87752326514', 'm'), 
                        ('Qozzy', '87782244444', 'm'), 
                        ('Dark', '87777777777', 'm'),
                        ('ACE', '87788567575', 'w' ) 
                        """)

            def update_contact(conn): #updating the data
                with conn.cursor() as cur_update:
                    # Display current data
                    cur_update.execute("SELECT * FROM PhoneBook")
                    rows = cur_update.fetchall()
                    print("Current data:")
                    for row in rows:
                        print(row)

                    # Ask for details
                    id_number = input("Enter the ID number of the contact you want to update: ")
                    new_name = input("Enter the new name: ")
                    new_phone_number = input("Enter the new phone number: ")

                    try:
                        # Update the name
                        cur_update.execute("UPDATE PhoneBook SET first_name = %s WHERE id = %s", (new_name, id_number))
                        conn.commit()
                        print("Name updated successfully.")

                        # Update the phone number
                        cur_update.execute("UPDATE PhoneBook SET phone_number = %s WHERE id = %s", (new_phone_number, id_number))
                        conn.commit()
                        print("Phone number updated successfully.")
                    except psycopg2.Error as e:
                        conn.rollback()
                        print("Error updating contact:", e)

            def delete_contact(conn):
                with conn.cursor() as cur_delete:
                    # Display current data
                    cur_delete.execute("SELECT * FROM PhoneBook")
                    rows = cur_delete.fetchall()
                    print("Current data:")
                    for row in rows:
                        print(row)

                    # Ask for details
                    id_number = input("Enter the ID number of the contact you want to delete: ")
                    confirm = input(f"Are you sure you want to delete contact with ID {id_number}? (y/n): ")

                    if confirm.lower() == 'y':
                        try:
                            cur_delete.execute("DELETE FROM PhoneBook WHERE id = %s", (id_number,))
                            conn.commit()
                            print("Contact deleted successfully.")
                        except psycopg2.Error as e:
                            conn.rollback()
                            print("Error deleting contact:", e)
                    else:
                        print("Deletion canceled.")
                #this function retrieves records from Phonebook table where the first name or phone number matches the pattern

            def get_records_by_pattern(conn, pattern):
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM PhoneBook WHERE first_name LIKE %s OR phone_number LIKE %s", (f"%{pattern}%", f"%{pattern}%"))
                    rows = cur.fetchall()
                    return rows

            def insert_or_update_user(conn, name, phone):
                with conn.cursor() as cur:
                    try:
                        cur.execute("INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (first_name) DO UPDATE SET phone_number = %s", (name, phone, phone))
                        conn.commit()
                        print("User inserted or updated successfully.")
                    except psycopg2.Error as e:
                        conn.rollback()
                        print("Error inserting or updating user:", e)
            #inserts a new user into the table, or updates the phone number if user already exists.
            #It checks if the name or phonenumber already exists before inserting

            def insert_many_users(conn, users):
                with conn.cursor() as cur:
                    incorrect_data = []
                    for user in users:
                        name, phone = user
                        cur.execute("SELECT id FROM PhoneBook WHERE first_name = %s OR phone_number = %s", (name, phone))
                        existing_id = cur.fetchone()
                        if not existing_id:
                            incorrect_data.append(user)
                        else:
                            cur.execute("INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
                    conn.commit()
                    if incorrect_data:
                        print("Incorrect data:")
                        for data in incorrect_data:
                            print(data)
                        return False, incorrect_data
                    else:
                        print("Users inserted successfully.")
                        return True, None

            def query_data_with_pagination(conn, limit, offset):
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM PhoneBook LIMIT %s OFFSET %s", (limit, offset))
                    rows = cur.fetchall()
                    return rows

            def delete_data_by_username_or_phone(conn, identifier):
                with conn.cursor() as cur:
                    try:
                        cur.execute("DELETE FROM PhoneBook WHERE first_name = %s OR phone_number = %s", (identifier, identifier))
                        conn.commit()
                        print("Data deleted successfully.")
                    except psycopg2.Error as e:
                        conn.rollback()
                        print("Error deleting data:", e)

            pattern = input("Enter a pattern to search for in names or phone numbers: ")
            records = get_records_by_pattern(conn, pattern)
            identifier = input("Enter the username or phone number you want to delete: ")
            delete_data_by_username_or_phone(conn, identifier)      
            print("Records matching the pattern:")
            for record in records:
                print(record)

            users_to_insert = [('Ann', '12345678901'), ('Bruno', '23456789012'), ('Mark', '34567890123'), ('Dave', '45678901234')]
            success, incorrect_data = insert_many_users(conn, users_to_insert)
            if not success:
                print("Insertion failed. Incorrect data:")
                for data in incorrect_data:
                    print(data)

            # Call other functions/procedures as needed

except psycopg2.Error as e:
    print("Error connecting to the database:", e)
