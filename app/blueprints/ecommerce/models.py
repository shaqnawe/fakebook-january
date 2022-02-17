from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f'<Cart: {self.product_id} {self.user_id}>'