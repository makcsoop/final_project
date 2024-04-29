import datetime

import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, login_user
from data import db_session
from flask_wtf import FlaskForm
from data.db_session import global_init, SqlAlchemyBase
from data.users import User, Products
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired
import urllib
import random
import sqlite3
import smtplib
from email.mime.text import MIMEText
import json

app = Flask(__name__)
frame_r = 0
login = ''
password = ''
role = ''
all_info = {}
current_menu_static = {}
current_menu = list()
user_info = []
submit_info = []
current_info_menu = []
all_info_ticket = None
all_prodict = []
all_new_prodict = []

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отечество')
    login = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    rules = BooleanField('Соглашение пользователя')
    submit = SubmitField('Зарегистрироваться')


class Feedback(FlaskForm):
    all_info = StringField('ФИО', validators=[DataRequired()])
    subject = StringField('Тема сообщения', validators=[DataRequired()])
    notes = TextAreaField('Текст сообщения', validators=[DataRequired()])
    file = FileField('Файл')
    submit = SubmitField('Отправить')


class AddProduct(FlaskForm):
    model = StringField('Модель обуви', validators=[DataRequired()])
    type_shoes = StringField('Вид обуви', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    quantity = StringField('Количество', validators=[DataRequired()])
    image = FileField('Фото обуви', validators=[DataRequired()])
    submit = SubmitField('Добавить')


def send_email(message, getters):
    sender = "maroz15official@gmail.com"
    getter = 'znv10324@omeie.com'
    password = "apirvlcgklmdkmkh"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Ваша регистрация"
        server.sendmail(sender, getters, msg.as_string())

        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def get_level_user(login):
    connect = sqlite3.connect('db/user.db')
    cursor = connect.cursor()
    id_user = cursor.execute(f"""SELECT * FROM users WHERE login = '{login}'""").fetchall()
    return id_user[0][6]


def get_all_product():
    global all_prodict
    connect = sqlite3.connect('db/user.db')
    cursor = connect.cursor()
    all_info = cursor.execute(f"""SELECT * FROM products""").fetchall()
    final = []
    for i in all_info:
        final.append(list(i))
    all_prodict = final


def get_new_product():
    global all_new_prodict
    connect = sqlite3.connect('db/user.db')
    cursor = connect.cursor()
    all_info = cursor.execute(f"""SELECT * FROM products ORDER BY data""").fetchall()
    final = []
    for i in all_info:
        final.append(list(i))
    all_new_prodict = final[:4]


get_all_product()
get_new_product()


def generator_log():
    alp = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    random.shuffle(alp)
    vowels = set('bcdfghjklmnpqrstvwxz')
    flag = True
    while flag:
        for i in range(4):
            if alp[i] in vowels and set(alp[i:i + 2]) <= vowels:
                random.shuffle(alp)
                flag = True
                break
            else:
                flag = False
    return ''.join(alp[:6])


# @app.route('/')
# def index():
#     return render_template('index.html', obj=all_info)
db_session.global_init('db/user.db')
db_sess = db_session.create_session()


@app.route('/')
def index():
    global all_prodict, all_new_prodict
    get_all_product()
    get_new_product()
    level = session.get('role', '')
    return render_template('home.html', current_menu=all_new_prodict, all_info=all_prodict,
                           login=session.get('login', ''), level=level)


@app.route('/login', methods=["GET", "POST"])
def login_form():
    session['login'] = ''
    session['role'] = 0
    form = LoginForm()
    if form.validate_on_submit():
        login_cur = db_sess.query(User).filter(User.login == str(form.login.data)).first()
        if not login_cur:
            return render_template('login_user.html', title='Авторизация',
                                   form=form,
                                   message="Такого пользователя не существует")
        elif login_cur.password != form.password.data:
            return render_template('login_user.html', title='Авторизация',
                                   form=form,
                                   message="Неверный пароль")
        login = form.login.data
        session['login'] = login
        session['role'] = get_level_user(login)

        return redirect('/')
    return render_template('login_user.html', title='Авторизация', form=form)


@app.route('/register', methods=["GET", "POST"])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        login_cur = db_sess.query(User).filter(User.login == form.login.data).first()
        if login_cur:
            return render_template('register_new.html', title='Авторизация',
                                   form=form,
                                   message="Такой пользователь уже существует")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.patronymic = form.patronymic.data
        user.login = form.login.data
        user.email = form.email.data
        user.password = form.password.data
        user.level = 1
        db_sess.add(user)
        db_sess.commit()

        return redirect('/')
    return render_template('register_new.html', title='Авторизация', form=form)


@app.route('/user/basket')
def basket():
    return render_template('basket.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form = Feedback()
    if request.method == 'POST':
        return redirect('/')
    return render_template('feedback.html', form=form, login=session.get('login', ''))


@app.route('/about')
def about():
    return render_template('about.html', login=session.get('login', ''))


@app.route('/admin')
def admin():
    login = session.get('login', '')
    level = session.get('role', '')
    return render_template('admin.html', login=login, level=level)


@app.route('/add', methods=['POST', 'GET'])
def add():
    login = session.get('login', '')
    level = session.get('role', '')
    form = AddProduct()
    if request.method == 'POST':
        request.files['image'].save(
            f'/Users/macbook/Desktop/итоговый проект/static/images/{request.files['image'].filename}')
        db_sess = db_session.create_session()
        product = Products()
        product.images = f'static/images/{request.files['image'].filename}'
        product.name = form.model.data
        product.prise = form.price.data
        product.quality = form.quantity.data
        product.notes = form.type_shoes.data
        product.data = datetime.datetime.now().date()
        db_sess.add(product)
        db_sess.commit()
        return redirect('/admin')
    return render_template('add.html', login=login, level=level, form=form)


if __name__ == '__main__':
    app.debug = True
    db_session.global_init("db/user.db")
    app.run(host="localhost", port=5050)
