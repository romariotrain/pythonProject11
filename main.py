import psycopg2


def get_phone_id(cursor, phone):
    cursor.execute("""
        select id from phone where phone=%s;""", (phone,))
    return cur.fetchone()[0]


def client_phone_id(cursor, phone_id):
    cursor.execute("""
            select phone_id from clients_phone where client_id=%s;""", (phone_id,))
    return cur.fetchone()[0]


def get_email_id(cursor, email):
    cursor.execute("""
            select id from clients where email=%s;""", (email,))
    data = cur.fetchone()
    if data == None:
        print('Такого клиента нет')
    else:
        return data[0]


def create_db():
        cur.execute("""
         create table if not exists clients(id serial primary key, 
         name varchar(20) not null,
        surname varchar(30) not null,
        email varchar(50) not null unique);
        """)

        cur.execute("""
         CREATE TABLE IF NOT EXISTS phone 
        (id SERIAL PRIMARY KEY,
        phone integer unique);""")

        cur.execute(""" CREATE TABLE IF NOT EXISTS clients_phone 
        (client_id integer REFERENCES clients(id), 
        phone_id integer REFERENCES phone(id),
        constraint pk primary key (client_id, phone_id));""")


def new_client():
    name_ = input('Введите имя ')
    surname_ = input('Введите фамилию')
    email_ = input('Введите email')
    cur.execute(f""" insert into clients(name, surname, email)
    values(%s,%s,%s);""", (name_, surname_, email_))

    cur.execute(""" select name, surname, email from clients
    ;""")

    print(cur.fetchall())


def new_phone():
    phone_ = int(input('Введите номер телефона'))
    cur.execute(f"""insert into phone(phone)
    values({phone_});""")
    email_ = input('Введите почту владельца телефона')
    phone_id = get_phone_id(cur,phone_)
    email_id = get_email_id(cur, email_)
    if email_id != None:
        cur.execute(f"""insert into clients_phone(phone_id, client_id)
        values('{phone_id}','{email_id}');""")
        cur.execute("""select phone_id, client_id from clients_phone""")
    print(cur.fetchall())


def change_client_name():
    email = input('Введите почту человека, данные которого хотите изменить')
    name = input('Введите новое имя')
    client_id = get_email_id(cur, email)
    cur.execute(f"""update clients
    SET name = %s
    where id = %s;""", (name, client_id,))
    cur.execute(f"""select name, surname, email from clients;""")
    print(cur.fetchall())


def change_client_surname():
    email = input('Введите почту человека, данные которого хотите изменить')
    surname = input('Введите новую фамилию')
    client_id = get_email_id(cur, email)
    cur.execute(f"""update clients
    SET surname = %s
    where id = %s;""", (surname, client_id,))
    cur.execute(f"""select name, surname, email from clients;""")
    print(cur.fetchall())


def change_client_email():
    email = input('Введите почту человека, данные которого хотите изменить')
    new_email = input('Введите новую почту')
    client_id = get_email_id(cur, email)
    cur.execute(f"""update clients
    SET email = %s
    where id = %s;""", (new_email, client_id,))
    cur.execute(f"""select name, surname, email from clients;""")
    print(cur.fetchall())


def change_client_phone():
    email = input('Введите почту человека, телефон которого хотите изменить')
    old_phone = input('Введите номер телефона, который хотите изменить')
    new_phone = input('Введите новый номер телефона')
    client_id = get_email_id(cur, email)
    phone_id = client_phone_id(cur, client_id)
    cur.execute(f"""update phone
        SET phone = %s
        where id = %s and phone = %s;""", (new_phone, phone_id, old_phone,))
    cur.execute(f"""select phone from phone;""")
    print(cur.fetchall())


def delete_phone():
    email = input('Введите email человека, телефон которого хотите удалить')
    client_id = get_email_id(cur, email)
    phone_number = input('Введите номер телефона, который хотите удалить')
    phone_id = get_phone_id(cur, phone_number)
    cur.execute(f"""delete from clients_phone
    where phone_id = %s and client_id = %s;""", (phone_id, client_id))
    cur.execute(f"""delete from phone
        where id = %s;""", (phone_id,))
    cur.execute(f"""select phone from phone;""")
    print(cur.fetchall())


def delete_client():
    email = input('Введите почту человека, которого хотите удалить')
    client_id = get_email_id(cur, email)
    cur.execute(f"""delete from clients
    where id = %s;""", (client_id,))
    cur.execute(f"""select name, surname, email from clients;""")
    print(cur.fetchall())


def search_name():
    name = input('Введите имя человека')
    cur.execute(f"""select name, surname from clients
                join clients_phone on clients_phone.client_id = clients.id
                join phone on phone.id = clients_phone.phone_id
                where name = %s""", (name,))
    print(cur.fetchall())


def search_surname():
    surname = input('Введите фамилию человека')
    cur.execute(f"""select name, surname from clients
                join clients_phone on clients_phone.client_id = clients.id
                join phone on phone.id = clients_phone.phone_id
                where surname = %s""", (surname,))
    print(cur.fetchall())


def search_email():
    email = input('Введите почту')
    cur.execute(f"""select name, surname from clients
                join clients_phone on clients_phone.client_id = clients.id
                join phone on phone.id = clients_phone.phone_id
                where email = %s""", (email,))
    print(cur.fetchall())


def search_phone():
    phone = input('Введите номер телефона')
    cur.execute(f"""select name, surname from clients
                join clients_phone on clients_phone.client_id = clients.id
                join phone on phone.id = clients_phone.phone_id
                where phone = %s""", (phone,))
    count = cur.execute(f"""select count()""")
    print(cur.fetchall())


def choose_what_to_change():
    while True:
        b = input("""напишите команду:
              name - изменить имя
              surname - изменить фамилию
              email - изменить электронную почту
              phone - изменить номер телефона
              q - выйти из раздела изменений""")
        if b == 'name':
            change_client_name()
        if b == 'surname':
            change_client_surname()
        if b == 'email':
            change_client_email()
        if b == 'phone':
            change_client_phone()
        if b == 'q':
            break


def find_client():
    while True:
        c = input("""выберите команду:
                  name - искать клиента по имени
                  surname - искать клиента по фамилии
                  email - искать клиента по электронной почте
                  phone - искать клиента по номеру телефона
                  q - выйти из раздела поиска""")
        if c == 'name':
            search_name()
        elif c == 'surname':
            search_surname()
        elif c == 'email':
            search_email()
        elif c == 'phone':
            search_phone()


with psycopg2.connect(database="romario", user="postgres", password="Roma2003") as conn:
    cur = conn.cursor()
    pass
create_db()


def commands():
    while True:
        a = input("""Введите команду. 
        a - добавить нового клиента
        p - добавить номер телефона существующему клиенту
        q - закончить работу
        c - Изменить данные о клиенте
        dp - удалить телефон
        dc - удалить клиента
        f - найти клиента"""
                  )
        if a == 'a':
            new_client()
        elif a == 'p':
            new_phone()
        elif a == 'c':
            choose_what_to_change()
        elif a == 'dp':
            delete_phone()
        elif a == 'dc':
            delete_client()
        elif a == 'f':
            find_client()
        elif a == 'q':
            break
commands()
cur.close()
conn.close()
