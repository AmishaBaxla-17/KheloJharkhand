
#from ast import If

#from turtle import width
from flask import Flask,render_template,request,redirect,url_for,session,flash

from team import team_op
from organizer import organizer_op
from captcha.image import ImageCaptcha


import random

app=Flask(__name__)   #object of class Flask
app.secret_key = "khelo"

@app.route('/')       
def home():
    return render_template('index.html')
           
@app.route('/index')       
def index():
    return render_template('index.html')         
    
@app.route('/aboutus')       
def aboutus():
    return render_template('aboutus.html') 
@app.route('/upcomingevents')       
def upcomingevents():
    return render_template('upcomingevents.html') 
      

 


# team
@app.route('/team_signup')
def team_signup():
    num=random.randrange(1000,9999)
    #Create an image instance of the given size
    img=ImageCaptcha(width=280,height=90)
    #Image captcha text
    global captcha_text
    captcha_text =str(num)
    #generate the image of the given text
    data=img.generate(captcha_text)
    #write the image on the given file and save it
    img.write(captcha_text,'static/images1/CAPTCHA.png')

    return render_template('team_signup.html')

@app.route('/team_signup_insert',methods=['POST','GET'])       
def team_signup_insert():

    if request.method=='POST':
        
        if captcha_text!=request.form["captcha"]:
            ms="Invalid Captcha!!"
            return redirect(url_for('team_signup',msg=ms))
        email=request.form["email"]
        password=request.form["password"]
        name=request.form["name"]
        mobile=request.form["mobile"]
        location=request.form["location"]
        city=request.form["city"]
        
        # for photo upload
        photo=request.files["photo"]
        photo_name = photo.filename
        photo.save("static/team1/" + photo_name)

        obj=team_op()
       
        obj.team_insert(email,password,name,mobile,location,city,photo_name)
        flash("Successfully Registered!!")
        return redirect(url_for('team_signup'))

@app.route('/team_login')       
def team_login():
    return render_template('team_login.html') 

@app.route('/team_login_verify',methods=['POST','GET'])
def team_login_verify():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        obj=team_op()
        m=obj.team_login_verify(email, password)
        if m == 0:
            ms="Invalid Email or Password"
            return render_template('team_login.html', msg=ms)
        else:
           # return session['email']
           return redirect(url_for('team')) 
         #  return "login sucessful"         
@app.route('/team')       
def team():
    if 'team_email' in session:
        return render_template('team_dashboard.html')
    else:
        return redirect(url_for('team_login')) 

@app.route('/team_profile')       
def team_profile():
    if 'team_email' in session:
        obj=team_op()
        record=obj.team_profile()

        return render_template('team_profile.html',rec=record)
    else:
        return redirect(url_for('team_login')) 

@app.route('/team_password')
def team_password():
    if 'team_email' in session:
        
        return render_template('team_password.html')
    else:
        return redirect(url_for('team_login'))

@app.route('/team_change_password',methods=['POST','GET'] )
def team_change_password():
    if request.method=='POST':
        password = request.form["password"]
        obj = team_op()
        obj.team_change_password(password)
        session.clear()
     #  flash("Successfully Changed!!")
        return redirect(url_for('team_password'))
    
     #  return render_template('team_login.html')   

@app.route('/team_profile_delete')       
def team_profile_delete():
    if 'team_email' in session:
        obj=team_op()
        obj.team_profile_delete()
        session.clear()
        return redirect(url_for('home'))    
    else:
        return redirect(url_for('team_login')) 

@app.route('/team_logout')       
def team_logout():
     session.clear()
     return redirect(url_for('team_login'))


@app.route('/team_game_search')
def team_game_search():
    if 'team_email' in session:
        return render_template('team_game_search.html')
    else:
        return redirect(url_for('team_login'))
    

@app.route('/team_game',methods=['POST','GET'] )
def team_game():
    if 'team_email' in session:
        
        if request.method=='POST':
            type = request.form["type"]
        obj = team_op()
        record=obj.team_game(type)
        return render_template('team_game_search.html',rec=record)
    else:    
        return redirect(url_for('team_login'))  

@app.route('/team_player_list')       
def team_player_list():
    if 'team_email' in session:
        obj=team_op()
        record=obj.team_player_list()

        return render_template('team_player_list.html',rec=record)
    else:
        return redirect(url_for('team_login')) 

