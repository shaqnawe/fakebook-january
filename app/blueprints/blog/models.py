from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        from app.blueprints.authentication.models import User
        data = {
            'id': self.id,
            'body': self.body,
            'date_created': self.date_created,
            'user_id': User.query.get(self.user_id).to_dict()
        }
        return data


    def __repr__(self):
        return f'<Post: {self.body[:10]}...>'