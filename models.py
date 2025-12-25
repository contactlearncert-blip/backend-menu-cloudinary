from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('categories', lazy=True, cascade='all, delete-orphan'))

class Dish(db.Model):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_base64 = db.Column(db.Text, nullable=True)  # on le garde pour compatibilité ancienne (optionnel)
    image_url = db.Column(db.String(500), nullable=True)  # <- NOUVEAU CHAMP
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('dishes', lazy=True, cascade='all, delete-orphan'))
    restaurant = db.relationship('Restaurant', backref=db.backref('dishes', lazy=True, cascade='all, delete-orphan'))

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    table_number = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant = db.relationship('Restaurant', backref=db.backref('orders', lazy=True, cascade='all, delete-orphan'))

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    notes = db.Column(db.Text, nullable=True)
    dish = db.relationship('Dish')
    order = db.relationship('Order', backref=db.backref('items', lazy=True, cascade='all, delete-orphan'))