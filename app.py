from flask import Flask, render_template, redirect, url_for, session, request, flash, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import requests
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'onlineprogrammingtutorials'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = 'a20df34009d3fa798812dd526c88b215689850e6'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users order by score desc LIMIT 10")
    topper = cur.fetchall()
    if result > 0 :
        return render_template('dashboard.html', toppers = topper)
    cur.close()


@app.route('/pythonassessment')
def pythonassessment():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM clanguageproblemstatements")
    problemstatement = cur.fetchall()
    if result > 0 :
        return render_template('pythonassessment.html', problemstatements = problemstatement)
    cur.close()

@app.route('/solvePythonproblem/<string:id>/', methods = ['GET', 'POST'])
def solvePythonproblem(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM clanguageproblemstatements WHERE id = %s", [id])
    problem = cur.fetchone()
    if request.method == 'POST' :
        #code_input = problem['input1']
        expected_output = problem['output1']+'\n'
        #expected_output = "Hello World"
        source = request.form['code']
        print(source)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        data = '{"clientId": "e3c6c549a53c4a22a12c6762cc00b37e","clientSecret":"f377260c438275c396a88f8c55973351c90766eb89b7f6c2878e06972d382f18","script":"'+source+'","language":"python3","versionIndex":"0"}'
        response = requests.post('https://api.jdoodle.com/v1/execute', headers=headers, data=data)
        r = response.json()
        score = 0
        print(r)
        flash('Expected output: '+expected_output)
        #if (r['compile_status'] == 'OK'):
        flash(json.dumps('Output : '+r['output']))
        if (expected_output == r['output']):
            score = problem['score']
            flash('Congratulations!Your code passed', 'success')
        else :
            flash('Your code is not passed', 'failure')
        #else :
        #    flash('Error : '+r['compile_status'])
        flash('Score :'+str(score))
        #cur = mysql.connection.cursor()
        #result = cur.execute("SELECT score FROM users WHERE username = %s", [session.username])
        #if (result > 0):
        #    scores = cur.fetchone()
        #    totalscore = scores['score']
        #    print(totalscore)
            #totalscore = totalscore + score
            #cur.execute("UPDATE users set score =%s WHERE username = %s", [totalscore],[session['username']])
            #mysql.connection.commit()
        cur.close()
    return render_template('solvePythonproblem.html', problem = problem)

@app.route('/cLanguageAssessment')
def cLanguageAssessment():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM clanguageproblemstatements")
    problemstatement = cur.fetchall()
    if result > 0 :
        return render_template('cLanguageAssessment.html', problemstatements = problemstatement)
    cur.close()

@app.route('/solveCproblem/<string:id>/', methods = ['GET', 'POST'])
def solveCproblem(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM clanguageproblemstatements WHERE id = %s", [id])
    problem = cur.fetchone()
    if request.method == 'POST' :
        #code_input = problem['input1']
        expected_output = problem['output1']+"\n"
        #expected_output = "Hello World"
        source = request.form['code']
        print(source)
        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': source,
            'lang': 'C',
            #'input': code_input,
            'time_limit': 5,
            'memory_limit': 262144,
        }
        score = '0'
        r = requests.post(RUN_URL, data=data).json()
        print(r)
        flash('Expected output: '+expected_output)
        if (r['compile_status'] == 'OK'):
            flash(json.dumps('Output : '+r['run_status']['output']))
            if (expected_output == r['run_status']['output']) :

                score = problem['score']
                flash('Congratulations!Your code passed', 'success')
            else :
                flash('Your code is not passed', 'failure')
        else :
            flash('Error : '+r['compile_status'])
            return redirect(r['web_link'])
        flash('Score :'+score)

    return render_template('solveCproblem.html', problem = problem)

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/c')
def c():
    return render_template('c/c.html')


@app.route('/python')
def python():
    return render_template('python/python.html')


@app.route('/silent')
def silent():
    return render_template('python/silent.html')

@app.route('/domain')
def domain():
    return render_template('python/domain.html')


@app.route('/syntax')
def syntax():
    return render_template('python/syntax.html')


@app.route('/variables')
def variables():
    return render_template('python/variables.html')


@app.route('/dataTypes')
def dataTypes():
    return render_template('python/dataTypes.html')


@app.route('/typeConversion')
def typeConversion():
    return render_template('python/typeConversion.html')


@app.route('/input')
def input():
    return render_template('python/input.html')

@app.route('/operators')
def operators():
    return render_template('python/operators.html')

@app.route('/nameSpace')
def nameSpace():
    return render_template('python/nameSpace.html')

@app.route('/ifelse')
def ifelse():
    return render_template('python/ifelse.html')

@app.route('/forLoop')
def forLoop():
    return render_template('python/forLoop.html')

@app.route('/while1')
def while1():
    return render_template('python/while1.html')

@app.route('/breakContinue')
def breakContinue():
    return render_template('python/breakContinue.html')

@app.route('/pass1')
def pass1():
    return render_template('python/pass1.html')


@app.route('/function')
def function():
    return render_template('python/function.html')


@app.route('/argument')
def argument():
    return render_template('python/argument.html')

@app.route('/recursion')
def recursion():
    return render_template('python/recursion.html')

@app.route('/anonymous')
def anonymous():
    return render_template('python/anonymous.html')

@app.route('/globalLocal')
def globalLocal():
    return render_template('python/globalLocal.html')

@app.route('/global1')
def global1():
    return render_template('python/global1.html')

@app.route('/modules')
def modules():
    return render_template('python/modules.html')

@app.route('/package')
def package():
    return render_template('python/package.html')

@app.route('/number')
def number():
    return render_template('python/number.html')

@app.route('/list')
def list():
    return render_template('python/list.html')

@app.route('/tuple')
def tuple():
    return render_template('python/tuple.html')

@app.route('/string')
def string():
    return render_template('python/string.html')

@app.route('/set')
def set():
    return render_template('python/set.html')

@app.route('/dictionary')
def dictionary():
    return render_template('python/dictionary.html')

@app.route('/nested')
def nested():
    return render_template('python/nested.html')

@app.route('/arrays')
def arrays():
    return render_template('python/arrays.html')

@app.route('/matrix')
def matrix():
    return render_template('python/matrix.html')

@app.route('/listCompre')
def listCompre():
    return render_template('python/listCompre.html')

@app.route('/fileOperation')
def fileOperation():
    return render_template('python/fileOperation.html')

@app.route('/directory')
def directory():
    return render_template('python/directory.html')

@app.route('/exception')
def exception():
    return render_template('python/exception.html')

@app.route('/exceptionHand')
def exceptionHand():
    return render_template('python/exceptionHand.html')

@app.route('/userDefined')
def userDefined():
    return render_template('python/userDefined.html')

@app.route('/oop')
def oop():
    return render_template('python/oop.html')

@app.route('/class1')
def class1():
    return render_template('python/class1.html')

@app.route('/inheritance')
def inheritance():
    return render_template('python/inheritance.html')

@app.route('/multipleInterit')
def multipleInterit():
    return render_template('python/multipleInterit.html')
@app.route('/overloading')
def overloading():
    return render_template('python/overloading.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max = 50)])
    username = StringField('Username', [validators.Length(min = 4, max = 25)])
    email = StringField('Email', [validators.Length(min = 6, max = 50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()
        cur.close()
        flash('You are now logged in', 'success')
        #return redirect(url_for('homepage'))
        session['logged_in'] = True
        session['username'] = username
        session['name'] = name
        return render_template('/homepage.html')
    return render_template('/register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST" :
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0 :
            data = cur.fetchone()
            password = data['password']
            name = data['name']
            if sha256_crypt.verify(password_candidate, password) :
                print("Password matched")
                session['logged_in'] = True
                session['username'] = username
                session['name'] = name
                flash('You are now logged in', 'success')
                #return redirect(url_for('homepage'))
                return render_template('/homepage.html')
            else :
                print("Not matched")
                error = 'Invalid Log in'
                return render_template('login.html', error=error)
            cur.close()
        else :
            error = 'User name not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/successfulregistration')
def successfulregistration():
    render_template('successfulregistration.html')
@app.route('/logout')
def logout():
    session.clear()
    return render_template('/home.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)
