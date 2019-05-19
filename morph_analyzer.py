from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from diagbot import DiagBot
from telegram.utils.request import Request

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Hi. Send me any English text and I'll summarize it for you.")


def summarize(bot, update):
    try:
        # text = update.message.text
        text = 'Добрый день, мне вас Марфа Петровна посоветовала.' \
               ' У меня такая проблема, я страдаю от лихорадки, горло больное,' \
               ' а еще сухость в глазах и, чихаю очень часто.' \
               ' А еще в полнолуние правое ухо начинает чесаться. Доктор, что со мной?'
        bot.extract_symptoms(text)

        diag = bot.consult()

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=diag)
    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sorry, but I can't summarise your text.")


def main():
    request = Request(con_pool_size=8, proxy_url='http://144.217.160.173:3128')
    bot = DiagBot(token='',
                  request=request)
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    summarize_handler = MessageHandler(Filters.text, summarize)

    dispatcher.add_handler(summarize_handler)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':

    main()
