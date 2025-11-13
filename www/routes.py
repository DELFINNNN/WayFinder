# www/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, make_response
from urllib.parse import unquote
import functools
import bcrypt
from .dbservice import (
    get_all_contacts,
    create_contact,
    create_booking,
    get_all_bookings,
    register_user,
    login_user,
    User
)

main = Blueprint('main', __name__)

# Декоратор авторизации
def login_required(route_func):
    @functools.wraps(route_func)
    def decorated_route(*args, **kwargs):
        if not session.get('user') or request.cookies.get('AuthToken') != session.get('user'):
            return redirect(url_for('main.login'))
        return route_func(*args, **kwargs)
    return decorated_route

# Главная страница
@main.route('/')
def index():
    return render_template('index.html', title="WayFinder")

# Страница направлений
@main.route('/destinations')
@login_required
def destinations():
    tours = [
        {"name": "Milford Sound: Nature's Masterpiece", "price": "$480", "image": "tour1.jpg"},
        {"name": "Doubtful Sound: The Sound of Silence", "price": "$525", "image": "tour2.jpg"},
        {"name": "Stellisee: Mirror of the Matterhorn", "price": "$400", "image": "tour3.jpg"},
        {"name": "Experience The Great Holiday On Beach", "price": "$350", "image": "tour8.jpg"},
        {"name": "Desert Highway Adventure", "price": "$350", "image": "tour7.jpg"},
        {"name": "Classic Venetian Gondola Ride", "price": "$350", "image": "tour11.jpg"}
    ]
    return render_template('dests.html', title="Destinations", tours=tours)

# Страница бронирования
@main.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        data = request.get_json()
        user_id = session.get('userId')
        result, status_code = create_booking(data, user_id)
        return jsonify(result), status_code

    tour_name = unquote(request.args.get('tour', 'Unknown Tour'))
    tour_price = request.args.get('price', '$0')
    return render_template('booking.html', title="Booking", tour_name=tour_name, tour_price=tour_price)

# Защищенная страница контактов
@main.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('firstname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        user_id = session.get('userId')
        result, status_code = create_contact({'firstname': name, 'phone': phone, 'email': email}, user_id)
        return jsonify(result), status_code

    return render_template('contacts.html', title="Contact Us")

# Регистрация пользователя
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result, status_code = register_user(request.form)
        if status_code == 201:
            return redirect(url_for('main.login'))
        else:
            return jsonify(result), status_code
    return render_template('register.html', title='Register')

# Авторизация пользователя
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response, status_code = login_user(request.form)
        if status_code == 200:
            return response
        else:
            return render_template('login.html', title='Login', error='Неверный логин или пароль')
    return render_template('login.html', title='Login')

@main.route('/api/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        result = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Выход из аккаунта
@main.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('userId', None)
    response = redirect(url_for('main.index'))
    response.set_cookie('AuthToken', '', expires=0)
    return response

# Защищённый маршрут
@main.route('/protected')
@login_required
def protected():
    return render_template('protected.html', title='Protected Area', username=session.get('user'))

# API: только для авторизованных пользователей
@main.route('/api/contacts/all', methods=['GET'])
def get_all_contact_requests():
    from www.dbservice import ContactRequest
    contacts = ContactRequest.query.all()
    result = [
        {
            'id': c.id,
            'firstname': c.firstname,
            'phone': c.phone,
            'email': c.email,
            'user_id': c.user_id
        }
        for c in contacts
    ]
    return jsonify(result), 200

@main.route('/api/contacts', methods=['POST'])
def create_new_contact():
    data = request.get_json()
    user_id = session.get('userId') or 0
    result, status_code = create_contact(data, user_id)
    return jsonify(result), status_code

@main.route('/api/contacts', methods=['GET'])
@login_required
def api_get_contacts():
    result, code = get_all_contacts()
    return jsonify(result), code

@main.route('/api/bookings', methods=['GET'])
@login_required
def api_get_bookings():
    result, code = get_all_bookings()
    return jsonify(result), code