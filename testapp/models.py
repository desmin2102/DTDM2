from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    quota = db.Column(db.Integer, default=1024)  # Quota mặc định là 1GB (1024MB)
    is_premium = db.Column(db.Boolean, default=False)  # Tình trạng Premium (miễn phí hoặc trả phí)

    # Quan hệ với bảng Billing (Một user có thể có nhiều billing record)
    billing_records = db.relationship('Billing', backref='owner', lazy=True)

    # Quan hệ với bảng File
    files = db.relationship('File', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(50), nullable=False)
    plan = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Billing {self.amount_paid} for {self.owner.username}>'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<File {self.filename} uploaded by {self.owner.username}>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
