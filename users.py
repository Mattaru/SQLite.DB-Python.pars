import uuid
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLITE_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base)
    """
    Описывает структуру таблицы user, содержащую данные пользователя
    """
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key = True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.INTEGER)

def db_connect():
    """
    Создает подключение к базе данных
    """
    engine = sa.create_engine(SQLITE_PATH)
    # Вставляем пункт на всякий случай, т.к. у нас есть готовая база с которой мы работаем, но в случае отсутствия, она будет создана
    Base.metadata.create_all()
    session = sessionmaker(engine)
    return session()

def add_user():
    """
    Запрашивает у пользователя данные для последующего внесения в базу данных
    """
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = input("Введите пол Mail/Female: ")
    email = input("Укажите адресс электронной почты: ")
    # Обратите внимание на способ ввода даты рождения
    birthdate = input("Укажите дату рождения в формате год-месяц-день (например: 1970-01-13): ")
    while not bd_parser(birthdate):
        print("Данные введены не корректно! Убедитесь,что вводите данные правильно.")
        birthdate = input("Укажите дату рождения в формате год-месяц-день (например: 1970-01-13): ")
    height = input("Укажите рост в метрах и сантиметрах через точку(например: 1.87): ")
    while not height_parser(height):
        print("Не корректный формат данных.")
        height = input("Укажите рост в метрах и сантиметрах через точку(например: 1.87): ")
    user_id = uuid.uuid4()

    user = User(
        id = user_id,
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )
def bd_parser(birthdate):
    """
    Обработчик входной даты рождения, если введенные данные не соответствуют шаблону ____-__-__ , то функция возвращает False,
    если же все в порядке True
    """
    if birthdate.count("-") == 2:
        tester = birthdate.split("-")
        for test in tester:
            if type(int(test)):
            else:
                return False
        if len(tester[0]) == 4 and len(tester[1]) == 2 and len(tester[2] == 2):
        else:
            return False
    else:
        False

def height_parser(height):
    """
    Обработчик роста, проверяет значение на соответствие нужному формату. При соответствии возвращает True, в обратном случае False
    """
    if "." in height:
        pars = height.split(".")
        if len(pars[0]) == 1 and len(pars[1]) == 2:
            if type(float(height)) == float:
            else:
                False
        else:
            False
    else:
        False

def find(user_id, session):
    """
    Запрашивает ID пользователя и выводит на экран двух отлетов: одного ближайшего по дате рождения к пользователю,
    второго ближайшего по росту к пользователю.
    """
    query = session.query(User).filter(User.id == user_id)
    usr_birthdate = query.birthdate
    usr_height = query.birthdate