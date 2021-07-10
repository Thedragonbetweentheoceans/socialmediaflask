from flask import Flask, request, render_template, Response, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import timedelta
import bcrypt
import base64
import time


from db import db_init, db
from models import Users, Profile, Post, PostUsers

app = Flask(__name__)
app.permanent_session_lifetime=timedelta(days=5)
app.secret_key = "gameover"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)






@app.route("/home", methods=['POST','GET'])
def homePage():
    
    userInSession = False
    if "usrSes" in session:

        userInSession = True
        if request.method == "POST":
            postSomething = request.form["post"]
            localtime = time.asctime( time.localtime(time.time()) )
            insertDB = Post(username = session["usrSes"],
                            post = postSomething,
                            time = localtime,
                            likes = 0,
                            dislikes = 0)
            db.session.add(insertDB)
            db.session.commit()

        userWhoLiked = session['usrSes']
        fromDB = PostUsers.query.filter_by(userId=userWhoLiked).all()

        k=0
        for k in range(len(fromDB)):
            k+=1
    

        selectPost = Post.query.all()
        i=0
        for i in range(len(selectPost)):
            i+=1


        return render_template("home.html", postOnWebsite = selectPost, i = i, userInSession = userInSession, numberOfRepetition = k, fromDB = fromDB)
    else:
        
        selectPost = Post.query.all()
        i=0
        for i in range(len(selectPost)):
            i+=1
        
        return render_template("home.html", postOnWebsite = selectPost, i = i, userInSession = userInSession)
    
        

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == "POST":

        session.permanent = True

        firstNameSignUp = request.form['first_name']
        lastNameSignUp = request.form['last_name']
        usrSignUp = request.form['signup_usr']
        passSignUp = request.form['signup_pass']
        mailSignUp = request.form['mail']
        profileImg = request.files['pic']

        usrVerif =  Users.query.filter_by(username=usrSignUp).first()
        if not usrVerif:

            session['usrSes'] = usrSignUp
            
            hashed = bcrypt.hashpw(passSignUp.encode('utf-8'), bcrypt.gensalt())

            usrDB = Users(first_name = firstNameSignUp,
                        last_name = lastNameSignUp,
                        username = usrSignUp,
                        password = hashed,
                        mail = mailSignUp)
            db.session.add(usrDB)
            db.session.commit()

            mimetype = profileImg.mimetype
            profileDB = Profile(img=profileImg.read(),
                                username=usrSignUp,
                                mimetype=mimetype,
                                description=" ")
            db.session.add(profileDB)
            db.session.commit()
        else:
            flash("This username is taken!")
    
    return render_template("signup.html")
@app.route("/changeprofilepic", methods=['POST','GET'])
def changeProfPic():
    if "usrSes" in session: 
        usrDB =  Profile.query.filter_by(username=session["usrSes"]).first()
        if request.method == "POST":
           
            changePic = request.files['changePic']
            usrDB.img=changePic.read()
            db.session.commit()
    return render_template("profilesettingPic.html", base64=base64, usrDB=usrDB)

@app.route("/changeprofiledescript", methods=['POST','GET'])
def changeProfDescript():
    if "usrSes" in session:
        usrDB =  Profile.query.filter_by(username=session["usrSes"]).first()
        if request.method == "POST":
            changeDescrip = request.form['changeDescrip']
            usrDB.description=changeDescrip
            db.session.commit()
    return render_template("profilesettingDescript.html")

@app.route("/profile", methods=['POST','GET'])
def profile():
    if "usrSes" in session:

        if request.method == "POST":
            postSomething = request.form["post"]
            localtime = time.asctime( time.localtime(time.time()) )
            insertDB = Post(username = session["usrSes"],
                            post = postSomething,
                            time = localtime,
                            likes = 0,
                            dislikes = 0)
            db.session.add(insertDB)
            db.session.commit()

        selectPost = Post.query.filter_by(username=session["usrSes"]).all()
        i=0
        for i in range(len(selectPost)):
            i+=1
        
        usrDB =  Profile.query.filter_by(username=session["usrSes"]).first()

        
        userWhoLiked = session['usrSes']
        fromDB = PostUsers.query.filter_by(userId=userWhoLiked).all()

        k=0
        for k in range(len(fromDB)):
           k+=1

        return render_template("profile.html", base64=base64, usrDB=usrDB, userName=usrDB.username, userDescription = usrDB.description, postOnWebsite = selectPost, i = i, numberOfRepetition = k, fromDB = fromDB )
    else:
        flash("Not signed in!")
        return redirect(url_for("signin"))

