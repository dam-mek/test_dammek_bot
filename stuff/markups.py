from telebot import types

source_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
source_markup_btn1 = types.KeyboardButton('Выбрать пункт конспекта')
source_markup_btn2 = types.KeyboardButton('/about')
source_markup_btn3 = types.KeyboardButton('/feedback')
source_markup.add(source_markup_btn1)
source_markup.add(source_markup_btn2)
source_markup.add(source_markup_btn3)

abstract_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
abstract_markup_btns = [types.KeyboardButton(str(i+1)) for i in range(12)]
abstract_markup_btns[11] = types.KeyboardButton('Файл doc')
for i in range(4):
    abstract_markup.row(abstract_markup_btns[i*3], abstract_markup_btns[i*3+1], abstract_markup_btns[i*3+2])

none_markup = types.ReplyKeyboardRemove()
