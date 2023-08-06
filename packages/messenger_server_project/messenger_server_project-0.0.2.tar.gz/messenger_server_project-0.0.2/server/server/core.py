import sys
import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os
import traceback

sys.path.append('../')
from common.decor import login_required
from common.utils import send_message, get_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE_TEXT, MESSAGE, SENDER, \
    RESPONSE_200, RESPONSE_400, DESTINATION, EXIT, GET_CONTACTS, RESPONSE_202, \
    LIST_INFO, ADD_CONTACT, DELETE_CONTACT, USERS_REQUEST, PUBLIC_KEY_REQUEST, \
    DATA, RESPONSE_511, PUBLIC_KEY, RESPONSE_205
from common.descrpts import Port

logger = logging.getLogger('server')


class ServerMain(threading.Thread):
    '''
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    '''
    port = Port()

    def __init__(self, listen_ip_address, listen_port, database):
        # Параментры подключения
        self.addr = listen_ip_address
        self.port = listen_port
        # База данных сервера
        self.database = database
        # Сокет, через который будет осуществляться работа
        self.sock = None
        # Список подключённых клиентов.
        self.clients = []
        # Сокеты
        self.listen_sockets = None
        self.error_sockets = None
        # Флаг продолжения работы
        self.running = True
        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()
        # Конструктор предка
        super().__init__()

    def run(self):
        '''Метод основной цикл потока.'''
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_ip_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соедение с ПК {client_ip_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                logger.error(f'Ошибка работы с сокетами: {err.errno}')

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.analyze_client_message(
                            get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError):
                        self.delete_client(client_with_message)

    def delete_client(self, client):
        '''
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        '''
        logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.client_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        '''Метод инициализатор сокета.'''
        logger.info(
            f'Запущен сервер, порт для подключений: {self.port} , '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')
        transit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transit.bind((self.addr, self.port))
        transit.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transit
        self.sock.listen(MAX_CONNECTIONS)

    def analyze_message(self, message):
        '''
        Метод отправки сообщения клиенту.
        '''
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]
        ] in self.listen_sockets:
            try:
                send_message(self.names[message[DESTINATION]], message)
                logger.info(
                    f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
            except OSError:
                self.delete_client(message[DESTINATION])
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] \
                not in self.listen_sockets:
            logger.error(
                f'Связь с клиентом {message[DESTINATION]} была потеряна. '
                f'Соединение закрыто, доставка невозможна.')
            self.delete_client(self.names[message[DESTINATION]])
        else:
            logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    @login_required
    def analyze_client_message(self, message, client):
        '''Метод отбработчик поступающих сообщений.'''
        logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message and USER in message:
            # Если сообщение о присутствии то вызываем функцию авторизации.
            self.autorize_user(message, client)

        # Если это сообщение, то отправляем его получателю.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message \
                and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message \
                and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.message_transmission(
                    message[SENDER], message[DESTINATION])
                self.analyze_message(message)
                try:
                    send_message(client, RESPONSE_200)
                except OSError:
                    self.delete_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.delete_client(client)

        # Если это запрос контакт-листа
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.list_of_contacts(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.delete_client(client)

        # Если это добавление контакта
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message \
                and USER in message and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.delete_client(client)

        # Если это удаление контакта
        elif ACTION in message and message[ACTION] == DELETE_CONTACT and ACCOUNT_NAME in message \
                and USER in message and self.names[message[USER]] == client:
            self.database.delete_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.delete_client(client)

        # Если это запрос известных пользователей
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.list_of_clients()]
            try:
                send_message(client, response)
            except OSError:
                self.delete_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST \
                and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.delete_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(client, response)
                except OSError:
                    self.delete_client(client)

        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_message(client, response)
            except OSError:
                self.delete_client(client)

    def autorize_user(self, message, sock):
        '''Метод реализующий авторизцию пользователей.'''
        # Если имя пользователя уже занято то возвращаем 400
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_client(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(
                self.database.get_hash(
                    message[USER][ACCOUNT_NAME]),
                random_str, 'MD5')
            digest = hash.digest()
            try:
                # Обмен с клиентом
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                print(f'Ошибка: {err}', traceback.format_exc())
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip_address, client_port = sock.getpeername()
                try:
                    send_message(sock, RESPONSE_200)
                except OSError:
                    self.delete_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.database.client_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip_address,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        '''Метод реализующий отправки сервисного сообщения 205 клиентам.'''
        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.delete_client(self.names[client])
