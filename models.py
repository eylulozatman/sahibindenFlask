from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='adverts')

    def __repr__(self):
        return f"Advert('{self.description}', '{self.price}', '{self.city}', '{self.image}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Category('{self.name}')"
