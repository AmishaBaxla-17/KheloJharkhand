import mysql.connector
from flask import session

# organizer
class organizer_op:
    def connection(self):
        db=mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="khelo_jharkhand")
        return db

    def organizer_insert(self,name,mobile,email,reg_id,address,password,photo):
        
        con=self.connection()
        sq="insert into organizer(name,mobile,email,reg_id,address,password,photo) values(%s,%s,%s,%s,%s,%s,%s)"

        record=[name,mobile,email,reg_id,address,password,photo]
          
        mycursor=con.cursor()  
        mycursor.execute(sq,record)
        con.commit()
        mycursor.close()
        con.close()
        return

    def organizer_login_verify(self, email, password):
        con = self.connection()
        query = "select name,email from organizer  where email=%s and password=%s"
        record = [email, password]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall()
        rc = cursor.rowcount
        if rc == 0:
           return 0
        else:
           session['organizer_email'] = email
           for r in row:
               session['organizer_name']=r[0]
           return 1

    def organizer_profile(self):
        con = self.connection()
        query = "select photo,name,mobile,email,reg_id,address,password from organizer where email=%s"
        record =[session['organizer_email']]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall() 
        cursor.close()
        con.close
        return row

    
    def organizer_change_password(self, password):
        con = self.connection()
        query = "update organizer set password=%s where email=%s"
        record = [password,session['organizer_email']]
        cursor = con.cursor()
        cursor.execute(query,record)
        con.commit()
        cursor.close()
        con.close()
        return 

    def organizer_profile_delete(self):
        con = self.connection()
        query = "delete from organizer where email=%s"
        record = [session['organizer_email']]
        cursor = con.cursor()
        cursor.execute(query,record)
        con.commit()
        cursor.close()
        con.close
        return 
    # game
    def organizer_game_insert(self,name,type,date,location,charge,photo_name):
        
        con=self.connection()
        sq="insert into game(organizer_email,name,type,date,location,charge,photo) values(%s,%s,%s,%s,%s,%s,%s)"

        record=[session['organizer_email'],name,type,date,location,charge,photo_name]
          
        mycursor=con.cursor()  
        mycursor.execute(sq,record)
        con.commit()
        mycursor.close()
        con.close()
        return

    def organizer_game_list(self):
        
        con=self.connection()
        query="select game_id,name,type,date,location,charge,photo from game where organizer_email=%s"

        record=[session['organizer_email']]
          
        cursor=con.cursor()  
        cursor.execute(query,record)
        row=cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return row
    def game_delete(self,game_id):
        con=self.connection()
        query="delete from game where game_id=%s"
        record=[game_id]
        mycursor=con.cursor()  
        mycursor.execute(query,record)
         
        con.commit()
        mycursor.close()
        con.close()
        return  
    def organizer_teamrequest_list(self):
        con = self.connection()
        query = "select request_id,email,name,mobile,location,city,photo from request r,team t where r.team_email=t.email and organizer_email=%s"
        record = [session['organizer_email']]
        cursor = con.cursor()
        cursor.execute(query, record)
        row = cursor.fetchall()
        cursor.close()
        con.close()
        return row  