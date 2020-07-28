import uuid
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    gender = input("Введите пол Male/Female: ")
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
    user_id = str(uuid.uuid4())

    user = User(
        id = user_id,
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
        if len(tester[0]) == 4 and len(tester[1]) == 2 and len(tester[2] == 2):
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

def find_user(user_name, session):
    """
    Запрашивает имя пользователя и в случае наличия этого имени в базе возвращает его id
    """
    query = session.query(User).filter(User.name == user_name)
    for user in query:
        return "{} {} id - {}".format(user.first_name, user.last_name, user.id)

def nearest(list, value):
    """
    Находит наиближайшее значение к заданному
    """
    return min(list, key = lambda i: abs(i - value))

def find_by_id(user_id, session):
    """
    Запрашивает ID пользователя и выводит на экран двух отлетов: одного ближайшего по дате рождения к пользователю,
    второго ближайшего по росту к пользователю.
    """
    query = session.query(User).filter(User.id == user_id)
    for user in query:
        usr_birthdate = user.birthdate
        usr_height = user.height

    # Составляем списки дат рождения атлетов и список их роста
    query_at = session.query(Athelete).all()
    list_of_birthdate = [athelete.birthdate for athelete in query_at]
    list_of_height = [athelete.height for athelete in query_at]
    # Обработаем формат дат для удобной проверки
    for index in range(len(list_of_birthdate)):
        list_of_birthdate[index] = int(list_of_birthdate[index].replace("-", ""))
    # Избавляемся от пустых значений
    for item in range(list_of_height.count(None)):
        list_of_height.remove(None)

    # Находим значение роста ближайшее к заданному
    query = session.query(Athelete).filter(Athelete.height == nearest(list_of_height, usr_height))
    nst_height = ["%s с ростом: %s."%(athelete.name, athelete.height) for athelete in query]

    # Находим ближайшее значение по дате рождения
    nst_val = nearest(list_of_birthdate, int(usr_birthdate.replace("-", "")))
    br_date = [str(nst_val)[0: 4], str(nst_val)[4: 6], str(nst_val)[6: 8]]
    query = session.query(Athelete).filter(Athelete.height == "-".join(br_date))
    nst_birthdate = ["%s с датой рождения: %s." % (athelete.name, athelete.birthdate) for athelete in query]

    return (nst_height[0], nst_birthdate[0])

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
        coincidence, coincidence1 = find_by_id(user_id, session)
        print("Схожий атлет по росу - {}\nСхожий атлет по дате рождения - {}".format(coincidence, coincidence1))
    else:
        print("Выбрана несуществующая команда")

if __name__ in "__main__":
    main()