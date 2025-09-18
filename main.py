import sqlite3
import re

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")
conn.commit()


def view_phone():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        print("Kontaktlar yo‘q")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")


def contact_manager():
    while True:
        kod = input("1: Add contact\n2: View contacts\n3: Edit contact\n4: Del contact\n5: Exit\nChoose: ")

        if kod == "1":  # Add
            name = input("Name: ")
            phone = input("Phone: ")
            cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
            print("Kontakt qoʻshildi")

        elif kod == "2":  # View
            view_phone()

        elif kod == "3":  # Edit
            view_phone()
            index = input("O‘zgartirmoqchi bo‘lgan kontakt ID sini kiriting: ")
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (index,))
            row = cursor.fetchone()
            if row:
                new_name = input("Yangi ism (bo‘sh qoldirsang o‘zgarmaydi): ")
                new_phone = input("Yangi telefon (bo‘sh qoldirsang o‘zgarmaydi): ")

                if new_name:
                    cursor.execute("UPDATE contacts SET name = ? WHERE id = ?", (new_name, index))
                if new_phone:
                    phone_pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
                    if re.match(phone_pattern, new_phone):
                        cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?", (new_phone, index))
                    else:
                        print("Telefon raqami notoʻgʻri formatda")
                conn.commit()
                print("Kontakt yangilandi")
            else:
                print("ID mavjud emas")

        elif kod == "4":  # Delete
            view_phone()
            index = input("O‘chirmoqchi bo‘lgan kontakt ID sini kiriting: ")
            cursor.execute("DELETE FROM contacts WHERE id = ?", (index,))
            conn.commit()
            print("Kontakt o‘chirildi")

        elif kod == "5":
            print("Dasturdan chiqildi")
            break

        else:
            print("Notoʻgʻri amal")


contact_manager()

conn.close()
