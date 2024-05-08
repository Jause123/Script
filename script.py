from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

DATOS_PERSONALES = "https://api-ricardo.onrender.com/api/federador/"


def start(update, context):
    update.message.reply_text("Plantilla by t.me/Detergentess\n\nComando:\n/renaper [DNI] [M/F]")
    
def dni(update, context):
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Por favor, usa el formato /renaper [DNI] [M/F]")
            return

        dni_number = args[0]
        gender = args[1].upper()

        if gender == 'M':
            gender = 'MASCULINO'
        elif gender == 'F':
            gender = 'FEMENINO'
        else:
            update.message.reply_text("El género debe ser 'M' o 'F'")
            return

        datos_personales_url = f"{DATOS_PERSONALES}{dni_number}/{gender[0]}"
        response_datos_personales = requests.get(datos_personales_url)
        datos_personales_data = response_datos_personales.json()

        if "respuesta" in datos_personales_data:
            respuesta_datos_personales = datos_personales_data["respuesta"]
            if respuesta_datos_personales["codigoError"] == 200:
                datos_personales = ""
                for key, value in respuesta_datos_personales.items():
                    if value:
                        datos_personales += f"[+] {key.capitalize()}: {value}\n"
                update.message.reply_text(datos_personales)
            else:
                update.message.reply_text("Hubo un error al obtener los datos personales.")
                return
        else:
            update.message.reply_text("Hubo un error al obtener los datos personales.")
            return

        rostro_url = f"https://weblogin.muninqn.gov.ar/DataServerOK/webRenaper/{gender}/{gender[0]}{dni_number}.png"
        response_rostro = requests.get(rostro_url)

        if response_rostro.status_code == 200:
            update.message.reply_photo(rostro_url)
        else:
            update.message.reply_text("No se pudo obtener la imagen del DNI.")

def main():
    updater = Updater("7114720876:AAHeKloGKrxCAqoXxRaQOaHRE_vBDq46sBY", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('renaper', dni))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()