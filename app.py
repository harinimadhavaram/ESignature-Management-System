import itsdangerous
from dominate.tags import a
from flask import Flask, render_template, json, request, redirect, url_for, flash,session,abort
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

from markupsafe import escape
import smtplib
import sys
import os
import re
#from Crypto.Cipher import AES
#import base64
from passlib.hash import sha256_crypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
fromaddr = "phaseteaching@gmail.com"
msg = MIMEMultipart()
#cipher = AES.new("hello",AES.MODE_ECB)
#BLOCK_SIZE = 32
#from Werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'calpers_users'
app.secret_key='hello'
ts = itsdangerous.URLSafeTimedSerializer(app.config["SECRET_KEY"])
mysql = MySQL(app)

Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        return render_template('index.html',message="User created successfully")
    return render_template('index.html')

#@app.route('/login',methods=['GET','POST'])
#def login():
#    return render_template('index.html')

@app.route('/homepage')
def home():
    return render_template('home_page.html') 

@app.route('/profilepage')
def profile():
    return render_template('profile_page.html') 

@app.route('/reset-password')
def resetpassword():
    return render_template('reset_password.html')

# @app.route('/forgot-password')
# def forgot_password():
#     dropdown=['What was the first name of your first pet?','Where was your mother born','What was your first car','What was your school\'s name?','Where were you born?']
#     return render_template('forgot_password.html',dropdown=dropdown)
   

@app.route('/index',methods=['GET','POST'])
def showlogin():

    cursor2= mysql.connection.cursor()
    try:
        if request.method=="POST":
            session.pop('user',None)

        print('0000000111111111')
        username = request.form['inputUsername1']
        password= request.form['inputPassword1']

        #password1 = sha256_crypt.hash(password)

        #pwd=sha256_crypt.verify(password,password1)
        #hash=sha256_crypt.hash("keerthi")
        ##pwd2=sha256_crypt.verify("keerthi",hash)
        #print(pwd2)
        #print(passwordlogin)
        if username and password:
        #if  'inputUsername1' in request.form and 'inputPassword1' in request.form:
            #print('0000000')
            #print('111111')
            #username = request.form['inputUsername1']
            #password = request.form['inputPassword1']

            #cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,pwd])
            #cursor2.execute("select Pwd from user_details where user_details.Username=%s",[username])

            #cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,password])
            #print('22222')
            #password1 = cursor2.fetchall()
            exists=cursor2.execute("select Pwd,Email_id from user_details where user_details.Username=%s ",[username])

            userdetail=cursor2.fetchall()
            print(userdetail)
            if exists != 0:
                match=sha256_crypt.verify(password,userdetail[0][0])
                print('sha1')
            else:
                match=0
            #pwd=sha256_crypt.verify(passwordlogin,password1)
            #pwd=check_password_hash(password,userexists)
            #print('222223')

            #pwd=sha256_crypt.verify(request.form['inputPassword1'],userexists)
            #print(pwd)
            #password1 = cipher.decrypt(baes64.b64decode(password))
            #if pwd:
            if match:
                session['loggedin']= True
                session['user']=username
                session['email']=userdetail[0][1]
               
                if 'user' in session:
                    print(session['user'])

                print('Logged in successfully')
                #return render_template('signature_upload.html')
                return render_template('home_page.html')

            else:
                print('Login failed')
                flash('USERNAME OR PASSWORD INCORRECT')
                #msg='Incorrect username/password!'
                return render_template('index.html')


        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    #elif request.method=='POST':
        # Form is empty... (no POST data)
    #    msg = 'Please fill out the form!'


    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor2.close()

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('user', None)
   session.pop('loggedin', None)
  
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/signup')
def signup():
    dropdown=['What was the first name of your first pet?','Where was your mother born','What was your first car','What was your school\'s name?','Where were you born?']
    return render_template('signup.html',dropdown=dropdown)



