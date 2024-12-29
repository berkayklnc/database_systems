from flask import current_app
import time
import random
class Flight:
    def __init__(
        self,
        origin_city,
        dest_city,
        origin_code,
        dest_code,
        flight_time,
        travel_time,        
        player_plane_id,
        passengers,
        economy_ticket_price,
        business_ticket_price
    ):
        self.origin_city=origin_city
        self.dest_city=dest_city
        self.origin_code=origin_code
        self.dest_code=dest_code
        self.flight_time=flight_time
        self.travel_time=travel_time
        self.player_plane_id=player_plane_id
        self.passengers=passengers
        self.economy_ticket_price=economy_ticket_price
        self.business_ticket_price=business_ticket_price

class FlightModel:
    def __init__(self):
        self.mysql=current_app.config['mysql']
    def get_all_flights(self):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM flights")
        flights=cursor.fetchall()
        cursor.close()
        return flights
    def add_flight(self,flight):
        cursor=self.mysql.connection.cursor()
        cursor.execute("INSERT INTO flights (origin_city, dest_city, origin_code, dest_code, flight_time, travel_time, player_plane_id, passengers, economy_ticket_price, business_ticket_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                      (flight.origin_city,
                      flight.dest_city,
                      flight.origin_code,
                      flight.dest_code,
                      flight.flight_time,
                      flight.travel_time,
                      flight.player_plane_id,
                      0,
                      flight.economy_ticket_price,
                      flight.business_ticket_price))
        flight_id=cursor.lastrowid
        cursor.close()
        return flight_id
    def get_direct_flights(self,origin,destination,flight_time):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM flights WHERE dest_city=%s AND origin_city=%s AND flight_time>= %s ORDER BY economy_ticket_price LIMIT 20",(destination,origin,flight_time))
        flights=cursor.fetchall()
        cursor.close()
        return flights
    def delete_flight_by_id(self,id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("DELETE * FROM flights WHERE id=%s",(id))
        self.mysql.connection.commit()
        flight=cursor.fetchnone()
        cursor.close()
        return flight
    def get_transfered_flights(self,origin,destination,flight_time):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT f1.id,f2.id,f1.origin_city as origin_city,f1.dest_city as transfer,f2.dest_city as dest_city,f1.origin_code as origin_code,f2.dest_code as dest_code,f1.flight_time as first_time,f2.flight_time as second_time,f1.player_plane_id,f2.player_plane_id,f1.passengers,f2.passengers,f1.economy_ticket_price,f2.economy_ticket_price ,f1.business_ticket_price,f2.business_ticket_price,f1.travel_time,f2.travel_time FROM flights f1 INNER JOIN flights f2 ON f1.dest_city=f2.origin_city WHERE f1.origin_city=%s AND f2.dest_city=%s AND f1.flight_time>= %s AND f2.flight_time > (f1.flight_time + INTERVAL f1.travel_time MINUTE) ORDER BY (f1.economy_ticket_price + f2.economy_ticket_price) LIMIT 10",(origin,destination,flight_time))
        flights=cursor.fetchall()
        cursor.close()
        return flights
    def fill_flight(self,origin_code,dest_code,base,chance,flight_id,player_id):
        cursor=self.mysql.connection.cursor()
        route=origin_code+'-'+dest_code
        cursor.execute("SELECT ratio FROM priors WHERE route=%s",(route,))
        ratio=cursor.fetchone()
        cursor.close()
        if ratio!=None:
            ratio=ratio[0]
        else:
            ratio=None
        passengers=0
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT chair_number FROM planes WHERE id=(SELECT plane_id FROM players_plane WHERE id=(SELECT player_plane_id FROM flights WHERE id=%s))",(flight_id,))
        seats=cursor.fetchone()
        cursor.close()
        seats=seats[0]
        if seats==None:
            per_second=3
        elif ratio==0 or ratio==None:
            per_second=2
        else:
            per_second=60/(base*ratio)  #MEDİUM BASE 80 EASY BASE 100 HARD BASE 60
        duration = 107
        start_time = time.time()
        while time.time() - start_time < duration:
            if passengers<=seats:
                if random.random() < chance:  # Random chance based on y
                    cursor=self.mysql.connection.cursor()
                    cursor.execute("UPDATE flights SET passengers=passengers+1 WHERE id=%s",(flight_id,))
                    self.mysql.connection.commit()
                    cursor.close()
                    passengers=passengers+1
                time.sleep(per_second)  
        economy_pass=int(float(passengers)*0.7)
        business_pass=passengers-economy_pass
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT business_ticket_price,economy_ticket_price FROM flights WHERE id=%s",(flight_id,))
        prices=cursor.fetchone()
        cursor.close()
        economy=prices[1]
        business=prices[0]
        gain_eco=economy*economy_pass
        gain_busi=business*business_pass
        gain=gain_eco+gain_busi
        cursor=self.mysql.connection.cursor()
        cursor.execute("UPDATE players SET balance=balance+%s WHERE id=%s",(gain,player_id))

