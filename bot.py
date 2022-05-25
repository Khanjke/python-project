import telebot
import enum
import game
import analyzer
import config
from bs4 import BeautifulSoup


# states of bot input
class States(enum.Enum):
    Idle = 0
    DirePick = 1
    RadiantPick = 2


# initialization
bot = telebot.TeleBot(config.token)
cur_analyzer = analyzer.Analayzer()
# dicts r used to store personal data for each user
cur_game = dict()
cur_state = dict()


# message handling
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Готовы к новому драфту\n"
                                      "Используй /dire или /radiant чтобы добавить героев в команды")

    cur_game[str(message.chat.id)] = game.Game([], [])
    cur_state[str(message.chat.id)] = States.Idle
    reply_text = cur_game[str(message.chat.id)].display()
    bot.send_message(message.chat.id, reply_text)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/start чтобы начать драфт, следуй инструкциям')
    bot.send_message(message.chat.id, '/info чтобы узнать о боте больше')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, "Добро пожаловать!\n"
                                      "Dota Draft Helper это телеграмм-бот, который помогает выбрать лучшего персонажа"
                                      " против уже взятых, основываясь на статистике собранной на"
                                      " https://ru.dotabuff.com/\nВ доте у персонажей есть сильные и слабые стороны,"
                                      " и определенные персонажи могут своим присутствием в игре свести силу персонажа"
                                      " соперника на нет.  В каком то смысле это камень-ножницы-бумага, одни герои"
                                      " хороши против других, но слабы против третьих. Dota Draft Helper помогает найти"
                                      " такого героя, который хорошо выступает против героев соперника.")


@bot.message_handler(commands=['dire'])
def dire(message):
    bot.send_message(message.chat.id, "Вводи персонажа dire")
    cur_state[str(message.chat.id)] = States.DirePick


@bot.message_handler(commands=['radiant'])
def radiant(message):
    bot.send_message(message.chat.id, "Вводи персонажа radiant")
    cur_state[str(message.chat.id)] = States.RadiantPick


@bot.message_handler(commands=['analyze'])
def analyze(message):
    bot.send_message(message.chat.id, "Лучшие пики")
    reply_txt = str(cur_analyzer.analyze(cur_game[str(message.chat.id)]))
    bot.send_message(message.chat.id, reply_txt)
    if cur_state[str(message.chat.id)] == States.RadiantPick:
        bot.send_message(message.chat.id, "Можешь продолжать вводить персонажей radiant\n"
                                          "/start если хочешь начать сначала\n"
                                          "/dire переключиться на другую команду\n")
    elif cur_state[str(message.chat.id)] == States.DirePick:
        bot.send_message(message.chat.id, "Можешь продолжать вводить персонажей dire\n"
                                          "/start если хочешь начать сначала\n"
                                          "/radiant переключиться на другую команду\n")


@bot.message_handler()
def handle_a_message(message):
    if str(message.chat.id) not in cur_state.keys():
        cur_state[str(message.chat.id)] = States.Idle
    if cur_state[str(message.chat.id)] == States.Idle:
        bot.send_message(message.chat.id, '/start чтобы начать драфт, следуй инструкциям')
    else:
        # добавление героя
        if message.text not in cur_analyzer.hero_list:
            bot.send_message(message.chat.id, "Такого героя нет, попробуй еще раз, формат ввода такой 'wraith-king'")
            if cur_state[str(message.chat.id)] == States.RadiantPick:
                bot.send_message(message.chat.id, "Вводи персонажа radiant")
            elif cur_state[str(message.chat.id)] == States.DirePick:
                bot.send_message(message.chat.id, "Вводи персонажа dire")
        else:
            if cur_state[str(message.chat.id)] == States.RadiantPick:
                # добавляем героя
                cur_game[str(message.chat.id)].add_radiant(message.text)
                # выводем обновлённую информацию
                reply_text = cur_game[str(message.chat.id)].display()
                bot.send_message(message.chat.id, reply_text)
                bot.send_message(message.chat.id, "/analyze для результата\n"
                                                  "/dire переключиться на другую команду")
                bot.send_message(message.chat.id, "Вводи персонажа radiant")
            elif cur_state[str(message.chat.id)] == States.DirePick:
                # добавляем героя
                cur_game[str(message.chat.id)].add_dire(message.text)
                # выводем обновлённую информацию
                reply_text = cur_game[str(message.chat.id)].display()
                bot.send_message(message.chat.id, reply_text)
                bot.send_message(message.chat.id, "/analyze для результата\n"
                                                  "/radiant переключиться на другую команду")
                bot.send_message(message.chat.id, "Вводи персонажа dire")


bot.polling()
