import psycopg2
import subprocess

def main():
    
    postgresConnection = psycopg2.connect(user="postgres", password="postgres", host="localhost")
    # Obtain a database Cursor
    curr     = postgresConnection.cursor()
    postgresConnection.autocommit = True
    curr.execute("drop database webvalley2022")
    curr.execute("create database webvalley2022")


    create_db = 'psql -U postgres -d webvalley2022 < webvalley2022.sql'
    print("Run SQL script...")
    useless_cat_call = subprocess.call([create_db],  
                                    shell=True,
                                    env={'PGPASSWORD': 'postgres'})


    curr.close()
    postgresConnection.close()
    print("All connections closed")
    
    
if __name__ == "__main__":
    main()