import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import find_athlete as af

SQLITE_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user, содержащую данные пользователя
    """
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.FLOAT)

class Athelete(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные пользователя
    """
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True)
    name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.FLOAT)

def db_connect():
    """
    Создает подключение к базе данных
    """
    engine = sa.create_engine(SQLITE_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def add_user():
    """
    Запрашивает у пользователя данные для последующего внесения в базу данных
    """
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = input("Введите пол: ")
    email = input("Укажите адресс электронной почты: ")
    while not valid_email(email):
        print("Введенные данные не являются адрессом электронной почты.")
        email = input("Укажите адресс электронной почты: ")
    # Обратите внимание на способ ввода даты рождения и роста
    birthdate = input("Укажите дату рождения в формате год-месяц-день (например: 1970-01-13): ")
    while not bd_parser(birthdate):
        print("Данные введены не корректно! Убедитесь,что вводите данные правильно.")
        birthdate = input("Укажите дату рождения в формате год-месяц-день (например: 1970-01-13): ")
    height = input("Укажите рост в метрах и сантиметрах через точку(например: 1.87): ")
    while not height_parser(height):
        print("Не корректный формат данных.")
        height = input("Укажите рост в метрах и сантиметрах через точку(например: 1.87): ")

    user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height
    )
    return user

def bd_parser(birthdate):
    """
    Обработчик входной даты рождения, если введенные данные не соответствуют шаблону ____-__-__ , то функция возвращает False,
    если же все в порядке True
    """
    if birthdate.count("-") == 2:
        tester = birthdate.split("-")
        for test in tester:
            if type(int(test)):
                return True
            else:
                return False
        if len(tester[0]) == 4 and len(tester[1]) == 2 and len(tester[2] == 2) and int(tester[1]) <= 12:
            return True
        else:
            return False
    else:
        return False

def height_parser(height):
    """
    Обработчик роста, проверяет значение на соответствие нужному формату. При соответствии возвращает True, в обратном случае False
    """
    if "." in height:
        pars = height.split(".")
        if len(pars[0]) == 1 and len(pars[1]) == 2:
            if type(float(height)) == float:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def valid_email(email):
    """
    Проверяет похожа ли строка на адресс электронной почты. Если да, то возвращает True, иначе False.
    """
    sp_dot = email.split(".")
    sp_dog = email.split("@")
    if email.count("@") < 1 or email.count(".") < 1:
        return False
    if sp_dot[0].count("@") > 1:
        return False
    for ind in range(1, len(sp_dot)):
        if sp_dot[ind].count("@") != 0:
            return False
    for ind1 in range(0, -1):
        if sp_dog[ind1].count(".") != 0:
            return False
    return True

def find_user(user_name, session):
    """
    Запрашивает имя пользователя и в случае наличия этого имени в базе возвращает его id
    """
    query = session.query(User).filter(User.first_name == user_name)
    for user in query:
        return "{} {}\nid - {}\nemail - <{}>\ngender - {}\nheight - {}\nbirthdate - {}".format(user.first_name, user.last_name, user.id, user.email, user.gender, user.height, user.birthdate)

def main():
    """
    Создает метод коммуникации пользователя с базой данных
    """
    session = db_connect()
    request = input("Добро пожаловать!\n"
          "Выберите действие которое хотите совершить:\n"
          "1 - добавить нового пользователя.\n"
          "2 - найти уже существующего пользователя.\n"
          "3 - ввести id пользователя и вывести двух спорцменов с похожими параметрами даты рождения и роста.\n")
    if request == "1":
        user = add_user()
        session.add(user)
        session.commit()
        print("Пользователь успешно добавлен")
    elif request == "2":
        user_name = input("Введите имя пользователя, id которого хотите найти: ")
        user = find_user(user_name, session)
        print(user)
    elif request == "3":
        user_id = input("Введите ID пользователя для поиска схожих данных с спорцменами: ")
        coincidence, coincidence1 = af.find_by_id(user_id, session)
        print("{}\n{}".format(coincidence, coincidence1))
    else:
        print("Выбрана несуществующая команда")

if __name__ in "__main__":
    main()