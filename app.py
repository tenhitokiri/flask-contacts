from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'soporte'
app.config['MYSQL_PASSWORD'] = '4c3r04dm1n'
app.config['MYSQL_DB'] = 'contactos'
mysql = MySQL(app)

# Settings
app.secret_key = 'qwerety'

# seguir en https://youtu.be/IgCfZkR8wME?list=PLoaAvlW6Ro3OWAlD4phaa-4fzyormJVh2&t=4301


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/contacts')
def Contacts():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    contacts = cur.fetchall()
    return render_template('index.html', contacts=contacts)


@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO contactos (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto Agregado!! ')
        return redirect(url_for('Contacts'))

    else:
        return render_template('index.html')


@app.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    contact = cur.fetchall()
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute('UPDATE contactos SET fullname = %s, phone = %s, email = %s WHERE id = %s ',
                    (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto Modificado!! ')
        return redirect(url_for('Contacts'))

    else:
        return render_template('contact.html', contact=contact[0])


@app.route('/contacts/delete/<int:id>', methods=['GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado!! ')
    return redirect(url_for('Contacts'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
