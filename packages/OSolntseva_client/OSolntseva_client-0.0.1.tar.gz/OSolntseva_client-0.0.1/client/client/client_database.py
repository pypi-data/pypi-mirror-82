import datetime
import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator

import traceback

try:
    class ClientDatabase:
        '''
        Класс - оболочка для работы с базой данных клиента.
        Использует SQLite базу данных, реализован с помощью
        SQLAlchemy ORM и используется классический подход.
        '''
        class KnownUsers:
            '''Класс - отображение для таблицы всех пользователей.'''
            def __init__(self, user):
                self.id = None
                self.username = user

        class MessageHistory:
            '''Класс - отображение таблицы истории сообщений'''

            def __init__(self, contact, direction, message):
                self.id = None
                self.contact = contact
                self.direction = direction
                self.message = message
                self.date = datetime.datetime.now()

        class Contacts:
            '''Класс - отображение списка контактов'''

            def __init__(self, contact):
                self.id = None
                self.name = contact

        def __init__(self, name):
            #движок базы данных, каждый клиент должен иметь свою бд
            path = os.getcwd()
            filename = f'client_{name}.db3'
            self.database_engine = create_engine(
                f'sqlite:///{os.path.join(path, filename)}',
                echo=False,
                pool_recycle=7200,
                connect_args={
                    'check_same_thread': False})

            # создать объект MetaData
            self.metadata = MetaData()

            # создать таблицу известных пользователей
            users = Table('known_users', self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('username', String))

            # создать таблицу истории сообщений
            history = Table('message_history', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('contact', String),
                            Column('direction', String),
                            Column('message', Text),
                            Column('date', DateTime))

            # создать таблицу контактов
            contacts = Table('contacts', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name', String, unique=True))

            # создание таблиц
            self.metadata.create_all(self.database_engine)

            # создать отображения
            mapper(self.KnownUsers, users)
            mapper(self.MessageHistory, history)
            mapper(self.Contacts, contacts)

            # создать сессию
            Session = sessionmaker(bind=self.database_engine)
            self.session = Session()

            # очистка таблицы от контактов(при запуске подгружаются с сервера)
            self.session.query(self.Contacts).delete()
            self.session.commit()

        def add_contact(self, contact):
            '''Метод - добавление контактов'''
            if not self.session.query(
                    self.Contacts).filter_by(
                    name=contact).count():
                contact_row = self.Contacts(contact)
                self.session.add(contact_row)
                self.session.commit()

        def contacts_clear(self):
            '''Метод - очистка таблицы со списком контактов'''
            self.session.query(self.Contacts).delete()

        def del_contact(self, contact):
            '''Метод - удаление контактов'''
            self.session.query(self.Contacts).filter_by(name=contact).delete()

        def add_users(self, users_list):
            '''Метод - добавление известных пользователей'''
            self.session.query(self.KnownUsers).delete()
            for user in users_list:
                user_row = self.KnownUsers(user)
                self.session.add(user_row)
            self.session.commit()

        def save_message(self, contact, direction, message):
            '''Метод - сохранение сообщений'''
            message_row = self.MessageHistory(contact, direction, message)
            self.session.add(message_row)
            self.session.commit()

        def get_contacts(self):
            '''Метод - возвращение контактов'''
            return [contact[0]
                    for contact in self.session.query(self.Contacts.name).all()]

        def get_users(self):
            '''Метод - возвращение списка известных пользователей'''
            return [
                user[0] for user in self.session.query(
                    self.KnownUsers.username).all()]

        def check_user(self, user):
            '''Метод - проверка наличия пользователей в известных'''
            if self.session.query(
                    self.KnownUsers).filter_by(
                    username=user).count():
                return True
            else:
                return False

        def check_contact(self, contact):
            '''Метод - проверка наличия пользователя в контактах'''
            if self.session.query(
                    self.Contacts).filter_by(
                    name=contact).count():
                return True
            else:
                return False

        def get_history(self, contact):
            '''Метод - возвращение истории переписки'''
            query = self.session.query(
                self.MessageHistory).filter_by(
                contact=contact)
            return [(history_row.contact,
                     history_row.direction,
                     history_row.message,
                     history_row.date) for history_row in query.all()]

    if __name__ == 'main':
        test_db = ClientDatabase('test1')
        # for i in ['test3', 'test4', 'test5']:
        #    test_db.add_contact(i)
        # test_db.add_contact('test4')
        #test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
        #test_db.save_message('test1', 'test2', f'Тестовое сообщение от {datetime.datetime.now()}!')
        # print(test_db.get_contacts())
        # print(test_db.get_users())
        # print(test_db.check_user('test1'))
        # print(test_db.check_user('test10'))
        # print(test_db.get_history('test2'))
        print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
        # test_db.del_contact('test4')
        # print(test_db.get_contacts())
except Exception as e:
    print('РћС€РёР±РєР°:\n', traceback.format_exc())
