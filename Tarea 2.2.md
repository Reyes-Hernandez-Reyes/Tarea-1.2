# ChatBot con Python y Telegram

# Evidencia
## Expresiones Regulares Utilizadas
Expresión regular para detectar saludos:    
   expresion_saludo = re.compile(r"hello|hi|hey|hola", re.IGNORECASE)

Expresión regular para validar el número de teléfono:   
   expresion_telefono = re.compile(r"^(55|77)\d{8}$")
   
## Captura 1
![Cap1](https://github.com/Reyes-Hernandez-Reyes/Tareas-Tema-2/assets/161515508/354b3f38-293d-48af-95c2-59a1db866863)


## Captura 2
![Cap2](https://github.com/Reyes-Hernandez-Reyes/Tareas-Tema-2/assets/161515508/7cfdef72-bb6c-48cd-86d7-7fab219ed1a8)


## Captura 3
## En la siguiente captura Esta la parte donde se utiliso la expresion para validar numero de Telefono y hasta que no se escriba correctamente el numero mandara un mensaje de EROOR  tanto no procedera a pedir el otro dato para concluir el registro
![Cap3](https://github.com/Reyes-Hernandez-Reyes/Tareas-Tema-2/assets/161515508/9f7c0c71-49f8-4eb7-afcf-95d1fdba59f1)


## Captura 4
![Cap4](https://github.com/Reyes-Hernandez-Reyes/Tareas-Tema-2/assets/161515508/016509ce-ab98-4957-abda-8b1a74aabfbe)

# CODIGO PYTHON

```python
import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters

# Habilitar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Estados del ConversationHandler
ASKING_NAME, ASKING_BIRTHDATE, ASKING_NATIONALITY, ASKING_STATE, ASKING_CITY, ASKING_PHONE, ASKING_EMAIL = range(7)

# Expresión regular para detectar saludos
expresion_saludo = re.compile(r"hello|hi|hey|hola", re.IGNORECASE)

# Expresión regular para validar el número de teléfono
expresion_telefono = re.compile(r"^(55|77)\d{8}$")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enviar un mensaje cuando se emite el comando /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola {user.mention_html()}! Bienvenido al proceso de preorden de la Cybertruck de Tesla. Por favor, saluda para comenzar el registro.",
        reply_markup=ForceReply(selective=True),
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enviar un mensaje cuando se emite el comando /help."""
    await update.message.reply_text("Este es el bot de ayuda para la preorden de la Cybertruck de Tesla. Saluda para comenzar el registro.")

# Iniciar registro
async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Iniciar el proceso de registro cuando el usuario saluda."""
    message_text = update.message.text
    if expresion_saludo.search(message_text):
        await update.message.reply_text("¡Hola! Comencemos con el registro de sus datos. Por favor, escriba su nombre completo empezando por sus apellidos.")
        return ASKING_NAME
    else:
        await update.message.reply_text("No entendí tu mensaje. Prueba diciendo 'hola' para comenzar.")
        return ConversationHandler.END

# fecha de nacimiento
async def ask_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """fecha de nacimiento."""
    context.user_data['nombre'] = update.message.text
    await update.message.reply_text("Gracias. Ahora, por favor, proporcione su fecha de nacimiento (DD/MM/AAAA).")
    return ASKING_BIRTHDATE

# nacionalidad
async def ask_nationality(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Pedir la nacionalidad."""
    context.user_data['fecha_nacimiento'] = update.message.text
    await update.message.reply_text("Perfecto. Ahora, ¿cuál es el Nombre de su Pais?")
    return ASKING_NATIONALITY

# estado
async def ask_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Pedir el estado de residencia."""
    context.user_data['nacionalidad'] = update.message.text
    await update.message.reply_text("Gracias. ¿En qué estado vive actualmente?")
    return ASKING_STATE

# Municipio
async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Pedir el municipio de residencia."""
    context.user_data['estado'] = update.message.text
    await update.message.reply_text("Muy bien. ¿Cuál es su municipio actual?")
    return ASKING_CITY

# Expresion regular para validar número de teléfono con e
def validar_telefono(telefono):
    """Validar que el número de teléfono tenga 10 dígitos y comience con 55 o 77."""
    if not expresion_telefono.match(telefono):
        if len(telefono) != 10:
            return "ERROR: Su número de teléfono solo consta de 10 dígitos y usted no cumple con esta regla."
        if not telefono.startswith(('55', '77')):
            return "Este número de teléfono no pertenece al país. Escriba de nuevo su número de teléfono."
    return None

# Teléfono
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Pedir el número de teléfono."""
    context.user_data['municipio'] = update.message.text
    await update.message.reply_text("Gracias. ¿Cuál es su número de teléfono de 10 dígitos?")
    return ASKING_PHONE

# Correo electrónico
async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Pedir el correo electrónico después de validar el número de teléfono."""
    telefono = update.message.text
    error_message = validar_telefono(telefono)
    if error_message:
        await update.message.reply_text(error_message)
        return ASKING_PHONE
    context.user_data['telefono'] = telefono
    await update.message.reply_text("Finalmente, por favor, proporcione su correo electrónico.")
    return ASKING_EMAIL

# Finalizar registro
async def end_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Finalizar el registro y agradecer al usuario."""
    context.user_data['correo'] = update.message.text
    await update.message.reply_text(
        "Muchas gracias por brindarnos su tiempo en recabar estos datos importantes para la preorden de su Cybertruck de Tesla. "
        "Estaremos en contacto con usted a través del correo electrónico que nos proporcionó."
    )
    return ConversationHandler.END

# Función principal
def main() -> None:
    """Iniciar el bot."""
    application = Application.builder().token(" EN ESTA PARTE VA EL TOKEN PROPORCIONADO POR TELEGRAM").build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Configurar ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, start_registration)],
        states={
            ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birthdate)],
            ASKING_BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_nationality)],
            ASKING_NATIONALITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_state)],
            ASKING_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            ASKING_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASKING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASKING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, end_registration)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # Iniciar el bot en modo polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

