from flask import Flask, request
from os import environ
from time import gmtime, asctime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import telebot

from stuff import markups, messages

# TODO
#  1) Залить на свой гит
#  2) Чтобы был файл doc

token = environ.get('TOKEN_HW')
password = environ.get('PASSWORD_HW')
server = Flask(__name__)
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    send_mail(message)
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.START, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['about'])
def about_message(message):
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.ABOUT, reply_markup=markups.source_markup,
                     parse_mode='markdown')


def help_message(message):
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.HELP, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.FEEDBACK, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['log'])
def log_message(message):
    if message.from_user.username != 'dam_mek':
        bot.send_message(chat_id=message.chat.id, text='*Ты чо удумал?!*', reply_markup=markups.source_markup,
                         parse_mode='markdown')
        log(message)
        return
    filename = 'log.log'
    with open(filename, 'r') as file:
        global password
        email = 'denisov_aa@gkl-kemerovo.ru'
        mail_account = smtplib.SMTP('smtp.gmail.com', 587)
        mail_account.starttls()
        mail_account.login(user=email, password=password)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Logging AntiMazur bot!'
        f = MIMEText(file.read(), _subtype='plain')
        f.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(f)

        text_message = f'Логи за {asctime()}'
        msg.attach(MIMEText(text_message, 'plain'))
        mail_account.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
        mail_account.quit()
    with open(filename, 'w') as file:
        file.write('======== LOGGING FILE FOR SOMELOG ======\n')
    bot.send_message(chat_id=message.chat.id, text='Всё сделано, Мой Господин', reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def dialogue(message):
    log(message)
    if do_prikol(message):
        return
    if message.text.lower() == 'выбрать пункт конспекта':
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_TEXT, reply_markup=markups.abstract_markup,
                               parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
    else:
        help_message(message)


@bot.message_handler(content_types=['video_note'])
def video(message):
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.source_markup,
                     parse_mode='markdown')


def ask_text(message):
    log(message)
    if message.text is None:
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_EXACTLY_TEXT, parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
        return
    if message.text.lower() == 'файл doc':
        doc = open('kospekt.doc', 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=markups.source_markup)
        doc.close()
        return
    if message.text == '1':
        msg_text = messages.P_1
    elif message.text == '2':
        msg_text = messages.P_2
    elif message.text == '3':
        msg_text = messages.P_3
    elif message.text == '4':
        msg_text = messages.P_4
    elif message.text == '5':
        msg_text = messages.P_5
    elif message.text == '6':
        msg_text = messages.P_6
    elif message.text == '7':
        msg_text = messages.P_7
    elif message.text == '8':
        msg_text = messages.P_8
    elif message.text == '9':
        msg_text = messages.P_9
    elif message.text == '10':
        msg_text = messages.P_10
    elif message.text == '11':
        msg_text = messages.P_11
    else:
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_EXACTLY_TEXT, parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
        return
    bot.send_message(chat_id=message.chat.id, text=msg_text, parse_mode='markdown',
                     reply_markup=markups.source_markup)


def do_prikol(msg):
    """
    It will do prikol. Return True if prikol can exist

    :param msg: <class 'telebot.types.Message'>
    :return: bool
    """
    text = msg.text.lower()
    if text in {'suck', 'пососи'}:
        bot.send_message(msg.chat.id, messages.suck)
    elif text in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(msg.chat.id, messages.cadillac)
    elif text in {'baby', 'малышка'}:
        bot.send_message(msg.chat.id, messages.baby)
    elif text in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(msg.chat.id, messages.ice)
    elif text in {'плодотворная дебютная идея'}:
        bot.send_message(msg.chat.id, messages.ostap)
    else:
        return False
    return True


def send_mail(message):
    global password
    email = 'denisov_aa@gkl-kemerovo.ru'
    mail_account = smtplib.SMTP('smtp.gmail.com', 587)
    mail_account.starttls()
    mail_account.login(user=email, password=password)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = f'Logging. {message.from_user.username} {message.from_user.first_name} sent a message to the bot!'
    text_message = create_log_str(message)
    msg.attach(MIMEText(text_message, 'plain'))
    mail_account.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
    mail_account.quit()


def log(message):
    with open('log.log', 'a') as file:
        file.write(create_log_str(message) + '\n')


def create_log_str(message):
    date = message.date
    date = '{}.{}.{} {}:{}:{}'.format(str(gmtime(date).tm_mday).rjust(2, '0'), str(gmtime(date).tm_mon).rjust(2, '0'),
                                      str(gmtime(date).tm_year).rjust(2, '0'), str(gmtime(date).tm_hour).rjust(2, '0'),
                                      str(gmtime(date).tm_min).rjust(2, '0'), str(gmtime(date).tm_sec).rjust(2, '0'))

    log_str = 'message_id:{}|date:{}|used_id:{}|username:{}|first_name:{}|last_name:{}|text:{}'.format(
        message.message_id, date, message.from_user.id, message.from_user.username,
        message.from_user.first_name, message.from_user.last_name, message.text
    )
    return log_str


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'Ну типа Хомворкер запущен', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-dammek-bot.herokuapp.com/' + token)
    return 'Ну типа АнтиМазур запущен, а я нужен для вебхука', 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
