from flask import Flask, render_template, json, request, redirect, url_for, flash,session
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'calpers_users'

mysql = MySQL(app)

Bootstrap(app)



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        return render_template('index.html',message="User created successfully")
    return render_template('index.html')

@app.route('/showlogin')
def showlogin():
    return render_template('login.html')


@app.route('/login',methods=['GET','POST'])
def login():
    print('0000000111111222222')
    try:
        msg =''

        cursor2= mysql.connection.cursor()
        print('0000000111111')
        username = request.form['inputUsername1']
        password = request.form['inputPassword1']
        if username and password:
        #if  'inputUsername1' in request.form and 'inputPassword1' in request.form:
            print('0000000')
            print('111111')
            #username = request.form['inputUsername1']
            #password = request.form['inputPassword1']

            cursor2.execute("select * from user_details where user_details.Username=%s and user_details.Pwd=%s",[username,password])
            print('22222')
            userexists = cursor2.fetchone()
            if userexists:
            #session['loggedin']= True
            #session['username']=user_details['username']
                msg='Incorrect username/password!'
                return render_template('login.html',msg=msg)

            #return 'Logged in successfully'
            else:
                print('Logged in successfully')
                return render_template('login.html',msg=msg)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    #elif request.method=='POST':
        # Form is empty... (no POST data)
    #    msg = 'Please fill out the form!'


    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor2.close();

@app.route('/showsignup')
def showsignup():
    dropdown=['Where was your mother born','What was your first car','What was the first name of your first pet?','What was your school\'s name?','Where were you born?']
    return render_template('signup.html',dropdown1=dropdown,dropdown2=dropdown)



@app.route('/signup', methods=['GET','POST'])
def signup():
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
                cursor1.execute("insert into user_details(Username,Pwd,Email_id,Preferred_name,SecQue1,Ans1,SecQue2,Ans2) values (%s,%s,%s,%s,%s,%s,%s,%s)",[_username,_pwd,_email,_prename,_que1,_ans1,_que2,_ans2])
                mysql.connection.commit()
                flash("Account created")
                print('This is standard output222223333344444')
                return redirect(url_for('index'))

            else:
                flash("Username Exists.Refill the form")
                print("Username Exists")
                return redirect(url_for('showsignup'))
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
