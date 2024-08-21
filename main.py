#6262707708:AAHYbgPIsDrNezEu4hNRoUZQEZRIpbqey-Y
import telebot
import requests
import json
import urllib.parse
import logging
from telebot import types
from telebot.types import Update


# Replace YOUR_TOKEN with your Telegram bot token
bot = telebot.TeleBot('7541074711:AAFDRtrdcx_91CAzhWv5G_LpXItFEiCORwo')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Supported languages
languages = {
    'Afan Oromo': 'om',
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Cebuano': 'ceb',
    'Chichewa': 'ny',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Frisian': 'fy',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hausa': 'ha',
    'Hawaiian': 'haw',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hmong': 'hmn',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Igbo': 'ig',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jv',
    'Kannada': 'kn',
    'Kazakh': 'kk',
    'Khmer': 'km',
    'Kinyarwanda': 'rw',
    'Korean': 'ko',
    'Kurdish (Kurmanji)': 'ku',
    'Kyrgyz': 'ky',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Luxembourgish': 'lb',
    'Macedonian': 'mk',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Mongolian': 'mn',
    'Myanmar (Burmese)': 'my',
    'Nepali': 'ne',
    'Norwegian': 'no',
    'Nyanja (Chichewa)': 'ny',
    'Odia (Oriya)': 'or',
    'Pashto': 'ps',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese (Portugal, Brazil)': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Scots Gaelic': 'gd',
    'Serbian': 'sr',
    'Sesotho': 'st',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Sinhala (Sinhalese)': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Somali': 'so',
    'Spanish': 'es',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tagalog (Filipino)': 'tl',
    'Tajik': 'tg',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Turkmen': 'tk',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uyghur': 'ug',
    'Uzbek': 'uz',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zulu': 'zu'
}




# Define the inline query handler function
def inlinequery(inline_query):
    if not inline_query.query:
        return
    try:
        # Get the user's preferred target language
        user_id = inline_query.from_user.id
        if user_id in user_data:
            target_lang = user_data[user_id]
        else:
            target_lang = 'om' # default to Oromic if no preferred language is set
        # Translate the query text
        translation = translate_text(inline_query.query, target_lang)
        # Create an inline query result article with the original and translated text
        results = [
            telebot.types.InlineQueryResultArticle(
                id=inline_query.id,
                title='Translated Text',
                description=translation,
                input_message_content=telebot.types.InputTextMessageContent(translation)
            )
        ]
        # Send the results to the user
        bot.answer_inline_query(inline_query.id, results, cache_time=1, is_personal=True, switch_pm_text="Switch to chat mode", switch_pm_parameter="start")
    except Exception as e:
        logging.error(str(e))

# Welcome message
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    set_language_button = types.KeyboardButton('Set Language')
    markup.add(set_language_button)
    bot.send_message(message.chat.id, 'Welcome to the Translate Bot!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Set Language')
def set_language_handler(message):
    set_language(message)



# Set target language
@bot.message_handler(commands=['set'])
def set_language(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    for language in languages:
        button = types.InlineKeyboardButton(text=language, callback_data=languages[language])
        markup.add(button)
    bot.send_message(message.chat.id, 'Choose your preferred target language:', reply_markup=markup)


# Handle callback data from InlineKeyboardButton
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback_query: telebot.types.CallbackQuery):
    lang_code = callback_query.data
    user_id = callback_query.from_user.id
    bot.answer_callback_query(callback_query.id)
    # store the preferred language in a dictionary
    user_data[user_id] = lang_code
    # send a message to confirm the language selection
    bot.send_message(user_id, f"Your preferred language has been set to {lang_code}")


# Dictionary to store user's preferred target language
user_data = {}


# Translate message
@bot.message_handler(func=lambda message: True)
def translate(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in user_data:
        target_lang = user_data[user_id]
    else:
        target_lang = 'om' # default to Oromic if no preferred language is set
    translated_text = translate_text(message.text, target_lang)
    bot.send_message(chat_id, translated_text)


# Translate text function
def translate_text(text, target_lang):
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {
        'client': 'gtx',
        'sl': 'auto',
        'tl': target_lang,
        'dt': 't',
        'q': text
    }
    response = requests.get(url, params=params)
    json_data = response.json()
    translated_lines = []
    for line in json_data[0]:
        translated_lines.append(line[0])
    translated_text = ''.join(translated_lines).strip()
    return translated_text



# Handle "Set Language" button
@bot.message_handler(func=lambda message: message.text == 'Set Language')
def handle_set_language(message):
    set_language(message)

# Handle inline queries
@bot.inline_handler(lambda query: True)
def handle_inline_query(query):
    inlinequery(query)

bot.polling()
