""" Главный модуль сервера. """
import threading
import select
import socket
import json
import hmac
import binascii
import os
from logs.configs_logs import config_server_log
from common.descriptors import Port, IpAddress
from common.vars import *
from common.utilities import message_out, message_in
from common.decorators import login_required

# Загрузка логера
server_logger = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    port = Port()
    ip_address = IpAddress()

    def __init__(self, listen_address, listen_port, database):
        # Параментры подключения
        self.addr = listen_address
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
        """Метод основной цикл потока."""
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                server_logger.info(f'Установлено соедение с ПК {client_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                server_logger.error(f'Ошибка работы с сокетами: {err.errno}')

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(
                            message_in(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        server_logger.debug(f'Getting data from client exception.', exc_info=err)
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        """
        server_logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        """Метод инициализатор сокета."""
        server_logger.info(
            f'Запущен сервер, порт для подключений: {self.port} , '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def process_message(self, message):
        """
        Метод отправки сообщения клиенту.
        """
        if message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                message_out(self.names[message[DESTINATION]], message)
                server_logger.info(
                    f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] not in self.listen_sockets:
            server_logger.error(
                f'Связь с клиентом {message[DESTINATION]} была потеряна. '
                f'Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message[DESTINATION]])
        else:
            server_logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    @login_required
    def process_client_message(self, message, client):
        """Метод отбработчик поступающих сообщений."""
        server_logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message \
                and USER in message:
            # Если сообщение о присутствии то вызываем функцию авторизации.
            self.autorize_user(message, client)

        # Если это сообщение, то отправляем его получателю.
        elif ACTION in message and message[ACTION] == MESSAGE \
                and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message \
                and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.process_message(
                    message[SENDER], message[DESTINATION])
                self.process_message(message)
                try:
                    message_out(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    message_out(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # Если это запрос контакт-листа
        elif ACTION in message and message[ACTION] == GET_CONTACTS \
                and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                message_out(client, response)
            except OSError:
                self.remove_client(client)

        # Если это добавление контакта
        elif ACTION in message and message[ACTION] == ADD_CONTACT \
                and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                message_out(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это удаление контакта
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT \
                and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                message_out(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это запрос известных пользователей
        elif ACTION in message and message[ACTION] == USERS_REQUEST \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            try:
                message_out(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST \
                and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    message_out(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    message_out(client, response)
                except OSError:
                    self.remove_client(client)

        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                message_out(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        """Метод реализующий авторизцию пользователей."""
        # Если имя пользователя уже занято то возвращаем 400
        server_logger.debug(f'Start auth process for {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                server_logger.debug(f'Username busy, sending {response}')
                message_out(sock, response)
            except OSError:
                server_logger.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                server_logger.debug(f'Unknown username, sending {response}')
                message_out(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            server_logger.debug('Correct username, starting passwd check.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            server_logger.debug(f'Auth message = {message_auth}')
            try:
                # Обмен с клиентом
                message_out(sock, message_auth)
                ans = message_in(sock)
            except OSError as err:
                server_logger.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    message_out(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    message_out(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        """Метод реализующий отправки сервисного сообщения 205 клиентам."""
        for client in self.names:
            try:
                message_out(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
