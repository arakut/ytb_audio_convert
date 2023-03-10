import os
import telebot
from pytube import YouTube


bot = telebot.TeleBot('YOUR TOKEN')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Привет, я бот который конвертирует видео с YouTube в аудио файл для тебя.")
    bot.send_message(message.from_user.id,
                     "Чтобы перевести видео в аудио напиши /download")


@bot.message_handler(commands=['download'])
def get_link_audio(message):
    bot.send_message(message.from_user.id,
                     "Отправь ссылку на нужное тебе видео.")

    bot.register_next_step_handler(message, download_audio)


def download_audio(message):

    bot.send_message(message.from_user.id,
                     "Уже выполняю. Жди...")

    # Создаем класс видео с ютуба
    yt = YouTube(str(message))

    # Выделяем только аудиодорожки у выбранного видео
    try:
        audio = yt.streams.filter(only_audio=True).filter(mime_type='audio/mp4').order_by(attribute_name='filesize')
    except:
        audio = yt.streams.filter(only_audio=True).order_by(attribute_name='filesize')

    # Достаем нахвание видео
    title = audio[-1].title

    # Заменяем запрещенные символы для нахваний
    if '/' or ':' or '*' or '?' or '<' or '>' or '|' in title:
        title = title.replace('/', '_') \
            .replace(':', '_') \
            .replace('*', '_') \
            .replace('?', '_') \
            .replace('<', '_') \
            .replace('>', '_') \
            .replace('|', '_')

    # Загрузка аудио-файла
    audio[-1].download(filename=f'{title}.mp4')

    # Отправка файла пользователю
    file = open(f'{title}.mp4', 'rb')
    bot.send_audio(message.chat.id, file, 'Держи твое аудио.')
    file.close()
    bot.register_next_step_handler(message, download_audio)

    # Удаление файла из хранилища
    os.unlink(f"{os.curdir}/{title}.mp4")

    bot.send_message(message.from_user.id,
                     "Чтобы перевести другое видео снова напиши /download")

if __name__ == '__main__':
    bot.infinity_polling()

