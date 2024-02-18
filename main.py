import telebot
from telebot import types
import sheets_google
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv('TOKEN'))

credentials_file = 'creds.json'
spreadsheet_id = os.getenv('SPREADSHEET_ID')
googlesheets_link = os.getenv('GOOGLESHEETS_LINK')


questions_list = [
    "Показания счетчика ХВ",
    "Показания счетчика ГВ",
    "Показания счетчика электроэнергии",
]

user_answers = {}
user_states = {}

QUESTION_STATE = 'questionstate'

def set_user_state(chat_id, state):
    user_states[chat_id] = state

def get_user_state(chat_id):
    return user_states.get(chat_id, None)

def ask_questions(chat_id, message_id, flat_id):
    set_user_state(chat_id, f'{QUESTION_STATE}_{flat_id}')
    if flat_id == 'flat1':
        flat_address = 'Бутлерова'
    elif flat_id == 'flat2':
        flat_address = 'Климашкина'
    bot.send_message(chat_id, f"Начинаем заполнение таблицы для квартиры <b>{flat_address}</b>. Введите:", parse_mode='html')
    ask_next_question(chat_id, message_id, flat_id, 0)

def ask_next_question(chat_id, message_id, flat_id, question_index):
    if question_index < len(questions_list):
        current_question = questions_list[question_index]
        bot.send_message(chat_id, current_question)
    else:
        sent_message = bot.send_message(chat_id=chat_id, text="Показания счетчиков сохранены локально. Спасибо!")
        print(user_answers[flat_id], flat_id)
        print(type(user_answers[flat_id]), type(flat_id))

        info = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data(flat_id, 'A1:E50', 'COLUMNS')
        # bot.send_message(chat_id, str(info['values']))
        len_columns = len(info['values'][1])
        # bot.send_message(chat_id, len_columns)

        start_row = len_columns + 1
        write_range = f'A{start_row}:D{start_row}'


        # user_answers[flat_id].insert(0, (datetime.now(timezone.utc) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M:%S'))
        user_answers[flat_id].insert(0, f'=DATEVALUE("{(datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}")')
        # user_answers[flat_id].insert(0, '=NOW()')

        data_list_to_write = [user_answers[flat_id]]
        # print(type(data_list_to_write))

        sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).write_data(flat_id, write_range, data_list_to_write, 'ROWS')
        print('строка записана')

        
        link_text = f"[GoogleSheets]({googlesheets_link})"

        updated_message = f"Показания счетчиков сохранены в {link_text}. Спасибо!"
        bot.edit_message_text(chat_id=chat_id, message_id=sent_message.message_id, text=updated_message, parse_mode='Markdown')

        user_answers[flat_id] = []
        set_user_state(chat_id, None)

def check_len_sheets_columns(data):
    return len(data['values'][0])

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Выбрать квартиру")
    item2 = types.KeyboardButton("Добавить квартиру")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ помогу с заполнением таблицы квартплаты.".format(message.from_user),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    message_id = message.message_id
    current_state = get_user_state(chat_id)

    if message.text == "Выбрать квартиру":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Бутлерова", callback_data='flat1')
        item2 = types.InlineKeyboardButton("Климашкина", callback_data='flat2')
        markup.add(item1, item2)
        bot.send_message(chat_id, 'Выбери квартиру из списка', reply_markup=markup)
    elif current_state and current_state.startswith(QUESTION_STATE):
        flat_id = current_state.split('_')[1]
        current_question_index = len(user_answers.get(flat_id, []))
        user_answer = message.text

        if flat_id not in user_answers:
            user_answers[flat_id] = []
        

        user_answers[flat_id].append(user_answer)
        next_question_index = current_question_index + 1

        ask_next_question(chat_id, message_id, flat_id, next_question_index)
    else:
        bot.send_message(chat_id, "Это обработка вне состояния вопросов.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.message:
        if call.data == 'flat1':
            # info = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data('flat1', 'A1:E10', 'COLUMNS')
            # bot.send_message(call.message.chat.id, str(info['values']))
            # bot.send_message(call.message.chat.id, str(len(info['values'][0])))
            set_user_state(chat_id, QUESTION_STATE)
            ask_questions(chat_id, message_id, 'flat1')
        elif call.data == 'flat2':
            set_user_state(chat_id, QUESTION_STATE)
            ask_questions(chat_id, message_id, 'flat2')

bot.polling(none_stop=True)
