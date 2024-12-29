from flask import current_app

class Plane:
    def __init__(self, name, chair_number,price,id=0):
        self.name = name
        self.chair_number = chair_number
        self.price = price
        self.id = id
        

class PlaneModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_all_planes(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM planes")
        planes = cursor.fetchall()
        cursor.close()
        planes = [Plane(plane[1], plane[2], plane[3],plane[0]) for plane in planes]
        return planes

    def get_plane_by_id(self, plane_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM planes WHERE id = %s", (plane_id,))
        plane = cursor.fetchone()
        cursor.close()
        plane =Plane(plane[1], plane[2], plane[3],plane[0])
        return plane
    def add_plane(self, plane):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO planes (name, chair_number, price) VALUES (%s, %s, %s)",(plane.name, plane.chair_number, plane.price))
        self.mysql.connection.commit()
        plane_id = cursor.lastrowid
        cursor.close()
        return plane_id
    def update_plane(self,plane_id,new_price=-1,new_chair_number=-1):
        cursor=self.mysql.connection.cursor()
        if new_price==-1:
            cursor.execute("UPDATE planes SET chair_number=%s WHERE id=%s",(new_chair_number,plane_id))
        elif new_chair_number==-1:
            cursor.execute("UPDATE planes SET price=%s WHERE id=%s",(new_price,plane_id))
        else:
            cursor.execute("UPDATE planes SET price=%s,chair_number=%s WHERE id=%s",(new_price,new_chair_number,plane_id))
        self.mysql.connection.commit()
        cursor.close()
    def get_plane_price(self,plane_id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM planes WHERE id=%s",(plane_id,))
        plane=cursor.fetchone()
        price=plane[3]
        price=float(price)
        return price
