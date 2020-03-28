from flask import Flask, render_template
from webapp.forms import FlaskLogin
from webapp.model import db, News
from webapp.weather import weather_by_city
from webapp.python_org_news import get_python_news


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route('/')
    def index():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.all()
        return render_template('index.html', page_title=page_title, weather=weather, news_list=news_list)


    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = FlaskLogin()
        return render_template('login.html', page_title=title, form=login_form)


    return app

