import telebot
from telebot import types
import sheets_google
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
import locale
load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv('TOKEN'))

credentials_file = 'creds.json'
spreadsheet_id = os.getenv('SPREADSHEET_ID')
googlesheets_link = os.getenv('GOOGLESHEETS_LINK')

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

questions_list = {
    'flat0': [
        "Показания счетчика электроэнергии Т1",
        "Показания счетчика электроэнергии Т2",
        "Показания счетчика ХВ",
        "Показания счетчика ГВ",
    ],
    'flat1': [
        "Показания счетчика электроэнергии Т1",
        "Показания счетчика электроэнергии Т2",
        "Показания счетчика электроэнергии Т3",
        "Показания счетчика ХВ",
        "Показания счетчика ГВ",
    ],
    'flat2': [
        "Показания счетчика электроэнергии Т1",
        "Показания счетчика электроэнергии Т2",
        "Показания счетчика ХВ",
        "Показания счетчика ГВ",
    ],
}

# def choose_row(row):
#     chosen_row = {
#         'flat0': [('A', row), ('C', row), ('F', row), ('I', row), ('L', row)],
#         'flat1': [('A', row), ('C', row), ('F', row), ('I', row), ('L', row), ('O', row)],
#         'flat2': [('A', row), ('C', row), ('F', row), ('I', row), ('L', row)],
#     }
#     return chosen_row

sheet_value_indexes = {
    'flat0': [0,2,5,8,11],
    'flat1': [0,2,5,8,11,14],
    'flat2': [0,2,5,8,11],
}

sheet_link = {
    'flat0': '#gid=496456968',
    'flat1': '#gid=0',
    'flat2': '#gid=255523584',
}

all_flat_info = {
    'flat0': 'Тестовая',
    'flat1': 'Бутлерова',
    'flat2': 'Климашкина',
}


user_answers = {}
user_states = {}

QUESTION_STATE = 'questionstate'

def set_user_state(chat_id, state):
    user_states[chat_id] = state

def get_user_state(chat_id):
    return user_states.get(chat_id, None)

# def user_answers_index_into_sheets_index(user_ans, flat_id):
#     sheets_row = [] * 12
#     for index, sheet_index in enumerate(sheet_indexes[flat_id]):
#         sheets_row[sheet_index] = user_ans[index]
#     return sheets_row

def sheet_values_func(flat_id):
    sheet_values = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data(flat_id, 'A1:O50', 'ROWS')
    return sheet_values


def ask_questions(chat_id, message_id, flat_id):
    set_user_state(chat_id, f'{QUESTION_STATE}_{flat_id}')
    # if flat_id == 'flat0':
    #     flat_address = 'Тестовая'
    # elif flat_id == 'flat1':
    #     flat_address = 'Бутлерова'
    # elif flat_id == 'flat2':
    #     flat_address = 'Климашкина'
    flat_address = all_flat_info[flat_id]


    sheet_values = sheet_values_func(flat_id)
    try:
        len_sheet_columns = len(sheet_values['values'])  
    except:
        len_sheet_columns = 0

    prev_month_info = ''
    prev_month_info = f"Прошлая запись за {sheet_values['values'][len_sheet_columns-2][sheet_value_indexes[flat_id][0]]}\n"
    for i in range(len(questions_list[flat_id])):
        prev_month_info += f"{questions_list[flat_id][i][-2:]}: {sheet_values['values'][len_sheet_columns-2][sheet_value_indexes[flat_id][i+1]]}\n"
    bot.send_message(chat_id, f"Начинаем заполнение таблицы для квартиры <b>{flat_address}</b>.\n\n{prev_month_info}\nВведите:", parse_mode='html')
    ask_next_question(chat_id, message_id, flat_id, 0)

