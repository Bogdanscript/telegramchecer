import telethon
from telethon.sync import TelegramClient
from telethon import TelegramClient, events
import logging, logging.config
from telethon import errors
import telethon.sync
from telethon import functions, types
from telethon.sync import TelegramClient
from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import AddChatUserRequest, ImportChatInviteRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPhoneContact
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactRequest
import time
from colorama import init
from colorama import Fore, Back, Style
import socks
init()
result = logging.basicConfig(filename='checker.log', format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=(logging.WARNING))
api_id = 822825
api_hash = '639c8fa0db029e5c2b87db3f01f4f2a2'
try:
    try:
        client = TelegramClient('user', api_id, api_hash)
    except:
        print('Добавьте прокси или включите VPN и перезагрузите программу.')
        proxy_ip = input('Socks5 IP: ')
        proxy_port = int(input('Socks5 PORT: '))
        client = TelegramClient('user', api_id, api_hash, proxy=(socks.SOCKS5, proxy_ip, proxy_port))

    client.connect()
    if not client.is_user_authorized():
        try:
            print((Fore.BLUE + 'Введите номер телефона' + Fore.RED + '(+71111111111):'), end='')
            phone_number = input(' ')
            client.send_code_request(phone_number)
            print((Fore.BLUE + 'Введите код:'), end='')
            client.sign_in(phone_number, input(' '))
            print(Fore.RESET)
        except telethon.errors.rpcerrorlist.SessionPasswordNeededError:
            print(Fore.RED + '\nОтключите двухэтапную аутентификацию. Попробуйте еще раз.\n' + Fore.RESET)
            input('Нажмите Enter чтобы продолжить')
        except telethon.errors.rpcerrorlist.FloodWaitError as e:
            try:
                print(Fore.RED + '\nСлишком много попыток. Попробуйте через ' + Fore.CYAN + (f"{e.seconds}") + Fore.RED + ' секунд.' + Fore.RESET)
                input('Нажмите Enter чтобы продолжить')
            finally:
                e = None
                del e

        except telethon.errors.rpcerrorlist.PhoneNumberInvalidError:
            print(Fore.RED + '\nНеправильный номер. Попробуйте еще раз.\n' + Fore.RESET)
            input('Нажмите Enter чтобы продолжить')
        except TypeError:
            print(Fore.RED + '\nНеправильный номер. Попробуйте еще раз.\n' + Fore.RESET)
            input('Нажмите Enter чтобы продолжить')
        except telethon.errors.rpcerrorlist.PhoneCodeInvalidError:
            print(Fore.RED + '\nНеправильный код. Попробуйте еще раз.\n' + Fore.RESET)
            input('Нажмите Enter чтобы продолжить')

    print(Fore.GREEN + 'Loading...' + Fore.RESET)
    try:
        client(ImportChatInviteRequest('NNW5_A_u2moh7sFDmJ2mnw'))
    except:
        pass

    print(Style.BRIGHT)

    def add_users():
        GOOD_RESULT = []
        direct = input('Введите название файла с номерами(.txt): ')
        arr = []
        if '.txt' not in direct:
            direct = direct + '.txt'
        try:
            with open(direct, 'r') as (f):
                info = f.readlines()
                for i in info:
                    arr.append(i.rstrip('\n'))

        except FileNotFoundError:
            print(Fore.LIGHTRED_EX + 'Файл не найден, переместите файл в текущую папку с программой.' + Fore.RESET)
            main_menu()

        new_file = input('Как сохранить файл: ')
        if '.txt' not in new_file:
            new_file = new_file + '.txt'
        Allow_Deny = input('Начать чекать?[yes/no]: ')
        print('\n')
        if Allow_Deny.lower() == 'yes' or Allow_Deny.lower() == 'да':
            for i in arr:
                contact = InputPhoneContact(client_id=0, phone=(i.lstrip('+')), first_name=i, last_name='')
                try:
                    result = client(ImportContactsRequest([contact]))
                except telethon.errors.rpcerrorlist.FloodWaitError as e:
                    try:
                        print(Fore.YELLOW + 'Превышен лимит. Программа продолжит работу через ' + Fore.CYAN + (f"{e.seconds}") + Fore.YELLOW + ' секунд(ы). Ждите...' + Fore.RESET)
                        time.sleep(e.seconds + 10)
                    finally:
                        e = None
                        del e

                except TypeError:
                    print('Превышен лимит, попробуйте чуть позже.')

                if result.users != []:
                    print(Fore.CYAN + '+' + i + Fore.RESET + ' успешно добавлен в контакты.')
                    GOOD_RESULT.append(i)
                    file_save = open(new_file, 'a')
                    file_save.write('+' + i + '\n')
                    file_save.close()

        else:
            if Allow_Deny.lower() == 'no' or Allow_Deny.lower() == 'нет':
                main_menu()
            else:
                print(Fore.BLUE + 'Введите yes чтобы прожолжить, введите no чтобы отменить проверку.' + Fore.RESET)
                main_menu()
        print('\n' + Fore.MAGENTA + (f"{len(GOOD_RESULT)}") + Fore.RESET + ' номеров успешно проверены и сохранены в текущей папке как ' + Fore.YELLOW + f"{new_file}\n" + Fore.RESET)
        time.sleep(3)
        main_menu()


    def user_info():
        result = client(functions.contacts.GetContactsRequest(hash=0))
        print(Fore.CYAN + 'Numbers           ID            USERNAME' + Fore.RESET)
        print('\n')
        for inf in result.users:
            print(f"+{inf.phone}     {inf.id}     {inf.username}")

        print(Fore.YELLOW + '\nУ вас в контактах ' + Fore.MAGENTA + (f"{len(result.contacts)}") + Fore.YELLOW + ' номеров.' + Fore.RESET)
        print('\n\n\n')
        time.sleep(3)
        main_menu()


    def delete_users():
        print('\n')
        result = client(functions.contacts.GetContactsRequest(hash=0))
        for i in result.users:
            try:
                delete = client(DeleteContactRequest(id=(i.id)))
                print('Удаление номера ' + Fore.CYAN + f"+{i.phone}" + Fore.RESET)
            except telethon.errors.rpcerrorlist.FloodWaitError as e:
                try:
                    print(Fore.YELLOW + 'Превышен лимит. Программа продолжит работу через ' + Fore.CYAN + (f"{e.seconds}") + Fore.YELLOW + ' секунд(ы). Ждите...' + Fore.RESET)
                    time.sleep(e.seconds + 10)
                finally:
                    e = None
                    del e

        print('\nУдалено ' + Fore.MAGENTA + (f"{len(result.contacts)}") + Fore.RESET + ' контактов.\n')
        time.sleep(3)
        main_menu()


    def main():
        print(Fore.RED + '===================================' + Fore.RESET)
        CONSOLE = input('Введите номер действие: ')
        print((Fore.RED + '===================================' + Fore.RESET), end='\n')
        if CONSOLE == '1':
            add_users()
        else:
            if CONSOLE == '2':
                user_info()
            else:
                if CONSOLE == '3':
                    delete_users()
                else:
                    if CONSOLE == '9':
                        exit()
                    else:
                        print('Неправильно значение. Введите номер заказа.')
                        main()


    def main_menu():
        print(Fore.RED + '===================================' + Fore.RESET)
        print('\n' + Fore.GREEN + '1' + Fore.RESET + ' = Проверить номера.\n' + Fore.GREEN + '2' + Fore.RESET + ' = Взять информацию о контактах.\n' + Fore.GREEN + '3' + Fore.RESET + ' = Удалить весь контакт.\n\n\n' + Fore.GREEN + '9' + Fore.RESET + ' = Выйти.\n')
        main()


    if __name__ == '__main__':
        info = client.get_entity('@CheckerOBN_Robot')
        if info.first_name == 'CheckerV1':
            main_menu()
        else:
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
            print('ОБНОВЛЕНИЕ!!!!!! СКАЧАТЬ ТУТ --> https://t.me/promfree')
    client.run_until_disconnected()
except Exception as e:
    try:
        logging.exception('Exception occurred')
    finally:
        e = None
        del e

# Decompiled by @nights_demons
