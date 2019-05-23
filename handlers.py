def start(bot, update):
    bot.chat_id = update.message.chat_id
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

    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sorry, but I can't summarise your text.")
