import telebot

CHAVE_API = "7296023269:AAHpuNynWBaNdSJDLtWauRwJhDQMn83eNHU"

bot = telebot.TeleBot(CHAVE_API)

def verificar(mensagem):
        return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    bot.reply_to(mensagem, "Olá, esse é um teste do bot")

bot.polling()