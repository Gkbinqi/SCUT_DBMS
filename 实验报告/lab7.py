import mysql.connector
import random
import string
import time

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql',
    'database': 'university'
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def create_table(cursor):
    query = """
    CREATE TABLE test_table
    (
    ID varchar(5),
    name varchar(20),
    primary key(ID)
    )
    """
    cursor.execute(query)
    print("table created")
    
def generate_record(cursor, num_records=100):
    query = """
    INSERT INTO test_table (ID, name)
    VALUES (%s, %s)
    """
    data = []
    for i in range(1, num_records+1):
        ID = f"{i:05}"
        name = ''.join(random.choices(string.ascii_letters, k=20))
        data.append((ID, name))
        if i % 10 == 0:
            print(f"generating {i}th data", name)
            cursor.executemany(query, data)
            data.clear()
    print(f"{num_records} records have been inserted.")

def modify_record(cursor):
    query = """
    UPDATE test_table
    SET name = 'modifed_name'
    """
    cursor.execute(query)
    print(f"Records have been modified.")

def delete_record(cursor):
    query = """
    DELETE FROM test_table
    """
    cursor.execute(query)
    print(f"Records have been deleted.")



def main():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        input("press to start...")
        create_table(cursor)
        input("press to continue")
        generate_record(cursor, num_records=100)
        conn.commit()
        input("press to continue")
        modify_record(cursor)
        conn.commit()
        input("press to continue")
        delete_record(cursor)
        conn.commit()
        input("press to continue")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
