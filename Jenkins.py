import jenkins
import getpass
import sqlite3


def database(url, job_name, job_status) :
    db = sqlite3.connect('data/jenkins.db')
    db.commit()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jenkins_jobs(id INTEGER PRIMARY KEY,instance_url TEXT, job_name TEXT, job_status TEXT, checked_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    db.commit()

    # Perform insert
    cursor.execute('''INSERT INTO jenkins_jobs(instance_url, job_name, job_status) VALUES(?,?,?)''', (url, job_name, job_status))
    db.commit()

    # Close db
    db.close()


def getRecords(instance_url = "http://localhost:8080") :

    db = sqlite3.connect('data/jenkins.db')
    cursor = db.execute("SELECT * from jenkins_jobs where instance_url like '%s'" % (instance_url))

    print("------------------------------------------------------------------------")
    print("| Job Name        | Timestamp            |  URL                        |")
    print("------------------------------------------------------------------------")
    for row in cursor:
       print("| %s            | %s  |  %s      |" % (row[2], row[4], row[1] ))
    print("------------------------------------------------------------------------")


check = True;
while check:
    # Ask for Jenkins instance from user
    url = input("Enter Jenkins instance (leave blank to use default http://localhost:8080): ")

    # Set default instance if user has the same default
    # Else user input will be used
    if not url or len(url) < 1:
        url = 'http://localhost:8080'

    # Get credentials from users
    username = input("Enter admin username: ")
    password = getpass.getpass(prompt='Enter password: ')

    # Attempt connecting to server using user's credentials
    # username='admin', password='44f1a7a11753446d9274dc9669f46db6'
    try:
        server = jenkins.Jenkins(url, username=username, password=password)

        user = server.get_whoami()
        version = server.get_all_jobs()

        count = 0;
        print("\n fetching logs...")
        print("List of jobs from %s" % (url))
        getRecords(url)
        # for item in version:
        #     database(url, item['name'], item['color']);
        #     count +=1
        #     print("---------------------------- \n")
        #     print("%s: %s Status: [%s]" % (count, item['name'], item['color']))
        #     print("---------------------------- \n")
        break
    except Exception as e:
        print("############## ERROR! ################")
        print("----> %s" % (e))
        print("----> PLEASE TRY AGAIN or use CMD + C to cancel")
        print("############## ====== ################")
    # else:
    #     print("Wrong credentials, please try again")