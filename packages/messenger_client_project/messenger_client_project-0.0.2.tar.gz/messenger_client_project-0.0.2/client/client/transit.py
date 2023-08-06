import binascii
import hashlib
import hmac
import json
import logging
import sys
import threading
import time
import socket
from PyQt5.QtCore import QObject, pyqtSignal
sys.path.append('../')
from common.utils import get_message, send_message
from common.errors import ServerError
from common.variables import USERS_REQUEST, TIME, ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, USER, ERROR, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, GET_CONTACTS, \
    LIST_INFO, ADD_CONTACT, DELETE_CONTACT, EXIT, PUBLIC_KEY, DATA, RESPONSE_511, \
    PUBLIC_KEY_REQUEST

# Логер и объект блокировки для работы с сокетом.
logger = logging.getLogger('client')
sock_lock = threading.Lock()


class ClientTransit(threading.Thread, QObject):
    '''
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    '''
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    lost_connect = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # Вызываем конструкторы предков
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Пароль
        self.password = passwd
        # Сокет для работы с сервером
        self.transit = None
        # Набор ключей для шифрования
        self.keys = keys
        # Устанавливаем соединение:
        self.connection_with_server(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.update_list_of_clients()
            self.update_list_of_contacts()
        except OSError as err:
            if err.errno:
                logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
        # Флаг продолжения работы транспорта.
        self.running = True

    def connection_with_server(self, port, ip_address):
        '''Метод отвечающий за устанновку соединения с сервером.'''
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transit.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True если
        # удалось
        connection = False
        for i in range(5):
            logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transit.connect((ip_address, port))
            except (OSError, ConnectionRefusedError) :
                pass
            else:
                connection = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connection:
            logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        logger.debug('Установлено соединение с сервером')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Авторизируемся на сервере
        with sock_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            # Отправляем серверу приветственное сообщение.
            try:
                send_message(self.transit, presense)
                ans = get_message(self.transit)
                logger.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ServerError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash = hmac.new(
                            passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.transit, my_ans)
                        self.analyze_answer_from_server(
                            get_message(self.transit))
            except (OSError, json.JSONDecodeError):
                raise ServerError('Сбой соединения в процессе авторизации.')


    def analyze_answer_from_server(self, message):
        '''Метод обработчик поступающих сообщений с сервера.'''
        logger.debug(f'Разбор приветственного сообщения от сервера: {message}')

        # Если это подтверждение чего-либо
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.update_list_of_clients()
                self.update_list_of_contacts()
                self.message_205.emit()
            else:
                logger.debug(
                    f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу, даём сигнал о
        # новом сообщении
        elif ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
            logger.debug(
                f'Получено сообщение от пользователя {message[SENDER]}:{message[MESSAGE_TEXT]}')
            self.new_message.emit(message)

    def update_list_of_contacts(self):
        '''Метод обновляющий с сервера список контактов.'''
        self.database.contacts_clear()
        logger.debug(
            f'Запрос списка контактов для пользователя {self.name}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {req}')
        with sock_lock:
            send_message(self.transit, req)
            ans = get_message(self.transit)
        logger.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            logger.error('Не удалось обновить список контактов.')

    def update_list_of_clients(self):
        '''Метод обновляющий с сервера список пользователей.'''
        logger.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            send_message(self.transit, req)
            ans = get_message(self.transit)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_clients(ans[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей.')

    def key_request(self, user):
        '''Метод запрашивающий с сервера публичный ключ пользователя.'''
        logger.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with sock_lock:
            send_message(self.transit, req)
            ans = get_message(self.transit)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            logger.error(f'Не удалось получить ключ собеседника{user}.')

    def add_contact(self, contact):
        '''Метод отправляющий на сервер сведения о добавлении контакта.'''
        logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.transit, req)
            self.analyze_answer_from_server(get_message(self.transit))

    def delete_contact(self, contact):
        '''Метод отправляющий на сервер сведения о удалении контакта.'''
        logger.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: DELETE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.transit, req)
            self.analyze_answer_from_server(get_message(self.transit))

    def transit_closed(self):
        '''Метод уведомляющий сервер о завершении работы клиента.'''
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            try:
                send_message(self.transit, message)
            except OSError:
                pass
        logger.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, to, message):
        '''Метод отправляющий на сервер сообщения для пользователя.'''
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        # Необходимо дождаться освобождения сокета для отправки сообщения
        with sock_lock:
            send_message(self.transit, message_dict)
            self.analyze_answer_from_server(get_message(self.transit))
            logger.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        '''Метод содержащий основной цикл работы транспортного потока.'''
        logger.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать тут задержку, то отправка может достаточно долго
            # ждать освобождения сокета.
            time.sleep(1)
            message = None
            with sock_lock:
                try:
                    self.transit.settimeout(0.5)
                    message = get_message(self.transit)
                except OSError as err:
                    if err.errno:
                        logger.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.lost_connect.emit()
                        # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.lost_connect.emit()
                finally:
                    self.transit.settimeout(5)

            # Если сообщение получено, то вызываем функцию обработчик:
            if message:
                logger.debug(f'Принято сообщение с сервера: {message}')
                self.analyze_answer_from_server(message)
