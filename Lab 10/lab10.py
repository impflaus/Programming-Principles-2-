import psycopg2
import csv

# Подключение к базе данных
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="kaztayd2006"
    )

# Создание таблицы (один раз в начале)
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

# Ввод из консоли
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    print("✅ Contact added!")

# Импорт из CSV
def insert_from_csv(path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    print("📁 CSV data imported!")

# Обновление контакта
def update_user(name, new_phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    print("🔄 Contact updated.")

# Показ всех записей
def query_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            for row in cur.fetchall():
                print(row)

# Поиск по имени
def query_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            print(cur.fetchall())

# Удаление записи
def delete_user(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    print("❌ Contact deleted.")

# Главное меню
def menu():
    create_table()  # создаёт таблицу при первом запуске
    while True:
        print("\n📱 PhoneBook Menu")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update contact")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Delete contact")
        print("7. Exit")

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
            print("👋 Bye!")
            break
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    menu()