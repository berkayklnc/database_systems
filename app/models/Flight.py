from flask import current_app

class Flight:
    def __init__(
        self,
        origin_city,
        dest_city,
        flight_time,
        travel_time,
        plane_id,
        player_id,
        economy_ticket_price,
        business_ticket_price
    ):
        self.origin_city=origin_city
        self.dest_city=dest_city
        self.flight_time=flight_time
        self.travel_time=travel_time
        self.plane_id=plane_id
        self.player_id=player_id
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
        cursor.execute("INSERT INTO flights (origin_city,dest_city,flight_time,travel_time,plane_id,player_id,economy_ticket_price,business_ticket_price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                      (flight.origin_city,
                      flight.dest_city,
                      flight.flight_time,
                      flight.travel_time,
                      flight.plane_id,
                      flight.player_id,
                      flight.economy_ticket_price,
                      flight.business_ticket_price))
        flight_id=cursor.lastrowid
        cursor.close()
        return flight_id
    def get_flight_by_destination(self,destination):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM flights WHERE dest_city=%s",(destination))
        flight=cursor.fetchnone()
        cursor.close()
        return flight
    def get_flight_by_origin(self,origin):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM flights WHERE origin_city=%s",(origin))
        flight=cursor.fetchnone()
        cursor.close()
        return flight
    def get_direct_flights(self,destination,origin):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM flights WHERE dest_city=%s AND origin_city=%s",(destination,origin))
        flight=cursor.fetchnone()
        cursor.close()
        return flight
    def deleete_flight_by_id(self,id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("DELETE * FROM flights WHERE id=%s",(id))
        flight=cursor.fetchnone()
        cursor.close()
        return flight