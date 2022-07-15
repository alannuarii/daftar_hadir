from sqlalchemy import desc
from app import app
from app import db
from flask import render_template, request, redirect, url_for, flash, make_response
from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.controller import tanggal
from app.models.user import User
from app.models.agenda import Agenda
from app.models.absen import Absen
from PIL import Image
from io import BytesIO
import base64
import os
import qrcode
import pdfkit



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

    return render_template('pages/login.html', title='Login', tahun=tahun)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET','POST'])
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
    rapat_today = Agenda.query.filter_by(tanggal_real=today).all()

    if request.method == 'POST':
        str_tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        tempat = request.form['tempat']
        link = request.form['link']
        agenda = request.form['agenda']
        user_id = request.form['user_id']
        rapat = Agenda(tanggal=tanggal(str_tanggal), tanggal_real=str_tanggal, waktu=waktu, tempat=tempat, link=link, agenda=agenda, user_id=user_id)
        db.session.add(rapat)
        db.session.commit()
        return redirect(url_for('index'))
    # for i in range(100):
    #     tanggal = '2022-07-09'
    #     waktu = '09:00'
    #     tempat = 'Aula Pertemuan'
    #     agenda = 'Rapat Pembahasan Persiapan Pekerjaan Perbaikan Cooling Tower'
    #     rapat = Agenda(tanggal=tanggal, waktu=waktu, tempat=tempat, agenda=agenda)
    #     db.session.add(rapat)
    #     db.session.commit()
    return render_template('pages/home.html', title='Home', today=rapat_today)


@app.route('/input-absen/<id>', methods=['GET','POST'])
def input_absen(id):
    rapat = Agenda.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        nama = request.form['nama']
        instansi = request.form['instansi']
        jabatan = request.form['jabatan']
        email = request.form['email']
        hp = request.form['hp']
        agenda_id = request.form['agenda_id']
        ttd = request.form['ttd']
        new_ttd = ttd.replace('data:image/png;base64,', '')
        bytes_decoded = base64.b64decode(new_ttd)
        img = Image.open(BytesIO(bytes_decoded))
        out_jpg = img.convert("RGB")

        # Random Name 
        now = datetime.now()
        microsecond = now.strftime('%f')  
        filename = nama+'-'+microsecond+'.png'
        qrcodename = 'qr'+nama+'-'+microsecond+'.png'

        # QR Code Generate 
        qr = qrcode.QRCode()
        qr.add_data('http://127.0.0.1:5000/detail-peserta/{}'.format(microsecond))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        absen = Absen(nama=nama, instansi=instansi, jabatan=jabatan, email=email, hp=hp, agenda_id=agenda_id, ttd=filename, qrcode=qrcodename, id=microsecond)
        db.session.add(absen)
        db.session.commit()
        out_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], qrcodename))
        
        return redirect(url_for('peserta_rapat', agenda_id=agenda_id, page_num=1))

    return render_template('pages/input-absen.html', title='Input Daftar Hadir', rapat=rapat)


@app.route('/daftar-hadir/<int:page_num>')
def daftar_hadir(page_num):
    rapat_all = Agenda.query.order_by(desc('tanggal')).paginate(per_page=10, page=page_num, error_out=True)

    return render_template('pages/daftar-hadir.html', title='Daftar Hadir Rapat', rapats=rapat_all)


@app.route('/peserta-rapat/<agenda_id>/<int:page_num>')
def peserta_rapat(agenda_id, page_num):
    guest = Absen.query.filter_by(agenda_id=agenda_id)
    peserta = Absen.query.filter_by(agenda_id=agenda_id).paginate(per_page=10, page=page_num, error_out=True)

    return render_template('pages/peserta-rapat.html', title='Peserta Rapat', guests=peserta, guest=guest)


@app.route('/detail-peserta/<id>')
def detail_peserta(id):
    peserta = Absen.query.filter_by(id=id).first()
    print(peserta)

    return render_template('pages/detail-peserta.html', title='Detail Peserta Rapat', guest=peserta)


@app.route('/cetak-absen/<agenda_id>')
def cetak_absen(agenda_id):
    guest = Absen.query.filter_by(agenda_id=agenda_id)

    return render_template('pages/cetak-absen.html', title='Cetak Daftar Hadir', guests=guest)


@app.route('/pengaturan/<id>/<int:page_num>')
def pengaturan(id, page_num):
    rapats = Agenda.query.filter_by(user_id=id).paginate(per_page=10, page=page_num, error_out=True)

    return render_template('pages/pengaturan.html', title='Pengaturan', rapats=rapats)


@app.route('/absen-pdf/<agenda_id>')
def konversi(agenda_id):
    res = 'http://127.0.0.1:5000/cetak-absen/{}'.format(agenda_id)
    path_wkthmltopdf = b'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    responsestring = pdfkit.from_url(res, configuration=config)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=output.pdf'
    return response