@app.route("/otheruserprofile", methods=["POST","GET"])
def otheruserprofile():
    if request.method == "POST":
        searchedUser = request.form["searchedUser"]

        fromDB = Profile.query.filter_by(username=searchedUser).first()

        if fromDB:
            userName = fromDB.username
            userDescription = fromDB.description
        else:
            return render_template("nouserfound.html")
        
        selectPost = Post.query.filter_by(username=searchedUser).all()
        i=0
        for i in range(len(selectPost)):
            i+=1

        userInSession=False
        if "usrSes" in session:
            userInSession=True
            userWhoLiked = session['usrSes']
            postToLike = PostUsers.query.filter_by(userId=userWhoLiked).all()

            k=0
            for k in range(len(postToLike)):
                k+=1
            
            return render_template("otheruserprofile.html", userName=userName, userDescription=userDescription, base64=base64, usrDB=fromDB, postOnWebsite = selectPost, i = i, numberOfRepetition = k, postToLike = postToLike, userInSession=userInSession)
        else:
            return render_template("otheruserprofile.html", userName=userName, userDescription=userDescription, base64=base64, usrDB=fromDB, postOnWebsite = selectPost, i = i, userInSession=userInSession)
        


@app.route("/likeanddislikesprofile", methods=["POST" , "GET"])
def likesAndDislikesprofile():
    if "usrSes" in session:
        if request.method == 'POST':
            numberOfLikes = request.form['like']
            numberOfDislikes = request.form['dislike']
            whatPost = request.form['whatPost']
            
            likeordislike = 2

            if int(numberOfLikes) == 1 and int(numberOfDislikes) == 0:
                likeordislike = 1
            elif int(numberOfLikes) == 0 and int(numberOfDislikes) == 1:
                likeordislike = 0
    
            
            
            fromDB = PostUsers.query.filter_by(postId=whatPost).all()
            k=0
            
            for i in range(len(fromDB)):
                if fromDB[i].userId == session["usrSes"]:
                   k=1

            if k == 0:
                inDB = PostUsers(
                                userId = session["usrSes"],
                                postId = whatPost,
                                likeordislike=likeordislike)
                db.session.add(inDB)
                db.session.commit()

                fromDB = Post.query.filter_by(post=whatPost).first()
                
                fromDB.likes = int(fromDB.likes) + int(numberOfLikes)
                fromDB.dislikes = int(fromDB.dislikes) + int(numberOfDislikes)
                db.session.commit()
            
            
               
        return redirect(url_for("profile"))

@app.route("/likeanddislikeshome", methods=["POST" , "GET"])
def likesAndDislikeshome():
    if "usrSes" in session:
        if request.method == 'POST':
            numberOfLikes = request.form['like']
            numberOfDislikes = request.form['dislike']
            whatPost = request.form['whatPost']

            fromDB = PostUsers.query.filter_by(postId=whatPost).all()
            k=0
            for i in range(len(fromDB)):
                if fromDB[i].userId == session["usrSes"]:
                   k=1
            if k == 0:
                inDB = PostUsers(
                                userId = session["usrSes"],
                                postId = whatPost)
                db.session.add(inDB)
                db.session.commit()

                fromDB = Post.query.filter_by(post=whatPost).first()
                fromDB.likes = int(fromDB.likes) + int(numberOfLikes)
                fromDB.dislikes = int(fromDB.dislikes) + int(numberOfDislikes)
                db.session.commit()
    
        return redirect(url_for("homePage"))

@app.route("/signin", methods = ['POST', 'GET'])
def signin():
    if "usrSes" in session:
        flash("You are logged in!")
        return render_template("signin.html")
    else:
        if request.method == "POST":

            session.permanent = True

            usrSignIn = request.form['signin_usr']
            passSignIn = request.form['signin_pass']


            usrnDB = Users.query.filter_by(username=usrSignIn).first()
            

            if usrnDB:
                if bcrypt.checkpw(passSignIn.encode('utf-8'),usrnDB.password):
                    session["usrSes"] = usrSignIn
                    flash("Now you are signed in!")
                else:
                    flash("Password incorrect!")
            else:
                flash("User not found!")

            
        return render_template("signin.html")

@app.route("/signout")
def signout():
    if "usrSes" in session:
        session.pop("usrSes", None)
        return redirect(url_for("homePage"))

if __name__== "__main__":
    app.run(debug=True)