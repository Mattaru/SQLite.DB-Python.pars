import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# !!ВАЖНО: Модуль импортирован в users.py и запускается через него же.

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

def nearest(list, value):
    """
    Находит наиближайшее значение к заданному
    """
    return min(list, key = lambda i: abs(i - value))

def find_by_id(user_id, session):
    """
    Запрашивает ID пользователя и выводит на экран двух атлетов: одного ближайшего по дате рождения к пользователю,
    второго ближайшего по росту к пользователю.
    """
    query = session.query(User).filter(User.id == user_id)
    usr_birthdate = [user.birthdate for user in query]
    usr_height = [user.height for user in query]
    if usr_height == [] or usr_birthdate == []:
        return "Пользователя с таким ID не существует.", ""
    # Составляем спискок дат рождения атлетов и список их роста
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
    query = session.query(Athelete).filter(Athelete.height == nearest(list_of_height, usr_height[0]))
    nst_height = ["Схожий атлет по росту - %s с ростом: %s." % (athelete.name, athelete.height) for athelete in query]
    # Находим ближайшее значение по дате рождения
    nst_val = nearest(list_of_birthdate, int(usr_birthdate[0].replace("-", "")))
    br_date = [str(nst_val)[0: 4], str(nst_val)[4: 6], str(nst_val)[6: 8]]
    query = session.query(Athelete).filter(Athelete.birthdate == "-".join(br_date))
    nst_birthdate = ["Схожий атлет по дате рождения - %s с датой рождения: %s." % (athelete.name, athelete.birthdate) for athelete in query]

    return nst_height[0], nst_birthdate[0]