@app.route('/showsignup', methods=['GET','POST'])
def showsignup():
    cursor1 = mysql.connection.cursor()
    try:
        print('This is standard one')
        _username = request.form['inputUsername']
        _pwd = request.form['inputPassword']
        _email = request.form['inputEmail']
       # _prename = request.form['inputPreferredname']
        #_que1 = str(request.form.get('dropdown1'))
        _que1 = request.form['dropdown']
        _ans1 = request.form['dropdown-answer']
        #_que2 = request.form['dropdown2']
        #_ans2 = request.form['security_ans2']
        #password1 = base64.b64encode(cipher.encrypt(_pwd))
        password1 = sha256_crypt.hash(_pwd)
        #password1=generate_password_hash(_pwd)

        print(' two')
        cursor1.execute("select 1 from user_details where user_details.Username=%s",[_username])
	#cursor1.execute("select * from user_details where user_details.Username='%s'",_name)
        data=cursor1.fetchall()

        if _username and _pwd and _email and _que1 and _ans1:
            print('three')
            #cursor.callproc('sp_createUser',(_name, _pwd, _email,_prename, _que1, _ans1, _que2, _ans2))
            #cursor1.execute("select * from user_details where user_details.Username=%s",_name)
            #data=cursor1.fetchall(
            print('4')
            if len(data) is 0:

                print('5')
                cursor1.execute("insert into user_details(Username,Pwd,Email_id,SecQue1,Ans1) values (%s,%s,%s,%s,%s)",[_username,password1,_email,_que1,_ans1])

                #cursor1.execute("insert into user_details(Username,Pwd,Email_id,SecQue1,Ans1) values (%s,%s,%s,%s,%s)",[_username,_pwd,_email,_que1,_ans1])
                mysql.connection.commit()
                flash("Account created")
                print('6')
                #return render_template('login.html')
                return redirect(url_for("login"))

            else:
                flash("ACCOUNT ALREADY EXISTS. TRY LOGGIN IN")
                print("Username Exists")

                return redirect(url_for("signup"))
                #conn.commit()
                print('7')
            #for result in cursor.stored_results():
            #    data = cursor.fetchall()
            #if len(data) is 0:

                #return json.dumps({'message': 'User created successfully!'})
            #else:
            #    return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor1.close()



@app.route('/confirm/<token>', methods=["GET", "POST"])
def confirm_email(token):
    cursor3 = mysql.connection.cursor()
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        print(email)
    except:
        abort(404)
    user=cursor3.execute("select * from user_details where user_details.Email_id=%s ", [email])
    if user is not 0:
        #passwordreset(email)
        #url_for('passwordreset', email=email, _external=True)
        session['sessionemail']=email
        return render_template('reset_password.html')
        #return render_template('passwordreset.html')
    else:
        abort(404)

@app.route('/passwordreset',methods=["GET", "POST"])
def passwordreset():
    print("111111")
    cursor5 = mysql.connection.cursor()
    if 'sessionemail' in session:
        email=session['sessionemail']
        pwd2 = request.form['inputPassword1']
        print(pwd2)
        password22 = sha256_crypt.hash(pwd2)
        # print("password ", password22)
        #cursor5.execute("select Username from user_details where user_details.Email_id = %s",email)
        #user=cursor5.fetchall();
        #print(user)
        sql="update calpers_users.user_details set Pwd = (%s) where user_details.Email_id = (%s)"
        cursor5.execute(sql,(password22, email))
        mysql.connection.autocommit(True)
        print("5555555")
        #cursor5.execute("select Username from user_details where Pwd=%s",[pwd2])
        user2=cursor5.fetchall()

        print(user2)
        #print("333")
        cursor5.close()
        #print(pwd)
        session.pop('sessionemail', None)
        return redirect(url_for("login"))
    else:
        abort(404)

@app.route('/forgotpwd')
def forgotpwd():
    dropdown=['What was the first name of your first pet?','Where was your mother born','What was your first car','What was your school\'s name?','Where were you born?']
    return render_template('forgot_password.html',dropdown=dropdown)
    

@app.route('/forgotpassword',methods=["GET", "POST"])
def forgotpassword():
    cursor4 = mysql.connection.cursor()
    _email = request.form['inputEmail1']
    _que1 = request.form['dropdown']
    _ans1 = request.form['dropdown1']
    if _email and _que1 and _ans1:
        cursor4.execute("select Username from user_details where user_details.Email_id=%s and user_details.SecQue1=%s and user_details.Ans1=%s", [_email,_que1,_ans1])
        user=cursor4.fetchall()
    
    
    if user is not 0:
        toaddr = _email
        token = ts.dumps(_email, salt='email-confirm-key')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        msg['Subject'] = "Reset password link"
        body = "Hi "  + user[0][0] + " This is link for resetting the pwd        " + confirm_url
        msg.attach(MIMEText(body, 'plain'))
        email = smtplib.SMTP('smtp.gmail.com', 587)
        email.starttls()
        email.login(fromaddr, "phaseteach123")
        message = msg.as_string()
        email.sendmail(fromaddr, toaddr, message)
        email.quit()
        return render_template('index.html', message="User created successfully")
    else:
        abort(404)


@app.route('/signupload')
def dashboard():
    if 'user' in session:
        return render_template('signature_upload.html')
    return render_template('index.html',message="Not Logged in")

@app.route('/draw_signature')
def draw_signature():
    if 'user' in session:
        return render_template('draw_signature.html')
    return render_template('index.html',message="Not Logged in")


if __name__ == '__main__':
    app.run(debug=True)
