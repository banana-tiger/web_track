#from getpass import win_getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User


app = create_app()

with app.app_context():

    username = input('Введите имя: ')

    if User.query.filter(User.username == username).count():
        print('Пользователь с таким именем уже существует')
        sys.exit()
# пока ввод пароля реализован без getpassa из-за Warninga
    password1 = input('Введите пароль: ')
    password2 = input('Подтвердите пароль: ')

    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit()

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id {}'.format(new_user.id))

