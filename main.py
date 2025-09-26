import re
import psycopg2

conn = psycopg2.connect(
    dbname="contacts_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
    text TEXT
);
""")
conn.commit()

class Contact:
    def __init__(self, name, phone):
        self.__name = name
        self.__phone = phone

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        if new_name.strip():
            self.__name = new_name
            return True
        return False

    def get_phone(self):
        return self.__phone

    def set_phone(self, new_phone):
        phone_pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        if re.match(phone_pattern, new_phone):
            self.__phone = new_phone
            return True
        return False

    def __str__(self):
        return self.__phone

    def info(self):
        print(f"Name: {self.__name}\nPhone: {self.__phone}")


def contact_manager():
    while True:
        kod = input("==== Kontakt menejerga xush kelibsiz ====\n1: Add contact\n2: View contacts\n3: Edit contact\n4: Del contact\n5: Exit\nTanlov: ")
        if kod == "1":
            name = input("Name: ")
            contact_phone = input("Phone: ")

            r_name = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
            if re.match(r_name, contact_phone):

                cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, contact_phone))
                conn.commit()
                print("Kontakt qoʻshildi")
            else:
                print("Telefon raqam notoʻgʻri formatda")

        elif kod == "2":

            cur.execute("SELECT id, name, phone FROM contacts")
            rows = cur.fetchall()
            for row in rows:
                print(f"\nID: {row[0]}\nName: {row[1]}\nPhone: {row[2]}")

        elif kod == "3":
            cur.execute("SELECT id, name, phone FROM contacts")
            rows = cur.fetchall()
            for row in rows:
                print(f"{row[0]}. {row[1]} — {row[2]}")

            index = int(input("Oʻzgartirmoqchi boʻlgan kontakt ID sini kiriting: "))
            new_name = input("Yangi ism: ")
            new_phone = input("Yangi telefon: ")

            if new_name:
                cur.execute("UPDATE contacts SET name=%s WHERE id=%s", (new_name, index))
            if new_phone:
                cur.execute("UPDATE contacts SET phone=%s WHERE id=%s", (new_phone, index))
            conn.commit()
            print("Kontakt yangilandi")

        elif kod == "4":
            cur.execute("SELECT id, name, phone FROM contacts")
            rows = cur.fetchall()
            for row in rows:
                print(f"{row[0]}. {row[1]} - {row[2]}")

            index = int(input("Oʻchirmoqchi boʻlgan kontakt ID sini kiriting: "))
            cur.execute("DELETE FROM contacts WHERE id=%s", (index,))
            conn.commit()
            print("Kontakt oʻchirildi")

        elif kod == "5":
            print("Dasturdan chiqildi")
            break
        else:
            print("Notoʻgʻri amal")


def write_sms():
    cur.execute("SELECT id, name, phone FROM contacts")
    contacts = cur.fetchall()
    if not contacts:
        print("Kontaktlar roʻyxati boʻsh")
        return

    print("\n=== SMS Yozish ===")
    for row in contacts:
        print(f"{row[0]}. {row[1]} ({row[2]})")

    try:
        tanlov = int(input("Kimga yozmoqchisiz (ID): "))
        sms = input("SMS matni: ")
        cur.execute("INSERT INTO messages (contact_id, text) VALUES (%s, %s)", (tanlov, sms))
        conn.commit()
        print("SMS muvaffaqiyatli yuborildi")
    except ValueError:
        print("Faqat raqam kiriting")


def view_sms():
    cur.execute("SELECT id, name FROM contacts")
    contacts = cur.fetchall()
    if not contacts:
        print("Kontaktlar roʻyxati boʻsh")
        return

    for row in contacts:
        print(f"{row[0]}. {row[1]}")

    try:
        tanlov = int(input("Qaysi kontaktning SMSlarini koʻrmoqchisiz? (ID): "))
        cur.execute("SELECT id, text FROM messages WHERE contact_id=%s", (tanlov,))
        messages = cur.fetchall()
        if not messages:
            print("SMSlar yoʻq")
        else:
            for msg in messages:
                print(f"{msg[0]}. {msg[1]}")
    except ValueError:
        print("Faqat raqam kiriting")


def edit_sms():
    contact_id = int(input("Qaysi kontakt ID? "))
    cur.execute("SELECT id, text FROM messages WHERE contact_id=%s", (contact_id,))
    messages = cur.fetchall()
    if not messages:
        print("SMSlar yoʻq")
        return

    for msg in messages:
        print(f"{msg[0]}. {msg[1]}")

    sms_id = int(input("Qaysi SMS ID ni o‘zgartirasiz? "))
    new_text = input("Yangi matn: ")
    cur.execute("UPDATE messages SET text=%s WHERE id=%s", (new_text, sms_id))
    conn.commit()
    print("SMS yangilandi")


def delete_sms():
    contact_id = int(input("Qaysi kontakt ID? "))
    cur.execute("SELECT id, text FROM messages WHERE contact_id=%s", (contact_id,))
    messages = cur.fetchall()
    if not messages:
        print("SMS yoʻq")
        return

    for msg in messages:
        print(f"{msg[0]}. {msg[1]}")

    sms_id = int(input("Qaysi SMS ID ni o‘chirasiz? "))
    cur.execute("DELETE FROM messages WHERE id=%s", (sms_id,))
    conn.commit()
    print("SMS oʻchirildi")


def sms_manager():
    while True:
        print("\n=== SMS BOʻLIMI ===")
        print("1. SMS larni koʻrish")
        print("2. Yangi SMS yozish")
        print("3. SMS ni tahrirlash")
        print("4. SMS ni oʻchirish")
        print("5. Chiqish")

        tanlov = input("Tanlovingizni kiriting: ")

        if tanlov == "1":
            view_sms()
        elif tanlov == "2":
            write_sms()
        elif tanlov == "3":
            edit_sms()
        elif tanlov == "4":
            delete_sms()
        elif tanlov == "5":
            print("SMS boʻlimidan chiqildi")
            break
        else:
            print("Notoʻgʻri tanlov. Qayta urinib koʻring")


def main_menu():
    while True:
        print("\n=== SMS managerga xush kelibsiz ===")
        print("1. Kontaktlar")
        print("2. SMS")
        print("3. Chiqish")

        tanlov = input("Tanlovingizni kiriting: ")

        if tanlov == "1":
            contact_manager()
        elif tanlov == "2":
            sms_manager()
        elif tanlov == "3":
            print("Dasturdan chiqildi")
            break
        else:
            print("Notoʻgʻri tanlov. Qayta urinib koʻring")


main_menu()

cur.close()
conn.close()
