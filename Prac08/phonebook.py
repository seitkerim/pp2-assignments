from connect import connect


# поиск контактов
def search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# insert или update
def upsert(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_user(%s::text, %s::text);", (name, phone))
    conn.commit()

    print("User inserted/updated!")

    cur.close()
    conn.close()


# добавление нескольких пользователей
def insert_many():
    conn = connect()
    cur = conn.cursor()

    names = ["Mary", "Alisher", "Diana"]
    phones = ["12345", "abc123", "67890"]

    cur.execute("CALL insert_many(%s, %s);", (names, phones))
    conn.commit()

    print("Bulk insert done!")

    cur.close()
    conn.close()


# pagination
def paginate(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s);",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# удаление контакта
def delete(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s);", (value,))
    conn.commit()

    print("Deleted!")

    cur.close()
    conn.close()


# меню
def main():
    while True:
        print("\n1. Search")
        print("2. Upsert user")
        print("3. Insert many")
        print("4. Paginate")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            pattern = input("Enter search: ")
            search(pattern)

        elif choice == "2":
            name = input("Name: ")
            phone = input("Phone: ")
            upsert(name, phone)

        elif choice == "3":
            insert_many()

        elif choice == "4":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            paginate(limit, offset)

        elif choice == "5":
            value = input("Enter name or phone: ")
            delete(value)

        elif choice == "0":
            break


if __name__ == "__main__":
    main()