@app.route('/player_delete',methods=['POST','GET'])       
def player_delete():
    if 'team_email' in session:
        if request.method=='GET':
           player_id=request.args.get("player_id") 
           obj=team_op()
           obj.player_delete(player_id)
           flash("Successfully Deleted!!")
           return redirect(url_for('team_player_list'))
          
    else:
        return redirect(url_for('team_login'))            


@app.route('/team_request',methods=['POST','GET'])       
def team_request():
    
    if 'team_email' in session:
        if request.method=='GET':
            
            game_id=request.args.get("game_id")
            organizer=request.args.get("organizer") 
        obj=team_op()
        obj.team_request(game_id,organizer)
        flash("Your request Submitted Successfully!!!")
        return redirect(url_for('team_game_search'))
          
    else:
        return redirect(url_for('team_login')) 

@app.route('/team_applied_list')
def team_applied_list():
        if 'team_email' in session:
                obj=team_op() 
                record=obj.team_applied_list()
                return render_template('team_applied_list.html',rec=record)
        else:
                return redirect(url_for('team_login'))


#player
@app.route('/team_player')       
def team_player():
   # num=random.randrange(1000,9999)
   # Create an image instance of the given size
    #img=ImageCaptcha(width=280,height=90)
   # Image captcha text
   # global captcha_text1
   # captcha_text1=str(num)
    #generate the image of the given text
   # data=img.generate(captcha_text1)
    #write the image on the given file and save it
   # img.write(captcha_text1,'static/player1/CAPTCHA1.png')
    if 'team_email' in session:

        return render_template('team_player.html')
    else:
        return redirect(url_for('team_login'))    

@app.route('/team_player_insert',methods=['POST','GET'])       
def team_player_insert():
    if request.method=='POST':
          # if captcha_text1!=request.form["captcha"]:
           
           #  ms="Invalid Captcha!!"
            # return redirect(url_for('team_player',msg=ms))
        
        
        name=request.form["name"]
        mobile=request.form["mobile"]
        dob=request.form["dob"]
        uid=request.form["uid"]
        address=request.form["address"]
        #for photo upload
        photo=request.files["photo"]
        photo_name = photo.filename
        photo.save("static/player1/" + photo_name)

        obj=team_op()
       
        obj.team_player_insert(name,mobile,dob,uid,address,photo_name)
        flash("  Successfully Registered!!")
        return redirect(url_for('team_player'))                 

 
#organizer             

@app.route('/organizer_signup')       
def organizer_signup():
    num=random.randrange(1000,9999)
    #Create an image instance of the given size
    img=ImageCaptcha(width=280,height=90)
    #Image captcha text
    global captcha_text1
    captcha_text1 =str(num)
    #generate the image of the given text
    data=img.generate(captcha_text1)
    #write the image on the given file and save it
    img.write(captcha_text1,'static/images1/CAPTCHA1.png')
    
    return render_template('organizer_signup.html')

@app.route('/organizer_signup_insert',methods=['POST','GET'])       
def organizer_signup_insert():
    if request.method=='POST':
        if captcha_text1!=request.form["captcha"]:
            ms="Invalid Captcha!!"
            return redirect(url_for('organizer_signup',msg=ms))
        name=request.form["name"]
        mobile=request.form["mobile"]
        email=request.form["email"]
        reg_id=request.form["reg_id"]
        
        address=request.form["address"]
        password=request.form["password"]

        # for photo upload
        photo=request.files["photo"]
        photo_name = photo.filename
        photo.save("static/organizer1/" + photo_name)
        # organizer module class object
        obj=organizer_op()
       
        obj.organizer_insert(name,mobile,email,reg_id,address,password,photo_name)
        flash("Successfully Registered!!")
        return redirect(url_for('organizer_signup'))


         

@app.route('/organizer_login')       
def organizer_login():
    return render_template('organizer_login.html') 

@app.route('/organizer_login_verify',methods=['POST','GET'])
def organizer_login_verify():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        obj=organizer_op()
        m=obj.organizer_login_verify(email, password)
        if m == 0:
            ms="Invalid Email or Password"
            return render_template('organizer_login.html', msg=ms)
        else:
           # return session['email']
           return redirect(url_for('organizer')) 
         #  return "login sucessful" 
          

         
         


