from flask import current_app
from app.models.Plane import Plane,PlaneModel
class PlayerPlane:
    def __init__(self,id,is_available,plane_id,player_id):
        self.id=id
        self.player_id=player_id
        self.is_available=is_available
        self.plane_id=plane_id
class PlayerPlaneModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']
    def get_planes_by_user_id(self,player_id):
        print(player_id)
        player_id=int(player_id)
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players_plane WHERE player_id=%s",(player_id,))
        playersplanes=cursor.fetchall()
        cursor.close()
        playersplanes = [PlayerPlane(single[0], single[1], single[2],single[3]) for single in playersplanes]
        allmyplanes={}
        for i in range(len(playersplanes)):
            plane=PlaneModel().get_plane_by_id(playersplanes[i].plane_id)
            allmyplanes[playersplanes[i].id]=(plane)
        return allmyplanes
    def get_plane_id(self,player_plane_id):
        player_plane_id=int(player_plane_id)
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players_plane WHERE id=%s",(player_plane_id,))
        plane_id=cursor.fetchone()
        plane_id=plane_id[2]
        plane_id=int(plane_id)
        return plane_id
    def delete_player_plane(self,player_id,plane_id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("DELETE FROM players_plane WHERE player_id=%s AND id=%s",(player_id,plane_id,))
        self.mysql.connection.commit()
        cursor.close()


    