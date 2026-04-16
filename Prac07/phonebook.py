import csv
from connect import connect

# создание таблицы
def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully")

# вставка из CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted")

# вставка из консоли
def insert_from_console():
    conn = connect()
    cur = conn.cursor()
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added")

# обновление контакта
def update_contact():
    conn = connect()
    cur = conn.cursor()
    name = input("Enter name to update: ")
    new_name = input("New name (leave empty to skip): ") 
    new_phone = input("New phone (leave empty to skip): ")
    if new_name:
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, name)
        )
    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, name)
        )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated")

# поиск контактов


# удаление контакта
def delete_contact():
    conn = connect()
    cur = conn.cursor()
    choice = input("Delete by (1) name or (2) phone: ")
    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    else:
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted")

# меню
def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()