@app.route('/organizer')       
def organizer():
    if 'organizer_email' in session:
        return render_template('organizer_dashboard.html')
    else:
        return redirect(url_for('organizer_login')) 

@app.route('/organizer_profile')       
def organizer_profile():
    if 'organizer_email' in session:
        obj=organizer_op()
        record=obj.organizer_profile()

        return render_template('organizer_profile.html',rec=record)
    else:
        return redirect(url_for('organizer_login')) 

@app.route('/organizer_password')
def organizer_password():
    if 'organizer_email' in session:
        return render_template('organizer_password.html')
    else:
        return redirect(url_for('organizer_login'))

@app.route('/organizer_change_password',methods=['POST','GET'] )
def organizer_change_password():
    if request.method=='POST':
        password = request.form['password']
        obj = organizer_op()
        obj.organizer_change_password(password)
        session.clear()
     #  flash("Successfully Changed!!")
        return redirect(url_for('organizer_password'))
    
     #  return render_template('organizer_login.html')   

@app.route('/organizer_profile_delete')       
def organizer_profile_delete():
    if 'organizer_email' in session:
        obj=organizer_op()
        obj.organizer_profile_delete()
        session.clear()
        return redirect(url_for('home'))    
    else:
        return redirect(url_for('organizer_login')) 

@app.route('/organizer_game_list')       
def organizer_game_list():
    if 'organizer_email' in session:
        obj=organizer_op()
        record=obj.organizer_game_list()

        return render_template('organizer_game_list.html',rec=record)
    else:
        return redirect(url_for('organizer_login')) 

   
@app.route('/game_delete',methods=['POST','GET'])       
def game_delete():
    if 'organizer_email' in session:
        if request.method=='GET':
           game_id=request.args.get("game_id") 
           obj=organizer_op()
           obj.game_delete(game_id)
           flash("Successfully Deleted!!")
           return redirect(url_for('organizer_game_list'))
          
    else:
        return redirect(url_for('organizer_login')) 


@app.route('/organizer_logout')       
def organizer_logout():
     session.clear()
     return redirect(url_for('organizer_login'))

@app.route('/organizer_teamrequest_list')
def organizer_teamrequest_list():
        if 'organizer_email' in session:
                obj=organizer_op() 
                record=obj.organizer_teamrequest_list()
                return render_template('organizer_teamrequest_list.html',rec=record)
        else:
                return redirect(url_for('organizer_login'))
                  

                


#game
@app.route('/organizer_game')       
def organizer_game():
   # num=random.randrange(1000,9999)
    #Create an image instance of the given size
   # img=ImageCaptcha(width=280,height=90)
    #Image captcha text
  #  global captcha_text1
   # captcha_text1=str(num)
    #generate the image of the given text
    #data=img.generate(captcha_text)
    #write the image on the given file and save it
  #  img.write(captcha_text1,'static/images1/CAPTCHA1.png')
    if 'organizer_email' in session:

        return render_template('organizer_game.html')
    else:
        return redirect(url_for('workman_login'))    

@app.route('/organizer_game_insert',methods=['POST','GET'])       
def organizer_game_insert():
    if request.method=='POST':
      #  if captcha_text1!=request.form["captcha"]:
           # ms="Invalid Captcha!!"
           # return redirect(url_for('game_signup',msg=ms))
        
        
        name=request.form["name"]
        type=request.form["type"]
        date=request.form["date"]
        location=request.form["location"]
        charge=request.form["charge"]
        # for photo upload
        photo=request.files["photo"]
        photo_name = photo.filename
        photo.save("static/game1/" + photo_name)

        obj=organizer_op()
       
        obj.organizer_game_insert(name,type,date,location,charge,photo_name)
        flash(" Game info Successfully Registered!!")
        return redirect(url_for('organizer_game')) 
 #upcoming events
@app.route('/upcoming_events',methods=['POST','GET'])       
def upcoming_events():
    
    if request.method=='POST':
        session["name"]=request.form.get("name")
        
        type=request.form['type']
        obj=team_op()
        record=obj.upcoming_events(type)
    
        
        return render_template('upcomingevents.html',rec=record)
    

if __name__ =="__main__":
        app.run( debug=True) #to activate app server