def ask_next_question(chat_id, message_id, flat_id, question_index):
    if question_index < len(questions_list[flat_id]):
        ############### ПОДУМАТЬ КАК СДЕЛАТЬ ПРОВЕРКУ НА ВВОД ЗНАЧЕНИЯ СЧЕТЧИКА

        # if (user_answers[question_index-1] < prev_month_info[question_index-1]):
        #     bot.send_message(chat_id, "Введенное значение меньше предыдущего. Попробуйте еще раз.")
        current_question = questions_list[flat_id][question_index]
        bot.send_message(chat_id, current_question)
    else:
        sent_message = bot.send_message(chat_id=chat_id, text="Показания счетчиков сохранены локально. Спасибо!")
        print(user_answers[flat_id], flat_id)
        print(type(user_answers[flat_id]), type(flat_id))

        info = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data(flat_id, 'A1:O50', 'COLUMNS')
        # bot.send_message(chat_id, str(info['values']))
        try:
            len_columns = len(info['values'][0])
        except:
            len_columns = 0
        # bot.send_message(chat_id, len_columns)

        print('ДЛИНА КОЛОНОК-----------------------------------', len_columns)

        start_row = len_columns + 1

        # write_range = f'A{start_row}:L{start_row}'

        # user_answers[flat_id].insert(0, (datetime.now(timezone.utc) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M:%S'))
        user_answers[flat_id].insert(0, f'=DATEVALUE("{(datetime.now(timezone.utc) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}")')
        # user_answers[flat_id].insert(0, '=NOW()')

        
        # print(user_answers_index_into_sheets_index(user_answers[flat_id], flat_id))
        # data_list_to_write = [user_answers_index_into_sheets_index(user_answers[flat_id], flat_id)]
        

        # print(type(data_list_to_write))
        dict_list_of_tuples_to_write = {
            'flat0': [('A', start_row), ('C', start_row), ('F', start_row), ('I', start_row), ('L', start_row)],
            'flat1': [('A', start_row), ('C', start_row), ('F', start_row), ('I', start_row), ('L', start_row), ('O', start_row)],
            'flat2': [('A', start_row), ('C', start_row), ('F', start_row), ('I', start_row), ('L', start_row)],
        }
        
        # sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).write_data_local_calculation(flat_id, write_range, data_list_to_write, 'ROWS')
        sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).write_data_with_calculating_in_the_table(flat_id, dict_list_of_tuples_to_write[flat_id], user_answers[flat_id], 'ROWS')

        print('строка записана')

        
        link_text = f"[GoogleSheets]({googlesheets_link+sheet_link[flat_id]})"

        updated_message = f"Показания счетчиков сохранены в {link_text}. Спасибо!"
        bot.edit_message_text(chat_id=chat_id, message_id=sent_message.message_id, text=updated_message, parse_mode='Markdown')

        final_info = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data(flat_id, f'A{start_row-1}:U{start_row}', 'ROWS')
        # 15 - итоговая сумма (-3)
        # 16 - дата (-2)
        # 17 - адрес квартиры (-1)
        print('\n\n', final_info['values'])


        cur_date = datetime.strptime(final_info['values'][1][-2], "%d.%m.%Y").strftime("%d %B")
        prev_date = datetime.strptime(final_info['values'][0][-2], "%d.%m.%Y").strftime("%d %B")
        if (float(final_info['values'][1][-3].replace(",", ".")) >= 0):
            bot.send_message(chat_id=chat_id, text=f"Итоговая сумма квартплаты по адресу {final_info['values'][1][-1]} в период с {prev_date} по {cur_date} получается <b>{final_info['values'][1][-3]}</b> рублей", parse_mode='html')
        else:
            bot.send_message(chat_id=chat_id, text=f"Получилось отрицателное значение. Зайдите в таблицу и исправьте значения вручную.", parse_mode='html')

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
        item0 = types.InlineKeyboardButton("Тестовая", callback_data='flat0')

        item1 = types.InlineKeyboardButton("Бутлерова", callback_data='flat1')
        item2 = types.InlineKeyboardButton("Климашкина", callback_data='flat2')
        markup.add(item0, item1, item2)
        # markup.add(item1, item2)

        # markup.add(item0)

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
        if call.data in ['flat0', 'flat1', 'flat2']:
            # sheet_values = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data(call.data, 'A1:O50', 'ROWS')
            # try:
            #     len_sheet_columns = len(sheet_values['values'])
            # except:
            #     len_sheet_columns = 0
            set_user_state(chat_id, QUESTION_STATE)
            ask_questions(chat_id, message_id, call.data)
        

        # if call.data == 'flat1':
        #     # info = sheets_google.GoogleSheetsHandler(credentials_file, spreadsheet_id).read_data('flat1', 'A1:E10', 'COLUMNS')
        #     # bot.send_message(call.message.chat.id, str(info['values']))
        #     # bot.send_message(call.message.chat.id, str(len(info['values'][0])))
        #     set_user_state(chat_id, QUESTION_STATE)
        #     ask_questions(chat_id, message_id, 'flat1')
        # elif call.data == 'flat2':
        #     set_user_state(chat_id, QUESTION_STATE)
        #     ask_questions(chat_id, message_id, 'flat2')
        # elif call.data == 'flat0':
        #     set_user_state(chat_id, QUESTION_STATE)
        #     ask_questions(chat_id, message_id, 'flat0')


print('hohoho')
bot.polling(none_stop=True)
