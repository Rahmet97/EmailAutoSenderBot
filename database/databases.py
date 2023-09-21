import psycopg2


def connection():
    return psycopg2.connect(
        dbname='email_sender_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )


def create_table_email():
    con = connection()
    cur = con.cursor()
    cur.execute('''
        create table if not exists email(
            id serial primary key,
            subject varchar(255),
            description text,
            receiver varchar(100),
            send_time timestamp
        )
    ''')
    con.commit()
    con.close()


def insert_email(data:dict):
    con = connection()
    cur = con.cursor()
    cur.execute('''
            insert into email(subject, description, send_time, receiver)
            values (%s, %s, %s, %s)
        ''', (*data.values(),))
    con.commit()
    con.close()


def get_emails():
    con = connection()
    cur = con.cursor()
    cur.execute('''
            select * from email
            where send_time between current_timestamp - interval '20 seconds' and current_timestamp;
        ''')
    row = cur.fetchall()
    con.close()
    return row
