def tomysql(host_name, end_set, end_get, time_stamp, status):
    import mysql.connector
    import socket
    import time

    myConfig = {
        'user': '5cache',
        'password': 'SECRETPASS',
        'host': 'zi5-diamond.zi-5-dev.pl-kra-02.dc4.local',
        'database': '5cachestats',
    }
    try:

        cnx = mysql.connector.connect(**myConfig)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("USER/PASS issue")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("DB does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    # host_name = socket.fqdn()
    add_data = "INSERT INTO 5cachestats.logs VALUES(%r,%r,%r,%r,%r)" % (host_name, end_set, end_get, time_stamp, status)
    cursor.execute(add_data)
    cnx.commit()
    cursor.close()
    cnx.close()
