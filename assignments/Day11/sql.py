import mysql.connector
import streamlit as st

host = "localhost"     
user = "root"          
password = "manager" 
database = "test_db"   


try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    print("Connected to MySQL database!")

    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    st.write("Tables in database:", tables)

    cursor.execute("SELECT * FROM employees LIMIT 5")
    rows = cursor.fetchall()
    
    st.write(rows[0][1],"is working in",rows[0][2],"department with salary",rows[0][3])

    cursor.close()
    conn.close()
    print("Connection closed.")

except mysql.connector.Error as err:
    print("Error:", err)