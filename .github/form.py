from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import datetime

app = Flask(__name__)

# Verbind met de database
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={MySQL ODBC 9.2 ANSI Driver};'
        'SERVER=mysql;'  # Gebruik de naam van de MySQL-container
        'PORT=3306;'
        'DATABASE=winkel;'
        'UID=root;'
        'PWD=Toetsenbord11!'  # Voeg hier je wachtwoord in
    )
    return conn

# Maak de benodigde tabellen aan
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Maak gebruikers tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gebruikers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            voornaam VARCHAR(100),
            achternaam VARCHAR(100),
            email VARCHAR(100),
            telefoon VARCHAR(20),
            geboortedatum DATE,
            straatnaam VARCHAR(100),
            huisnummer VARCHAR(10),
            postcode VARCHAR(20),
            datum_aangemaakt DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Maak producten tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producten (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_nummer VARCHAR(50),
            naam VARCHAR(100),
            leverancier VARCHAR(100),
            aantal_per_dos INT
        )
    ''')

    # Maak bestellingen tabel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bestellingen (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gebruiker_id INT,
            product_id INT,
            datum_bestelling DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gebruiker_id) REFERENCES gebruikers(id),
            FOREIGN KEY (product_id) REFERENCES producten(id)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

# Initializeer de database als de app start
initialize_database()

# Startpagina
@app.route('/')
def home():
    return render_template('index.html')

# Gebruiker toevoegen
@app.route('/gebruiker_toevoegen', methods=['GET', 'POST'])
def gebruiker_toevoegen():
    if request.method == 'POST':
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        email = request.form['email']
        telefoon = request.form['telefoon']
        geboortedatum = request.form['geboortedatum']
        straatnaam = request.form['straatnaam']
        huisnummer = request.form['huisnummer']
        postcode = request.form['postcode']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gebruikers 
            (voornaam, achternaam, email, telefoon, geboortedatum, straatnaam, huisnummer, postcode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (voornaam, achternaam, email, telefoon, geboortedatum, straatnaam, huisnummer, postcode))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('overzicht'))

    return render_template('gebruiker.html')

# Product toevoegen
@app.route('/product_toevoegen', methods=['GET', 'POST'])
def product_toevoegen():
    if request.method == 'POST':
        product_nummer = request.form['product_nummer']
        naam = request.form['naam']
        leverancier = request.form['leverancier']
        aantal_per_dos = request.form['aantal_per_dos']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO producten (product_nummer, naam, leverancier, aantal_per_dos)
            VALUES (?, ?, ?, ?)
        ''', (product_nummer, naam, leverancier, aantal_per_dos))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('overzicht'))

    return render_template('product.html')

# Bestelling plaatsen
@app.route('/bestelling_plaatsen', methods=['GET', 'POST'])
def bestelling_plaatsen():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        gebruiker_id = request.form['gebruiker_id']
        product_id = request.form['product_id']

        cursor.execute('''
            INSERT INTO bestellingen (gebruiker_id, product_id)
            VALUES (?, ?)
        ''', (gebruiker_id, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('overzicht'))

    cursor.execute('SELECT id, voornaam, achternaam FROM gebruikers')
    gebruikers = cursor.fetchall()

    cursor.execute('SELECT id, naam FROM producten')
    producten = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('bestelling.html', gebruikers=gebruikers, producten=producten)

# Overzicht van bestellingen
@app.route('/overzicht')
def overzicht():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT b.id, g.voornaam, g.achternaam, p.naam, b.datum_bestelling
        FROM bestellingen b
        JOIN gebruikers g ON b.gebruiker_id = g.id
        JOIN producten p ON b.product_id = p.id
        ORDER BY b.datum_bestelling DESC
    ''')
    bestellingen = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('overzicht.html', bestellingen=bestellingen)

def start_app():
    app.run(port=3000, debug=True, host="0.0.0.0")

if __name__ == "__main__":
    start_app()
else:
    start_app()
    

