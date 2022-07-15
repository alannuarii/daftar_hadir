from app import db

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tanggal = db.Column(db.String(50), nullable=False)
    tanggal_real = db.Column(db.String(50), nullable=False)
    waktu = db.Column(db.String(10), nullable=False)
    tempat = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(250), nullable=True)
    agenda = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    absens = db.relationship('Absen', backref='agenda', cascade="all, delete-orphan")

    def __repr__(self):
        return '<{}. {} - {}>'.format(self.id, self.tanggal, self.agenda)