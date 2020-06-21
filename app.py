import itsdangerous

from dominate.tags import a
from flask import Flask, render_template, json, request, redirect, url_for, flash, session, abort
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from markupsafe import escape
import smtplib
#from itsdangerous import URLSafeTimedSerialize
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "phaseteaching@gmail.com"
msg = MIMEMultipart()
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'calpers_users'
app.secret_key = 'hello'
ts = itsdangerous.URLSafeTimedSerializer(app.config["SECRET_KEY"])


mysql = MySQL(app)

Bootstrap(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return render_template('index.html', message="User created successfully")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/showlogin', methods=['GET', 'POST'])
def showlogin():
    cursor2 = mysql.connection.cursor()
    try:

        if request.method == "POST":
            session.pop('user', None)

        print('0000000111111111')
        username = request.form['inputUsername1']
        password = request.form['inputPassword1']

        if username and password:

            cursor2.execute("select Pwd from user_details where user_details.Username=%s ", [username])
            userdetail = cursor2.fetchall()
            match = sha256_crypt.verify(password, userdetail[0][0])
            if match:

                session['loggedin'] = True
                session['user'] = username
                if 'user' in session:
                    print(session['user'])

                print('Logged in successfully')
                return redirect(url_for('dashboard'))

            else:
                print('Login failed')
                flash('USERNAME OR PASSWORD IS INCORRECT')
                return render_template('login.html')


        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})


    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor2.close();


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('loggedin', None)
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    dropdown = ['Where was your mother born', 'What was your first car', 'What was the first name of your first pet?',
                'What was your school\'s name?', 'Where were you born?']
    return render_template('signup.html', dropdown1=dropdown, dropdown2=dropdown)


@app.route('/showsignup', methods=['GET', 'POST'])
def showsignup():
    cursor1 = mysql.connection.cursor()
    try:

        _username = request.form['inputUsername']
        _pwd = request.form['inputPassword']
        _email = request.form['inputEmail']
        _prename = request.form['inputPreferredname']
        _que1 = request.form['dropdown1']
        _ans1 = request.form['security_ans1']
        _que2 = request.form['dropdown2']
        _ans2 = request.form['security_ans2']
        password = sha256_crypt.hash(_pwd)

        cursor1.execute("select 1 from user_details where user_details.Username=%s", [_username])
        data = cursor1.fetchall()

        if _username and _prename and _pwd and _email and _que1 and _ans1 and _que2 and _ans2:

            if len(data) is 0:

                cursor1.execute(
                    "insert into user_details(Username,Pwd,Email_id,Preferred_name,SecQue1,Ans1,SecQue2,Ans2) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                    [_username, password, _email, _prename, _que1, _ans1, _que2, _ans2])
                mysql.connection.commit()
                flash("Account created")


                return redirect(url_for("login"))

            else:
                flash("ACCOUNT ALREADY EXISTS. TRY LOGGING IN")
                print("Username Exists")

                return redirect(url_for("signup"))

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor1.close();

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
        return render_template('passwordreset.html')
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
        #password22 = sha256_crypt.hash(pwd2)
        #cursor5.execute("select Username from user_details where user_details.Email_id = %s",email)
        #user=cursor5.fetchall();
        #print(user)
        sql="update calpers_users.user_details set Pwd = (%s) where user_details.Email_id = (%s)"
        cursor5.execute(sql,(pwd2, email))
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
    return render_template('forgotpwd.html')


@app.route('/forgotpassword',methods=["GET", "POST"])
def forgotpassword():
    cursor4 = mysql.connection.cursor()
    _email = request.form['inputEmail1']
    user = cursor4.execute("select Username from user_details where user_details.Email_id=%s ", [_email])
    if user is not 0:

        toaddr = _email
        token = ts.dumps(_email, salt='email-confirm-key')
        confirm_url = url_for('confirm_email', token=token, _external=True)

        msg['Subject'] = "Reset password link"

        body = "Hi " + str(user) + " This is link for resetting the pwd" + confirm_url

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
    return render_template('index.html', message="Not logged in")


@app.route('/draw_signature')
def draw_signature():
    if 'user' in session:
        return render_template('draw_signature.html')
    return render_template('index.html', message="Not logged in")


if __name__ == '__main__':
    app.run(debug=True)
