import telebot
from telebot import types

alphabet = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9,
    'И': 10, 'Й': 11, 'К': 12, 'Л': 13, 'М': 14, 'Н': 15, 'О': 16, 'П': 17,
    'Р': 18, 'С': 19, 'Т': 20, 'У': 21, 'Ф': 22, 'Х': 23, 'Ц': 24, 'Ч': 25,
    'Ш': 26, 'Щ': 27, 'Ъ': 28, 'Ы': 29, 'Ь': 30, 'Э': 31, 'Ю': 32, 'Я': 33
}

bot = telebot.TeleBot('6163974304:AAE8QrsiTx_6LLGKYFEccCXCrOoA_mRCh3M')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    encrypt_btn = types.KeyboardButton('Зашифровать текст')
    decrypt_btn = types.KeyboardButton('Расшифровать текст')
    markup.add(encrypt_btn, decrypt_btn)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def process_message(message):
    if message.text == 'Зашифровать текст':
        bot.send_message(message.chat.id, 'Введите текст для шифрования:')
        bot.register_next_step_handler(message, encrypt_text)
    elif message.text == 'Расшифровать текст':
        bot.send_message(message.chat.id, 'Введите текст для расшифровки:')
        bot.register_next_step_handler(message, decrypt_text)
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда. Пожалуйста, выберите действие из предложенных кнопок.')

def encrypt_text(message):
    def encrypt(sentence):
        words = sentence.split()
        result = ''
        for index, word in enumerate(words):
            symbols = ''
            for symbol in word:
                if not symbol.isalpha():
                    symbols += symbol
            encrypted_word = 'п'
            for letter in word:
                if letter.isalpha():
                    encrypted_word += 'и' * alphabet[letter]
                    encrypted_word += 'п'
            result += encrypted_word + symbols
            if index != len(words) - 1:
                result += ' '
        return result

    sentence = message.text.strip()
    encrypted = encrypt(sentence.upper())
    bot.send_message(message.chat.id, 'Зашифрованный текст:')
    bot.send_message(message.chat.id, encrypted)

def decrypt_text(message):
    import re

    def decrypt(sentence):
        words = sentence.split()
        result = ''
        for index, word in enumerate(words):
            symbols = re.findall(r'[^\w\s]', word)
            word = re.sub(r'[^\w\s]', '', word)
            decrypted_word = ''
            count = 0
            for symbol in word:
                if symbol == 'и':
                    count += 1
                else:
                    if count > 0:
                        decrypted_word += list(alphabet.keys())[list(alphabet.values()).index(count)]
                        count = 0
                    decrypted_word += symbol
            if count > 0:
                decrypted_word += list(alphabet.keys())[list(alphabet.values()).index(count)]
            decrypted_word = decrypted_word.replace('п', '')
            result += decrypted_word + ' '.join(symbols)
            if index != len(words) - 1:
                result += ' '
        return result

    sentence = message.text.strip()
    decrypted = decrypt(sentence)
    bot.send_message(message.chat.id, 'Расшифрованный текст:')
    bot.send_message(message.chat.id, decrypted)

bot.polling()