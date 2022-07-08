from app import app
from app import db
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models.user import User
from app.models.agenda import Agenda


@app.route('/login', methods=['GET','POST'])
def login():
    tahun = datetime.now().strftime('%Y')

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Anda memasukkan email yang salah')
            return redirect(url_for('login'))
        if not user.checkPassword(password):
            flash('Anda memasukkan password yang salah')
            return redirect(url_for('login'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('pages/login.html', title='Login | RedPanda', tahun=tahun)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET','POST'])
@login_required
def index():
    # name = 'Alan Nuari'
    # email = 'email@alan.web.id'
    # password = 'admin123'
    # level = 1
    # admin = User(name=name, email=email, level=level)
    # admin.setPassword(password)
    # db.session.add(admin)
    # db.session.commit()

    today = datetime.now().strftime('%Y-%m-%d')
    rapat_today = Agenda.query.filter_by(tanggal=today).all()

    if request.method == 'POST':
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        tempat = request.form['tempat']
        agenda = request.form['agenda']
        rapat = Agenda(tanggal=tanggal, waktu=waktu, tempat=tempat, agenda=agenda)
        db.session.add(rapat)
        db.session.commit()
    return render_template('pages/home.html', title='Home | RedPanda', today=rapat_today)


@app.route('/input-absen', methods=['GET','POST'])
@login_required
def input_absen():
    if request.method == 'POST':
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        tempat = request.form['tempat']
        agenda = request.form['agenda']
        rapat = Agenda(tanggal=tanggal, waktu=waktu, tempat=tempat, agenda=agenda)
        db.session.add(rapat)
        db.session.commit()
    return render_template('pages/input-absen.html', title='Home | RedPanda')


