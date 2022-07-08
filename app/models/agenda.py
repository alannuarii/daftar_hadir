from app import db

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tanggal = db.Column(db.String(30), nullable=False)
    waktu = db.Column(db.String(10), nullable=False)
    tempat = db.Column(db.String(80), nullable=False)
    agenda = db.Column(db.String(150), nullable=False)
    absens = db.relationship('Absen', backref='agenda', cascade="all, delete-orphan")

    def __repr__(self):
        return '<{}. {} - {}>'.format(self.id, self.tanggal, self.agenda)