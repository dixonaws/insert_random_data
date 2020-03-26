import mysql.connector
import random
import string
import time
from progress.bar import Bar

cnx=mysql.connector.connect(database='test')
cursor=cnx.cursor(buffered=True)

def random_string(int_length):
    str_letters=string.ascii_lowercase
    return(''.join(random.choice(str_letters) for i in range(int_length)))

def insert(): 
    str_random_chars=random_string(1024)
    insert_query=("INSERT INTO random VALUES('" + str_random_chars + "')")

    cursor.execute(insert_query)

def select():
    select_query=("SELECT * FROM random")

    cursor.execute(select_query)
    results=cursor.fetchall()
    print(results)
        
def get_size():
    size_query=("SELECT table_schema ' Database Name' , SUM(data_length+index_length)/1024/1024 ' Database Size (MB)'   FROM information_schema.TABLES GROUP BY table_schema")
    cursor.execute(size_query)
    results=cursor.fetchall()
    print(results)


get_size()

bar=Bar('INSERTing 10,000 1kb records...', max=100)

# insert 1000 records in the database
current_time=int(round(time.time()*1000))

for i in range(100):
    for j in range(100):
        insert()
    
    cnx.commit()
    bar.next()

bar.finish()

new_time=int(round(time.time()*1000))
elapsed_time=new_time-current_time

print("Inserted 1,000 records in " + str(elapsed_time) + "ms.")

get_size()

# select()

cursor.close()
cnx.close()

