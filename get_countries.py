import pandas as pd
import pickle
import MySQLdb
from MySQLdb import escape_string as thwart

useful_data = pd.read_pickle('countries.pickle')




connection = MySQLdb.connect(
                            host='localhost', 
                            user = 'root', 
                            password = 'learntocode27', 
                            db = 'flaskproject'
                            )
cursor = connection.cursor()
cursor.execute("DROP TABLE countries")
try:

    cursor.execute("CREATE TABLE countries \
    (country_id INT(11) AUTO_INCREMENT PRIMARY KEY, city VARCHAR(30), country VARCHAR(30),\
    lat DECIMAL(5,2), lng DECIMAL(5,2))")

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
result = cursor.execute("SELECT * FROM countries")
result = cursor.fetchall()
print(len(result))
cursor.close()
connection.close()

print(useful_data)





    
    


