import pymysql

db_config = {
    'host': 'mysql-12139fd-hr-erp.j.aivencloud.com',
    'user': 'avnadmin',                     
    'password': 'AVNS_Bpoemtss83b6e7ezoz8',
    'database': 'defaultdb',
    'port': 26797,               
    'ssl_ca': '/etc/ssl/certs/ca-certificates.crt'
}

sql_commands = [
    # Drop tables if they exist (so we can start fresh)
    "DROP TABLE IF EXISTS `admin`;",
    "DROP TABLE IF EXISTS `register`;",

    # Create 'admin' table
    """
    CREATE TABLE `admin` (
      `username` varchar(15) NOT NULL PRIMARY KEY,
      `password` varchar(15) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # Insert data into 'admin'
    "INSERT INTO `admin` (`username`, `password`) VALUES ('admin', 'admin');",
    "INSERT INTO `admin` (`username`, `password`) VALUES ('prince', 'prince123');",

    # Create 'register' table
    """
    CREATE TABLE `register` (
      `emp_id` int(11) NOT NULL,
      `emp_name` varchar(50) NOT NULL,
      `emp_email` varchar(40) NOT NULL,
      `emp_mobile` bigint(20) DEFAULT NULL,
      `emp_designation` varchar(40) DEFAULT NULL,
      `emp_salary` int(11) NOT NULL,
      PRIMARY KEY (`emp_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # Insert data into 'register'
    "INSERT INTO `register` VALUES (101, 'Pinku Sharma', 'gogisodhi@gmail.com', 9904917000, 'Managing Director', 260000);",
    "INSERT INTO `register` VALUES (102, 'Tapu Gada', 'tipendra@gmail.com', 9924687680, 'Team Leader', 150000);",
    "INSERT INTO `register` VALUES (103, 'Goli Hathi', 'goli@gmail.com', 9428107560, 'Cloud Engineer', 95000);",
    "INSERT INTO `register` VALUES (104, 'Sonu Bhide', 'sonu@gmail.com', 9876543210, 'Senior Software Engineer', 130000);",
    "INSERT INTO `register` VALUES (105, 'Jethalal Gada', 'jetha@gmail.com', 9090909090, 'CEO', 250000);"
]

print("Connecting to Cloud Database...")

# Connect to the database
# Note: We remove 'ssl_ca' here if running on Windows to avoid errors
conn = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database'],
    port=db_config['port']
)

try:
    cursor = conn.cursor()
    print("Connected! Running SQL commands...")
    
    for command in sql_commands:
        cursor.execute(command)
        print(f"Executed: {command[:40]}...")
    
    conn.commit()
    print("\nSUCCESS! Your Cloud Database is now ready with all tables and data.")

except Exception as e:
    print(f"\nERROR: {e}")

finally:
    conn.close()