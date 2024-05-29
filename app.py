from flask import Flask, render_template, request, flash, redirect, url_for, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re
from functools import wraps
import os


app = Flask(__name__, static_folder='assets')
app.secret_key = 'your_secret_key'

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'rootpassword')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'mydb')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



@app.route("/")

def home():

    return render_template('index.html')

@app.route("/about",methods=['GET', 'POST'])

def about():
    return render_template('about.html')

@app.route("/contact",methods=['GET', 'POST'])

def contact():
    return render_template('contact.html')

@app.route("/houses", methods=['GET', 'POST'])

def houses():
    return render_template('houses.html')

@app.route("/marrakech_details1", methods=['GET', 'POST'])


def marrakech_details1():
    return render_template('marrakech_details1.html')

@app.route("/marrakech_details2", methods=['GET', 'POST'])


def marrakech_details2():
    return render_template('marrakech_details2.html')

@app.route("/marrakech_details3", methods=['GET', 'POST'])


def marrakech_details3():
    return render_template('marrakech_details3.html')

@app.route("/agadir_details1", methods=['GET', 'POST'])


def agadir_details1():
    return render_template('agadir_details1.html')

@app.route("/agadir_details2", methods=['GET', 'POST'])


def agadir_details2():
    return render_template('agadir_details2.html')
@app.route("/agadir_details3", methods=['GET', 'POST'])


def agadir_details3():
    return render_template('agadir_details3.html')
  

@app.route("/reservation", methods=['POST'])


def reservation():
    if 'email' not in session:
        flash('Vous devez être connecté pour faire une réservation.', 'error')
        return redirect(url_for('login'))  # Redirigez vers la page de connexion

    email = session['email']

    # Vérifiez que les autres champs sont présents
    nom_maison = request.form.get('nomdemaison')
    date = request.form.get('date')
    nombre_personnes = request.form.get('nombrePersonnes')
    nombre_nuits = request.form.get('nombreNuits')

    if not nom_maison or not date or not nombre_personnes or not nombre_nuits:
        flash('Tous les champs sont requis.', 'error')
        return redirect(url_for('reservation_form_page'))  # 'reservation_form_page' est le nom de la route de votre formulaire de réservation

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE email = %s', (email,))
    user = cur.fetchone()
    if not user:
        flash('Utilisateur non trouvé.', 'error')
        return redirect(url_for('reservation_form_page'))

    # Vérifiez si la maison est déjà réservée à la même date
    cur.execute('SELECT * FROM reservation WHERE nom_maison = %s AND date = %s', (nom_maison, date))
    existing_reservation = cur.fetchone()
    if existing_reservation:
        flash('Cette maison est déjà réservée pour cette date.', 'error')
        return 'Cette maison est réservée pour cette date.'

    # Insérer la réservation si elle n'existe pas déjà
    cur.execute("INSERT INTO reservation (email, nom_maison, date, nombre_personnes, nombre_nuits) VALUES (%s, %s, %s, %s, %s)", 
                (email, nom_maison, date, nombre_personnes, nombre_nuits))
    mysql.connection.commit()
    cur.close()
    flash('Reservation successful!', 'success')
    return  'Réservation enregistrée avec succès !'


@app.route("/login", methods=['GET', 'POST'])


def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('profile.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

    


@app.route("/signup", methods=['GET', 'POST'])

def signup():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (name, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('signup.html', mesage = mesage)

   

@app.route("/profile", methods=['GET', 'POST'])

def profile():
    if request.method == 'POST':
        if 'loggedin' in session:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            nom_maison = request.form.get('nomdemaison')            
            nombre_nuits = request.form.get('nombreNuits')

            user = {'username': username, 'email': email, 'password': password}
            reservations={'nom_maison': nom_maison, 'number':nombre_nuits}
            return render_template('profile.html', user=user, reservations=reservations)
        
    else:
        return redirect(url_for('login'))
@app.route('/logout')

def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)