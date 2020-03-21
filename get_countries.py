import pandas as pd
import pickle
import MySQLdb
from MySQLdb import escape_string as thwart



connection = MySQLdb.connect(
                            host='localhost', 
                            user = 'root', 
                            password = 'learntocode27', 
                            db = 'flaskproject'
                            )
cursor = connection.cursor()
cursor.execute('DROP TABLE housing')

try:
    cursor.execute("CREATE TABLE housing \
    (country VARCHAR(30), address VARCHAR(40), start_date DATE, end_date DATE,\
    fare DECIMAL(6,3), currency VARCHAR(10), time VARCHAR(20), sum_rub VARCHAR(40), uid INT(11), \
    PRIMARY KEY (start_date, end_date),\
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE)")

except Exception as e:
    print(e)

""" try:
    for key, value in useful_data.iterrows():
        try:
            cursor.execute("INSERT INTO countries (city, country, lat, lng) VALUES (%s, %s, %s, %s)",
                (thwart(value['city_ascii']), thwart(value['country']), thwart(str(value['lat'])), thwart(str(value['lng']))))
            connection.commit()
        except Exception as e:
            print(e)
except Exception as e:
    print(e) """

cursor.execute("SHOW TABLES")
result = cursor.fetchall()
print(list(result))
result = cursor.execute("SELECT * FROM housing")
result = cursor.fetchall()
print(len(result))
cursor.close()
connection.close()






    
    


