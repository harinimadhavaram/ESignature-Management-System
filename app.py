from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupload')
def dashboard():
    return render_template('signature_upload.html')

@app.route('/draw_signature')
def draw_signature():
    return render_template('draw_signature.html')    

if __name__ == '__main__':
    app.run(debug=True)