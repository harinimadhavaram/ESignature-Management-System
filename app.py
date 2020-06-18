from flask import Flask, render_template, json, request, redirect, url_for, flash,session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import sys
import os
import re
#from Crypto.Cipher import AES
#import base64
from passlib.hash import sha256_crypt
#cipher = AES.new("hello",AES.MODE_ECB)
#BLOCK_SIZE = 32
#from Werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'calpers_users'
app.secret_key='hello'

mysql = MySQL(app)

Bootstrap(app)




@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        return render_template('index.html',message="User created successfully")
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/showlogin',methods=['GET','POST'])
def showlogin():

    cursor2= mysql.connection.cursor()
    try:



        print('0000000111111111')
        username = request.form['inputUsername1']
        passwordlogin = request.form['inputPassword1']
        #password1 = sha256_crypt.hash(password)

        #pwd=sha256_crypt.verify(password,password1)
        #hash=sha256_crypt.hash("keerthi")
        ##pwd2=sha256_crypt.verify("keerthi",hash)
        #print(pwd2)
        print(passwordlogin)
        if username and passwordlogin:
        #if  'inputUsername1' in request.form and 'inputPassword1' in request.form:
            print('0000000')
            print('111111')
            #username = request.form['inputUsername1']
            #password = request.form['inputPassword1']

            #cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,pwd])
            #cursor2.execute("select Pwd from user_details where user_details.Username=%s",[username])

            #cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,password])
            print('22222')
            #password1 = cursor2.fetchall()
            cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,passwordlogin])

            userdetail=cursor2.fetchall()
            print(userdetail)
            #print(password1)
            #pwd=sha256_crypt.verify(passwordlogin,password1)
            #pwd=check_password_hash(password,userexists)
            print('222223')

            #pwd=sha256_crypt.verify(request.form['inputPassword1'],userexists)
            #print(pwd)
            #password1 = cipher.decrypt(baes64.b64decode(password))
            #if pwd:
            if len(userdetail) is not 0:
                #session['loggedin']= True
                #session['username']=userdetail['Username']
                print('Logged in successfully')
                return redirect(url_for('dashboard'))

            else:
                print('Login failed')
                msg='Incorrect username/password!'
                return render_template('login.html')


        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    #elif request.method=='POST':
        # Form is empty... (no POST data)
    #    msg = 'Please fill out the form!'


    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor2.close();
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/signup')
def signup():
    dropdown=['Where was your mother born','What was your first car','What was the first name of your first pet?','What was your school\'s name?','Where were you born?']
    return render_template('signup.html',dropdown1=dropdown,dropdown2=dropdown)



@app.route('/showsignup', methods=['GET','POST'])
def showsignup():
    cursor1 = mysql.connection.cursor()
    try:
        print('This is standard output00000')
        _username = request.form['inputUsername']
        _pwd = request.form['inputPassword']
        _email = request.form['inputEmail']
        _prename = request.form['inputPreferredname']
        #_que1 = str(request.form.get('dropdown1'))
        _que1 = request.form['dropdown1']
        _ans1 = request.form['security_ans1']
        _que2 = request.form['dropdown2']
        _ans2 = request.form['security_ans2']
        #password1 = base64.b64encode(cipher.encrypt(_pwd))
        #password1 = sha256_crypt.hash(_pwd)
        #password1=generate_password_hash(_pwd)

        print('This is standard output0')
        cursor1.execute("select 1 from user_details where user_details.Username=%s",[_username])
	#cursor1.execute("select * from user_details where user_details.Username='%s'",_name)
        data=cursor1.fetchall()

        if _username and _prename and _pwd and _email and _que1 and _ans1 and _que2 and _ans2:
            #print('This is standard output1', file=sys.stdout)
            #cursor.callproc('sp_createUser',(_name, _pwd, _email,_prename, _que1, _ans1, _que2, _ans2))
            #cursor1.execute("select * from user_details where user_details.Username=%s",_name)
            #data=cursor1.fetchall(
            print('This is standard output2222')
            if len(data) is 0:

                print('This is standard output2222233333')
                #cursor1.execute("insert into user_details(Username,Pwd,Email_id,Preferred_name,SecQue1,Ans1,SecQue2,Ans2) values (%s,%s,%s,%s,%s,%s,%s,%s)",[_username,password1,_email,_prename,_que1,_ans1,_que2,_ans2])

                cursor1.execute("insert into user_details(Username,Pwd,Email_id,Preferred_name,SecQue1,Ans1,SecQue2,Ans2) values (%s,%s,%s,%s,%s,%s,%s,%s)",[_username,_pwd,_email,_prename,_que1,_ans1,_que2,_ans2])
                mysql.connection.commit()
                flash("Account created")
                print('This is standard output222223333344444')
                return redirect(url_for('login'))

            else:
                flash("Username Exists.Refill the form")
                print("Username Exists")
                return redirect(url_for('signup'))
                #conn.commit()
                #print('This is standard output2', file=sys.stdout)
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
        cursor1.close();



@app.route('/signupload')
def dashboard():
    return render_template('signature_upload.html')
@app.route('/draw_signature')
def draw_signature():
    return render_template('draw_signature.html')

if __name__ == '__main__':
    app.run(debug=True)
