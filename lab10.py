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
                        (5, 'ACE', '87788567575', 'w' ),
                        (6, 'Dark' , '87789668695' , 'm')
                        """)

            def update_contact(conn):
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

            update_contact(conn)
            delete_contact(conn)

except psycopg2.Error as e:
    print("Error connecting to the database:", e)
