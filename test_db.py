import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",   # 🔴 replace this
    database="household_finance"
)

print("Connected Successfully!")

cursor = conn.cursor()
cursor.execute("SHOW TABLES")

for table in cursor:
    print(table)