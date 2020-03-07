from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from email.message import EmailMessage
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy
import smtplib
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PRAMOD_J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))


class Admins(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'email: {self.email}, password: {self.password}'


class UserNotifications(db.Model):
    serial = db.Column(db.Integer, primary_key=True)
    date_of_notification = db.Column(db.Text, nullable=False)
    time_of_notification = db.Column(db.Text, nullable=False)
    notification = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'serial: {self.serial}, time: {self.time_of_notification}, notification: {self.notification}'


class UserQueryContact(db.Model):
    serial = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    query = db.Column(db.Text, nullable=False)
    time_of_query = db.Column(db.Text, nullable=False)
    date_of_query = db.Column(db.Text, nullable=False)
    check_query = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'serial: {self.serial}, email: {self.email}, query: {self.query}'


class UserQueryWeTeach(db.Model):
    serial = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    query = db.Column(db.Text, nullable=False)
    time_of_query = db.Column(db.Text, nullable=False)
    date_of_query = db.Column(db.Text, nullable=False)
    check_query = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'serial: {self.serial}, email: {self.email}, query: {self.query}'


class DatabaseConnection:
    con = ''
    cur = ''

    def __init__(self):
        # ------------------ BLOCK-1 START ------------------
        # app.config['MYSQL_HOST'] = 'localhost'
        # app.config['MYSQL_USER'] = 'root'
        # app.config['MYSQL_PASSWORD'] = ''
        # app.config['MYSQL_DB'] = 'database_name'
        # mysql = MySQL(app)
        # self.con = mysql.connection()
        # self.cur = self.con.cursor()
        # ------------------ BLOCK-1 END --------------------

        # ------------------ BLOCK-2 START ------------------
        self.con = sqlite3.connect('test.db')
        self.cur = self.con.cursor()
        # ------------------ BLOCK-2 END --------------------

    def get_connection(self):
        return self.con, self.cur


# THIS CLASS IS USED TO SEND CONFIRMATION MAIL
class SendConfirmationMail:

    def confirmation_mail(self, email, subject, body):

        msg = EmailMessage()

        # SUBJECT OF THE MAIL
        msg['Subject'] = subject

        if "reply" in subject:
            # FROM ADDRESS
            msg['From'] = 'pragathiravikumarbr@gmail.com'

            # TO ADDRESS
            msg['To'] = email

        else:
            # FROM ADDRESS
            msg['From'] = email

            # TO ADDRESS
            msg['To'] = 'pragathiravikumarbr@gmail.com'

        # BODY OF THE MAIL
        mail_body = body
        msg.set_content(mail_body)
        print("mail will be sent to " + email + " from cookingguide.dsatm@gmail.com")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('pragathiravikumarbr@gmail.com', 'PRApra123!')
            smtp.send_message(msg)


@app.route('/')
@app.route('/home')
def home():
    notifications = []
    entries = UserNotifications.query.all()
    for entry in entries:
        item = {
            "date": entry.date_of_notification,
            "time": entry.time_of_notification,
            "notification": entry.notification
        }
        notifications.append(item)

    return render_template('home.html', notifications=notifications)


@app.route('/about-us')
def about_us():
    return render_template('aboutus.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/we-teach', methods=['POST'])
def we_teach():
    if request.method == 'POST':
        subject = "We Teach"
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['contact']
        content = request.form['content']

        NAME = "name: " + name + "\n"
        EMAIL = "email: " + email + "\n"
        CONTACT = "phone number: " + phone_number + "\n"

        body_of_mail = NAME + EMAIL + CONTACT + content

        mail = SendConfirmationMail()
        mail.confirmation_mail(email, subject, body_of_mail)

        d = datetime.now()
        user_query_we_teach = UserQueryWeTeach(name=name, email=email, phone_number=phone_number,
                                               query=content, check_query=False, date_of_query=d.date(),
                                               time_of_query=str(d.hour) + ":" + str(d.minute) + ":" + str(d.second))
        db.session.add(user_query_we_teach)
        db.session.commit()

        flash("Query submitted successfully", 'success')
        return redirect(url_for('home'))


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        subject = "Contact Us"
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['contact']
        content = request.form['content']
        
        NAME = "name: " + name + "\n"
        EMAIL = "email: " + email + "\n"
        CONTACT = "phone number: " + phone_number + "\n"

        body_of_mail = NAME + EMAIL + CONTACT + content

        mail = SendConfirmationMail()
        mail.confirmation_mail(email, subject, body_of_mail)

        d = datetime.now()
        user_query_contact = UserQueryContact(name=name, email=email, phone_number=phone_number,
                                              query=content, check_query=False, date_of_query=d.date(),
                                              time_of_query=str(d.hour) + ":" + str(d.minute) + ":" + str(d.second))
        db.session.add(user_query_contact)
        db.session.commit()

        flash("Query submitted successfully", 'success')
        return redirect(url_for('home'))


@app.route('/admin')
@app.route('/admin_contact')
def admin_contact_panel():
    if current_user.is_authenticated:
        queries = []

        database = DatabaseConnection()
        connection, cursor = database.get_connection()

        cursor.execute('SELECT * FROM user_query_contact')
        connection.commit()
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        for result in results:
            item = {
                'serial': result[0],
                'name': result[1],
                'email': result[2],
                'phone_number': result[3],
                'query': result[4],
                'time_of_query': result[5],
                'date_of_query': result[6],
                'replied': result[7]
            }
            queries.append(item)

        return render_template('admin_user_query_contact_panel.html', queries=queries)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_we_teach')
def admin_we_teach_panel():
    if current_user.is_authenticated:
        queries = []

        database = DatabaseConnection()
        connection, cursor = database.get_connection()

        cursor.execute('SELECT * FROM user_query_we_teach')
        connection.commit()
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        for result in results:
            item = {
                'serial': result[0],
                'name': result[1],
                'email': result[2],
                'phone_number': result[3],
                'query': result[4],
                'time_of_query': result[5],
                'date_of_query': result[6],
                'replied': result[7]
            }
            queries.append(item)

        return render_template('admin_user_query_we_teach_panel.html', queries=queries)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_notification_panel', methods=['POST', 'GET'])
def admin_notification_panel():
    if request.method == "POST":
        notification = request.form['notification']

        d = datetime.now()
        user_notification = UserNotifications(date_of_notification=d.date(),
                                              time_of_notification=str(d.hour) + ":" + str(d.minute) + ":" + str(d.second),
                                              notification=notification)
        db.session.add(user_notification)
        db.session.commit()

        notifications = []
        sent_notifications = UserNotifications.query.all()
        for sent_notification in sent_notifications:
            item = {
                "serial": sent_notification.serial,
                "date": sent_notification.date_of_notification,
                "time": sent_notification.time_of_notification,
                "notification": sent_notification.notification
            }
            notifications.append(item)

        return render_template("admin_notification_panel.html", notifications=notifications)
    else:
        notifications = []
        sent_notifications = UserNotifications.query.all()
        for sent_notification in sent_notifications:
            item = {
                "serial": sent_notification.serial,
                "date": sent_notification.date_of_notification,
                "time": sent_notification.time_of_notification,
                "notification": sent_notification.notification
            }
            notifications.append(item)

        return render_template("admin_notification_panel.html", notifications=notifications)


@app.route('/admin_create', methods=['POST'])
def admin_creation():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Admins.query.filter_by(email=email).first()

        if user:
            flash('Admin already exists for this email', 'warning')
            return redirect(url_for('admin_contact_panel'))

        user = Admins(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('New admin created successfully', 'success')
        return redirect(url_for('admin_contact_panel'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Admins.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                login_user(user, True)
                return redirect(url_for('admin_contact_panel'))
            else:
                flash('Invalid admin credentials', 'warning')
                return render_template('admin_login.html')
        else:
            flash('No record found, check your credentials', 'warning')
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')


@app.route('/logout')
def admin_logout():
    logout_user()
    flash('logged out successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/reply_to_query/<string:email>/<int:serial>/<string:category>', methods=['POST'])
def reply_to_query(email, serial, category):
    if request.method == 'POST':
        subject = "Your query reply from SRH Association"
        body_of_mail = request.form['reply_to_query']

        mail = SendConfirmationMail()
        mail.confirmation_mail(email, subject, body_of_mail)

        database = DatabaseConnection()
        connection, cursor = database.get_connection()

        if category == "we_teach":
            user_query_instance = " UPDATE user_query_we_teach SET check_query = ? WHERE serial = ? "
        else:
            user_query_instance = " UPDATE user_query_contact SET check_query = ? WHERE serial = ? "

        values = ('1', serial)
        cursor.execute(user_query_instance, values)
        connection.commit()
        cursor.close()
        connection.close()

        flash('Reply sent to ' + email + " successfully", 'success')
        return redirect(url_for('admin_contact_panel'))


@app.route('/delete/<int:serial>/<string:category>', methods=['GET'])
def delete(serial, category):
    database = DatabaseConnection()
    connection, cursor = database.get_connection()
    if category == "we_teach":
        user_query_instance = " DELETE FROM user_query_we_teach WHERE serial = ? "
    elif category == "contact":
        user_query_instance = " DELETE FROM user_query_contact WHERE serial = ? "
    else:
        user_query_instance = " DELETE FROM user_notifications WHERE serial = ? "

    values = (serial, )
    cursor.execute(user_query_instance, values)
    connection.commit()
    cursor.close()
    connection.close()

    flash('Deleted query: ' + str(serial) + " successfully", 'success')

    if category == "we_teach":
        return redirect(url_for('admin_we_teach_panel'))
    elif category == "contact":
        return redirect(url_for('admin_contact_panel'))
    else:
        return redirect(url_for('admin_notification_panel'))


if __name__ == "__main__":
    app.run(debug=True)
