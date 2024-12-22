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

def create_table():
    query = """
    CREATE TABLE test_table
    (
    ID varchar(5),
    name varchar(20),
    primary key(ID)
    )
    """
    cursor.execute(query)
    conn.commit()

def generate_record(cursor, num_records=10000):
    query = """
    INSERT INTO index_test_table (name, video)
    VALUES (%s, %s)
    """
    with open("movie.mp4", "rb") as file:
        video_data = file.read()
    data = []
    test_set = []
    for i in range(1, num_records+1):
        name = ''.join(random.choices(string.ascii_letters, k=10))
        data.append((name, video_data))
        if i % 10 == 0:
            print(f"generating {i}th data", name)
            if i % 1000 == 0:
                test_set.append(name)
            cursor.executemany(query, data)
            data.clear()
    print(f"{num_records} records have been inserted.")
    return test_set

def create_index(cursor):
    query = "CREATE INDEX idx_name ON index_test_table (name)"
    cursor.execute(query)
    print("Index created successfully using ", query)


def test_query_performance(cursor, test_num=10000, test_set=['wiBBxUWFkj'], with_index=False):
    if len(test_set) < 9:
        test_set = ['ZGwsLhwTca', 'wiBBxUWFkj', 'AlvMkSmVhl', 'RyvWUdwZUT', 'tfNLNqXKMi', 'XGlNznpAzn', 'JeucbhYhBA', 'GQWBmOiquB', 'iSprwIxsFS', 'echSxuaiqC']
    start_time = time.time()
    for i in range(test_num):  # 执行多次以平均时间
        query = "SELECT * FROM index_test_table WHERE name = " + "'" + random.choice(test_set) + "'"
        cursor.execute(query)
        cursor.fetchall()
    end_time = time.time()
    duration = end_time - start_time

    print(f"With index: {with_index}, test_num: {test_num}, Total time: {duration:.2f} seconds")
    return duration

def main():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        test_set = []
        if input("if insert data?(y/n): ") == "y":
            test_set = generate_record(cursor, num_records=10000)
            conn.commit()

        test_num = int(input("input test times: "))

        print("no index")
        no_index_time = test_query_performance(cursor, test_num, test_set, with_index=False)

        # 创建索引并测试
        print("createindex")
        create_index(cursor)
        conn.commit()
        
        print("testindex")
        with_index_time = test_query_performance(cursor, test_num, test_set, with_index=True)

        # 保存结果
        with open("test_results.txt", "w") as f:
            f.write(f"Without index: {no_index_time:.2f} seconds\n")
            f.write(f"With index: {with_index_time:.2f} seconds\n")
        print("Test finished, diff: ", with_index_time / no_index_time)
        print("Test results saved to test_results.txt.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
