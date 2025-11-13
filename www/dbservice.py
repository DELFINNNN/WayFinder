# www/dbservice.py
from www import db
from sqlalchemy import text
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class ContactRequest(db.Model):
    __tablename__ = 'contactrequests'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)

    def __init__(self, firstname, phone, email, user_id):
        self.firstname = firstname
        self.phone = phone
        self.email = email
        self.user_id = user_id

class Booking(db.Model):
    __tablename__ = 'tourrequests'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    tour_name = db.Column(db.String(255), nullable=False)
    tour_price = db.Column(db.String(6), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)

    def __init__(self, firstname, lastname, email, phone, tour_name, tour_price, user_id):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.tour_name = tour_name
        self.tour_price = tour_price
        self.user_id = user_id

def register_user(form_data):
    username = form_data.get('loginField')
    password = form_data.get('passField')
    email = form_data.get('emailField')
    if not username or not password or not email:
        return {'message': 'Missing fields'}, 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        new_user = User(username=username, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def login_user(form_data):
    # Импортируем Flask-объекты здесь, чтобы избежать циклического импорта
    from flask import session, redirect, url_for
    username = form_data.get('loginField')
    password = form_data.get('passField')
    if not username or not password:
        return {'error': 'Missing credentials'}, 400
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {'error': 'Invalid credentials'}, 401
    session['user'] = user.username
    session['userId'] = user.id
    response = redirect(url_for('main.index'))
    response.set_cookie('AuthToken', user.username)
    return response, 200

def create_contact(data, user_id):
    try:
        new_contact = ContactRequest(data['firstname'], data['phone'], data['email'], user_id)
        db.session.add(new_contact)
        db.session.commit()
        return {'message': 'Contact created successfully', 'id': new_contact.id}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def create_booking(data, user_id):
    try:
        new_booking = Booking(
            data['first-name'],
            data['last-name'],
            data['email'],
            data['phone'],
            data['tour_name'],
            data['tour_price'],
            user_id
        )
        db.session.add(new_booking)
        db.session.commit()
        return {'message': 'Booking created successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

def get_all_contacts():
    from flask import session
    try:
        user_id = session.get('userId')
        contacts = ContactRequest.query.filter_by(user_id=user_id).all()
        result = {'contacts': [
            {'id': c.id, 'firstname': c.firstname, 'phone': c.phone, 'email': c.email}
            for c in contacts
        ]}
        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500

def get_all_users():
    try:
        users = User.query.all()
        return [{
            'id': u.id,
            'username': u.username,
            'email': u.email
        } for u in users], 200
    except Exception as e:
        return {'error': str(e)}, 500

def get_all_bookings():
    from flask import session
    try:
        user_id = session.get('userId')
        bookings = Booking.query.filter_by(user_id=user_id).all()
        result = {'bookings': [
            {
                'id': b.id,
                'firstname': b.firstname,
                'lastname': b.lastname,
                'email': b.email,
                'phone': b.phone,
                'tour_name': b.tour_name,
                'tour_price': b.tour_price
            }
            for b in bookings
        ]}
        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500