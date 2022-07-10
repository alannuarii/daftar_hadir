from app import db
import datetime

class Absen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    instansi = db.Column(db.String(80), nullable=False)
    jabatan = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hp = db.Column(db.String(20), nullable=False)
    ttd = db.Column(db.String(50), nullable=False)
    qrcode = db.Column(db.String(50), nullable=False)
    checkin = db.Column(db.String(30), default=datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S'))
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __repr__(self):
        return '<{}. {}>'.format(self.id, self.nama)