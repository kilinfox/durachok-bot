from telebot import types
from player import Player
from inf import Information
from game import Game

class Trans:
    #два класса в одном - поменять
    def __init__(self, bot):
        self.bot = bot

    def request(self, text, player):
        #возвращает выбранную пользователем карту
        #pl - объект класса Player
        markup = types.InlineKeyboardMarkup(row_width=1)
        if player.pl_hand.hand:
            buttons = [types.InlineKeyboardButton(Secul.str_to_unicode(str(x)), callback_data= x.name + ' ' + str(x.cost)) for x in player.pl_hand.hand]
            empty = types.InlineKeyboardButton('Ничего', callback_data="empty")
            for but in buttons:
                markup.add(but)
            markup.add(empty)
            self.bot.send_message(player.pl_id, text, reply_markup=markup)

    def answer(self, player):
        while True:
                try:
                    data = answer_var
                    if data == '':
                        raise ValueError
                    if data != '':
                        print(data)
                    if data == "empty":
                        return ""
                    if data != 'empty' and data != '':
                        return Secul.str_to_card_trn([data[0:-1], data[-1]])
                except:
                    continue
                finally:
                    answer_var = ''

    def show(self, text, player):
        self.bot.send_message(player.pl_id, text)

import telebot
from telebot import types

bot = telebot.TeleBot('5680182660:AAF2rVr0r3CFlC7O9xKDvEwBVyPscMHMUXk')
inf = Information()

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username:
        inf.put(message.from_user.username, message.chat.id)
        bot.send_message(message.chat.id, 'Ваш username в телеграме - ваш ник в этой игре.\n' + message.from_user.username)
        bot.send_message(message.chat.id, 'Начать новую игру: /start_game')
    else:
        if not inf.show(message.chat.id):
            name = bot.send_message(message.chat.id, 'Придумайте имя:')
            bot.register_next_step_handler(name, new_name)

def new_name(message):
    if not inf.show(message.text):
        inf.put(message.text, message.chat.id)
        bot.send_message(message.chat.id, 'Начать новую игру: /start_game')
    else:
        name = bot.send_message(message.chat.id, 'Это имя занято. Придумайте другое имя:')
        bot.register_next_step_handler(name, new_name)


@bot.callback_query_handler(func=lambda call: True)
def call_back_but(call):
    if call.message:
        global answer_var
        if call.data != "empty":
            name, cost = call.data.split(' ')
            answer_var = [name, int(cost)]
        else:
            answer_var = "empty"



@bot.message_handler(commands=['start_game'])
def start_game(message):
    try:
        if message.chat.id == inf.show('karyysow'):
            bot.send_message(message.chat.id, 'Привет, Катя!' + '\u2764')
    finally:
        inf.app_user(message.from_user.username)
        username = bot.send_message(message.chat.id,
                                    'Введите username пользователя(без знака собаки), с которым хотите начать игру. Убедитесь в том, что пользователь зарегистрирован в боте(хоть раз набирал команду /start).')
        bot.register_next_step_handler(username, func_2)

def func_2(message):
    user_2 = inf.show(message.text)
    if user_2:
        answer = bot.send_message(user_2, f'Пользователь {inf.first_pl()} предлагает играть. Вы согласны?')
        bot.register_next_step_handler(answer, func_3)
    else:
        bot.send_message(message.chat.id, 'Этот пользователь не был зарегестрирован!!!')

def func_3(message):
    if 'да' in message.text.lower():
        if inf.first_pl() == message.from_user.username:
            bot.send_message(inf.show(inf.first_pl()), 'Вы не можете играть сами с собой!!!')
        else:
            inf.app_user(message.from_user.username)
            bot.send_message(inf.show(inf.first_pl()), f'Пользователь {inf.second_pl()} согласился играть.')
            game = Game(inf.show(inf.first_pl()), inf.show(inf.second_pl()), bot)
            game.main_loop()
    else:
        bot.send_message(inf.show(inf.first_pl()), f'Пользователь отказался играть.')

@bot.message_handler(content_types=['text'])
def hello(message):
    if message.text.lower() == 'привет':
        idd = message.chat.id
        if message.chat.id == inf.show('karyysow'):
            bot.send_message(idd, 'Привет, Катя!' + '\u2764')

        elif message.chat.id == inf.show('Chalemone'):
            bot.send_message(idd, 'Привет, Эля!')
        elif message.chat.id == inf.show('tokiponist'):
            bot.send_message(idd, 'Здравствуй, создатель!')
        else:
            bot.send_message(idd, f'Привет, {message.from_user.first_name}!')

bot.infinity_polling()
