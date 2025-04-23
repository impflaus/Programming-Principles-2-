import psycopg2
import csv

def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="kaztayd2006"
    )

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    phone VARCHAR(20)
                )
            """)
    print("📦 Table created.")

# === LAB 10 FUNCTIONS ===
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    print("✅ Contact added!")

def insert_from_csv(path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    print("📁 CSV data imported!")

def update_user(name, new_phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    print("🔄 Contact updated.")

def query_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            for row in cur.fetchall():
                print(row)

def query_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            print(cur.fetchall())

def delete_user(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    print("❌ Contact deleted.")

# === LAB 11 FUNCTIONS ===
def search_by_pattern(pattern):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_by_pattern(%s);", (pattern,))
            for row in cur.fetchall():
                print(row)

def insert_or_update_user(name, phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s, %s);", (name, phone))
    print("✅ User inserted or updated!")

def insert_many_users(names, phones):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_many_users(%s, %s, NULL);", (names, phones))
            print("✅ Bulk insert done. Check for invalids if needed.")

def get_paginated(limit, offset):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_paginated(%s, %s);", (limit, offset))
            for row in cur.fetchall():
                print(row)

def delete_by_name_or_phone(value):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_by_name_or_phone(%s);", (value,))
    print("❌ Contact deleted.")

# === MAIN MENU ===
def menu():
    create_table()
    while True:
        print("\n📱 PhoneBook")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update user")
        print("4. Show all contacts")
        print("5. Search by exact name")
        print("6. Delete by name")
        print("7. Search by pattern")
        print("8. Insert or update")
        print("9. Insert many user")
        print("10. Paginated view")
        print("11. Delete by name or phone")
        print("12. Exit")

        choice = input("Choose: ")

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_from_csv(input("Enter CSV path: "))
        elif choice == '3':
            update_user(input("Name to update: "), input("New phone: "))
        elif choice == '4':
            query_all()
        elif choice == '5':
            query_by_name(input("Name: "))
        elif choice == '6':
            delete_user(input("Name to delete: "))
        elif choice == '7':
            search_by_pattern(input("Enter pattern: "))
        elif choice == '8':
            insert_or_update_user(input("Name: "), input("Phone: "))
        elif choice == '9':
            names = input("Enter names (comma separated): ").split(',')
            phones = input("Enter phones (comma separated): ").split(',')
            if len(names) != len(phones):
                print("❗ Count mismatch")
            else:
                insert_many_users(names, phones)
        elif choice == '10':
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated(limit, offset)
        elif choice == '11':
            delete_by_name_or_phone(input("Enter value: "))
        elif choice == '12':
            print("👋 Bye!")
            break
        else:
            print("❗ Invalid choice")

if __name__ == "__main__":
    menu()