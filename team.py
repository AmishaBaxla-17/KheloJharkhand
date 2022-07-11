import mysql.connector
from flask import session
class team_op:
    def connection(self):
        db=mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="khelo_jharkhand")
        return db

    def team_insert(self,email,password,name,mobile,location,city,photo):
        
        con=self.connection()
        sq="insert into team(email,password,name,mobile,location,city,photo) values(%s,%s,%s,%s,%s,%s,%s)"

        record=[email,password,name,mobile,location,city,photo]
          
        mycursor=con.cursor()  
        mycursor.execute(sq, record)
        con.commit()
        mycursor.close()
        con.close()
        return
    def team_login_verify(self, email, password):
        con = self.connection()
        query = "select name,email from team  where email=%s and password=%s"
        record = [email, password]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall()
        rc = cursor.rowcount
        if rc == 0:
           return 0
        else:
           session['team_email'] = email
           for r in row:
               session['team_name']=r[0]
           return 1

    def team_profile(self):
        con = self.connection()
        query = "select photo,name,email,mobile,location,city from team where email=%s"
        record =[session['team_email']]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall()
        cursor.close()
        con.close
        return row
    def team_change_password(self, password):
        con = self.connection()
        query = "update team set password=%s where email=%s"
        record = [password,session['team_email']]
        cursor = con.cursor()
        cursor.execute(query,record)
        con.commit()
        cursor.close()
        con.close()
        return 

    def team_profile_delete(self):
        con = self.connection()
        query = "delete from team where email=%s"
        record = [session['team_email']]
        cursor = con.cursor()
        cursor.execute(query,record)
        con.commit()
        cursor.close()
        con.close
        return 
    #player
    def team_player_insert(self,name,mobile,dob,uid,address,photo_name):
        
        con=self.connection()
        sq="insert into player(team_email,name,mobile,dob,uid,address,photo) values(%s,%s,%s,%s,%s,%s,%s)"

        record=[session['team_email'],name,mobile,dob,uid,address,photo_name]
          
        mycursor=con.cursor()  
        mycursor.execute(sq,record)
        con.commit()
        mycursor.close()
        con.close()
        return
    def team_player_list(self):
        
        con=self.connection()
        query="select player_id,name,mobile,dob,uid,address,photo from player where team_email=%s"

        record=[session['team_email']]
          
        cursor=con.cursor()  
        cursor.execute(query,record)
        row=cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return row 
    def player_delete(self,player_id):
        
        con=self.connection()
        query="delete from player where player_id=%s"

        record=[player_id]
        mycursor=con.cursor()  
        mycursor.execute(query,record)
         
        con.commit()
        mycursor.close()
        con.close()
        return 
    
    def team_game(self,type):
        
        con=self.connection()
        query="select photo,name,type,charge,date,location,game_id,organizer_email from game where type=%s"
        record=[type]
        cursor=con.cursor()  
        cursor.execute(query,record)
        row=cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return row 
          

    def team_request(self,game_id,organizer):
        
        con=self.connection()
        sq="insert into request(team_email,game_id,organizer_email) values(%s,%s,%s)"
        record=[session['team_email'],game_id,organizer]
        mycursor=con.cursor()  
        mycursor.execute(sq,record)
        
        con.commit()
        mycursor.close()  
        con.close()
        return      
    

    def team_applied_list(self):
        con = self.connection()
        query = "select request_id,r.organizer_email,name,type,date,location,charge,photo from request r,game g where r.game_id=g.game_id and team_email=%s"
        record = [session['team_email']]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall()
        cursor.close()
        con.close()
        return row 

    def upcoming_events(self,type):
        
       con=self.connection()
       query="select photo,name,type,charge,date,location,game_id,organizer_email from game where type=%s"
       record=[type]
       cursor=con.cursor()  
       cursor.execute(query,record)
       row=cursor.fetchall()
       con.commit()
       cursor.close()
       con.close()
       return row 
    
    