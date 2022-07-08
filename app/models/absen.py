from app import db

class Absen(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(50), nullable=False)
    instansi = db.Column(db.String(80), nullable=False)
    jabatan = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hp = db.Column(db.String(20), nullable=False)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __repr__(self):
        return '<{}. {}>'.format(self.id, self.nama)