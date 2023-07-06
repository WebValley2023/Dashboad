import subprocess
import psycopg2
import paramiko

def main():

    print("Connection to the server...")
    k = paramiko.RSAKey.from_private_key_file("/home/cstefani/.ssh/old/id_rsa")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="20.105.143.189", username="wvuser", pkey=k)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("pg_dump -U postgres -h localhost -d webvalley2022 > webvalley2022.sql")
    ssh_stdin.write('postgres\n')
    print("Creating script SQL file...")
    ssh_stdout.channel.set_combine_stderr(True)
    output = ssh_stdout.readlines()
    ssh.close()
    print("closing connection with the server...")
    
    
    get_db_script = "scp -i ~/.ssh/old/id_rsa wvuser@20.105.143.189:webvalley2022.sql /home/cstefani/Documents/webvalley2022/webvalley-dashboard/plotly-app/pages/utils/debug/webvalley2022.sql"
    print("Downloading script...")
    useless_cat_call = subprocess.run(get_db_script.split(), 
                                    stdout=subprocess.PIPE, 
                                    text=True,)
    print(useless_cat_call.stdout)


    postgresConnection = psycopg2.connect(user="postgres", password="postgres", host="localhost")
    # Obtain a database Cursor
    curr     = postgresConnection.cursor()
    postgresConnection.autocommit = True
    curr.execute("drop database webvalley2022")
    curr.execute("create database webvalley2022")


    create_db = 'psql -U postgres -d webvalley2022 < /home/cstefani/Documents/webvalley2022/webvalley-dashboard/plotly-app/pages/utils/debug/webvalley2022.sql'
    print("Run SQL script...")
    useless_cat_call = subprocess.call([create_db],  
                                    shell=True,
                                    env={'PGPASSWORD': 'postgres'})


    curr.close()
    postgresConnection.close()
    print("All connections closed")
    
    
if __name__ == "__main__":
    main()
