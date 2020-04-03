from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city
from webapp.python_org_news import get_python_news


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.all()
        return render_template('index.html', page_title=page_title, weather=weather, news_list=news_list)


    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            flash('Пользователь уже авторизован')
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Успешный вход')
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Выход')
        return redirect(url_for('index'))

    @app.route('/admin/')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return "привет админ"
        else:
            return 'ты не админ'

    return app
