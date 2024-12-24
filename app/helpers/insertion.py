from flask import current_app
import pickle
import pandas as pd
import numpy as np
import random
def int_to_time(num):
    num_str = str(num)
    if len(num_str) == 1:  # 1-digit
        return f"00:0{num}"
    elif len(num_str) == 2:  # 2-digit
        return f"00:{num_str}"
    elif len(num_str) == 3:  # 3-digit
        return f"{num_str[0]}:{num_str[1:]}"
    elif len(num_str) == 4:  # 4-digit
        return f"{num_str[:2]}:{num_str[2:]}"


def insertData():
    mysql=current_app.config['mysql']
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM priors")
    is_empty=cursor.fetchall()
    cursor.close()
    if not is_empty:
        with open('app/helpers/data/priors.pkl', "rb") as pickle_file:
            data = pickle.load(pickle_file)
        keys=list(data.keys())
        for i in range(len(keys)):
            cursor=mysql.connection.cursor()
            cursor.execute("INSERT INTO priors(route,passengers,seats,distance,ratio) VALUES (%s,%s,%s,%s,%s)",(keys[i],data[keys[i]][0],data[keys[i]][1],data[keys[i]][2],data[keys[i]][3]))
            mysql.connection.commit()
            cursor.close()
    #------Inserting game modes
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM game_modes")
    is_empty=cursor.fetchall()
    cursor.close()
    if not is_empty:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO game_modes (id, chance, coin_multiplier, first_balance) VALUES('EASY', 0.90, 2.0, 100000),('MEDIUM', 0.75, 1.5, 75000),('HARD', 0.50, 1.0, 50000);")
        mysql.connection.commit()
        cursor.close()
    
    #------Inserting planes
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM planes")
    is_empty=cursor.fetchall()
    cursor.close()
    if not is_empty:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO planes (name, chair_number, price) VALUES ('Boeing 737', 180, 1000), ('Airbus A320', 150, 950),('Boeing 747', 366, 3800),('Airbus A380', 555, 4450),('Embraer E190', 100, 580),('Bombardier CRJ900', 76, 480),('Cessna Citation X', 12, 230),('Gulfstream G650', 18, 650),('Concorde', 92, 1200),('Boeing 777', 396, 3900);")
        mysql.connection.commit()
        cursor.close()

    #Inserting user0
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    is_empty=cursor.fetchall()
    cursor.close()
    if not is_empty:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, surname, gender) VALUES ('Test22', 'Test', 'male');")
        mysql.connection.commit()
        cursor.close()

    #Inserting root player
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM players")
    is_empty=cursor.fetchall()
    cursor.close()
    if not is_empty:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO players (balance, user_id, password, user_name) VALUES (1500, (SELECT id FROM users WHERE name = 'Test22' AND surname = 'Test'), 'scrypt:32768:8:1$IaMiHGPAYlQOvk33$1e7861e65c06baf878b0028e412c0efa019587e9d6db3b78a5ba0b378b81f08d83e42907631a668ee426c8d0437f0eab5dbc7292f7fe66cb54bfecf314abf9f0', 'root');")
        mysql.connection.commit()
        cursor.close()

    #Inserting basic player-plane
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM players_plane")
    is_empty=cursor.fetchone()
    cursor.close()
    if not is_empty:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO players_plane (is_available,plane_id,player_id) VALUES (TRUE,4,1);")
        mysql.connection.commit()
        cursor.close()
    
    #Inserting Flights
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM flights")
    is_empty=cursor.fetchone()
    cursor.close()
    if not is_empty:

        df=pd.read_csv("app/helpers/data/flights.csv")
        keys=list(df.keys())
        origin_state=np.array(df[keys[0]])
        origin_state=origin_state.reshape(-1,1)

        dest_state=np.array(df[keys[1]])
        dest_state=dest_state.reshape(-1,1)

        origin=np.array(df[keys[2]])
        origin=origin.reshape(-1,1)

        dest=np.array(df[keys[3]])
        dest=dest.reshape(-1,1)

        flight_date=np.array(df[keys[4]])
        flight_date=flight_date.reshape(-1,1)

        flight_hour=np.array(df[keys[5]])
        flight_hour=flight_hour.reshape(-1,1)

        airtime=np.array(df[keys[6]])
        airtime=airtime.reshape(-1,1)
        
        result=np.concatenate((origin_state,dest_state,origin,dest,flight_date,flight_hour,airtime),axis=1)
        long_months=["01","03","05","07","08","10","12"]
        non_febs=["01","03","04","05","06","07","08","09","10","11","12"]
        for i in range(result.shape[0]):
            economy = round(random.uniform(100, 400), 2)
            business = round(random.uniform(500, 900), 2)
            hour=int_to_time(result[i][5])

            if result[i][4][8:]=='31':
                month=long_months[random.randint(0,6)]
            elif result[i][4][8:]=='30':
                month=non_febs[random.randint(0,10)]
            else:
                month=random.randint(1,12)
                month=str(month)
            if len(month)==1:
                month="0"+month
            if result[i][6]!=0:
                date=result[i][4]
                date=date[:5] + month + date[7:]
                date="2024"+date[4:]
                cursor=mysql.connection.cursor()
                cursor.execute("INSERT INTO flights (origin_city, dest_city, origin_code, dest_code, flight_time, travel_time, player_plane_id, passengers, economy_ticket_price, business_ticket_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(result[i][0],result[i][1],result[i][2],result[i][3],(date+' '+hour+':00'),result[i][6],1,0,economy,business))
                mysql.connection.commit()
                cursor.close()