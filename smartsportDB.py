import pymysql

# Database Configuration
smartsport = {
    'host' : '34.48.139.101',
    'user' : 'root',
    'password' : 'Lordm0ngrel1129?',
    'database' : 'SmartSport',
    'port' : 3306
}

# Establish Database Connection
def db_connection():
    try:
        conn = pymysql.connect(**smartsport, cursorclass=pymysql.cursors.DictCursor)
        return conn
    except pymysql.MySQLError as err:
        print(f"Database connection error: {err}")
        return None