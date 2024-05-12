import telebot
from telebot import types
import test2


bot = test2.bot
TARGET_USER_CHAT_ID = test2.TARGET_USER_CHAT_ID

# Словарь для хранения выбранного языка для каждого пользователя
user_language = {}
choise = []
sending_message = []

def send_to_admin(message):
    # Сообщение об выбранных пользователем опциях
    bot.send_message(TARGET_USER_CHAT_ID , message)


@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    # Создаем инлайн-клавиатуру для выбора языка
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Crnogorski  🇲🇪', callback_data='montenegrin'))
    markup.add(types.InlineKeyboardButton('Српски 🇷🇸', callback_data='serbian'))
    markup.add(types.InlineKeyboardButton('English 🇺🇸', callback_data='english'))
    markup.add(types.InlineKeyboardButton('Русский 🇷🇺', callback_data='russian'))
    markup.add(types.InlineKeyboardButton('Deutsch 🇩🇪', callback_data='german'))
    markup.add(types.InlineKeyboardButton('Español 🇪🇸', callback_data='spanish'))
    markup.add(types.InlineKeyboardButton('Francus 🇫🇷', callback_data='francus'))
    markup.add(types.InlineKeyboardButton('Polski 🇵🇱', callback_data='polski'))

    # Отправляем сообщение с предложением выбрать язык
    bot.send_message(message.chat.id, f'Hello Mr/Ms {message.from_user.first_name} {message.from_user.last_name}\n'
                                      'Please choose your language', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global sending_message
    # Определяем действие пользователя по данным callback_data
    if call.data in ['english', 'russian', 'german', 'spanish', 'serbian', 'montenegrin', 'francus', 'polski']:
        # Сохраняем выбранный язык для пользователя
        user_language[call.message.chat.id] = call.data

        # Сообщаем пользователю о выбранном языке
        if call.data == 'english':
            bot.send_message(call.message.chat.id, 'You chose English!')
        elif call.data == 'russian':
            bot.send_message(call.message.chat.id, 'Вы выбрали русский!')
        elif call.data == 'german':
            bot.send_message(call.message.chat.id, 'Sie haben Deutsch gewählt!')
        elif call.data == 'spanish':
            bot.send_message(call.message.chat.id, '¡Has elegido español!')
        elif call.data == 'serbian':
            bot.send_message(call.message.chat.id, 'Izabrali ste srpski jezik!')
        elif call.data == 'montenegrin':
            bot.send_message(call.message.chat.id, 'Izabrali ste crnogorski!')
        elif call.data == 'francus':
            bot.send_message(call.message.chat.id, 'Vous avez choisi le français!')
        elif call.data == 'polski':
            bot.send_message(call.message.chat.id, 'Wybrałeś język polski!')

        # После выбора языка, предлагаем выбрать комнату
        room(call.message)
    elif call.data.startswith('room_'):
        lang = user_language.get(call.message.chat.id, 'english')
        # Пользователь выбрал номер комнаты
        if lang == 'english':
            bot.send_message(call.message.chat.id, f'You selected room {call.data}')
        elif lang == 'russian':
            bot.send_message(call.message.chat.id, f'Вы выбрали комнату {call.data}')
        elif lang == 'german':
            bot.send_message(call.message.chat.id, f'Sie haben Zimmer {call.data} ausgewählt')
        elif lang == 'spanish':
            bot.send_message(call.message.chat.id, f'Has seleccionado la habitación {call.data}')
        elif lang == 'serbian':
            bot.send_message(call.message.chat.id, f'Izabrali ste sobu {call.data}')
        elif lang == 'montenegrin':
            bot.send_message(call.message.chat.id, f'Izabrali ste sobu {call.data}')
        elif lang == 'francus':
            bot.send_message(call.message.chat.id, f'Vous avez sélectionné la chambre {call.data}')
        elif lang == 'polski':
            bot.send_message(call.message.chat.id, f'Wybrałeś pokój {call.data}')

        sending_message.append(call.data.split('_')[1])

        # Предлагаем выбрать проблему после выбора комнаты
        choose_problem(call.message)

    elif call.data == 'Клининг':
        clean(call)
    elif call.data == 'Техник':
        technical_problems(call)
    elif call.data == 'Ресепшн':
        reception(call)
    elif call.data == 'Сообщение':
        handle_special_query(call)

    elif call.data == 'new_order':
        main(call.message)

    if call.data != 'new_order' and not call.data.startswith('room_'):
        sending_message.append(call.data)

    if len(sending_message) > 3:
        send_to_admin(f'В комнату {sending_message[1]} нужно: Кто делает -  {sending_message[2]}, что нужно сделать - {sending_message[3]}')
        print(sending_message)
        sending_message = []
        one_more_time(call.message, user_language.get(call.message.chat.id, 'english'))


@bot.message_handler()
def one_more_time(message, language):
    thanks_messages = {
        'english': 'Thank you for your request, we will resolve your issue soon.',
        'russian': 'Спасибо за ваше обращение, мы решим вашу проблему в ближайшее время.',
        'german': 'Danke für Ihre Anfrage, wir werden Ihr Problem bald lösen.',
        'spanish': 'Gracias por su solicitud, resolveremos su problema pronto.',
        'serbian': 'Hvala na vašem zahtevu, rešićemo vaš problem uskoro.',
        'montenegrin': 'Hvala na vašem zahtevu, rešićemo vaš problem uskoro.',
        'french': 'Merci pour votre demande, nous résoudrons votre problème bientôt.',
        'polish': 'Dziękujemy za Twoje zgłoszenie, wkrótce rozwiążemy Twój problem.'
    }
    bot.send_message(message.chat.id,
                     thanks_messages.get(language, 'Thank you for your request, we will resolve your issue soon.'))

    button_texts = {
        'english': 'If you want to make a new request, press this button',
        'russian': 'Если вы хотите оставить новую заявку, нажмите эту кнопку',
        'german': 'Wenn Sie eine neue Anfrage stellen möchten, drücken Sie diese Taste',
        'spanish': 'Si quieres hacer una nueva solicitud, presiona este botón',
        'serbian': 'Ako želite da podnesete novi zahtev, pritisnite ovo dugme',
        'montenegrin': 'Ako želite podnijeti novi zahtjev, pritisnite ovo dugme',
        'french': 'Si vous voulez faire une nouvelle demande, appuyez sur ce bouton',
        'polish': 'Jeśli chcesz złożyć nowe zgłoszenie, naciśnij ten przycisk'
    }

    # Создание инлайн-клавиатуры и добавление кнопки с новым текстом
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('New',
                                   callback_data='new_order'))

    # Отправка сообщения с вопросом о новом запросе и клавиатурой
    bot.send_message(message.chat.id,
                     button_texts.get(language, 'If you want to make a new request, press this button'),
                     reply_markup=markup)


@bot.message_handler()
def room(message):
    # Создаем инлайн-клавиатуру для выбора номера комнаты
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('101', callback_data='room_101'),
        types.InlineKeyboardButton('102', callback_data='room_102'),
        types.InlineKeyboardButton('103', callback_data='room_103'),
        types.InlineKeyboardButton('104', callback_data='room_104')
    )

    # Этаж 2
    markup.row(
        types.InlineKeyboardButton('201', callback_data='room_201'),
        types.InlineKeyboardButton('202', callback_data='room_202'),
        types.InlineKeyboardButton('203', callback_data='room_203'),
        types.InlineKeyboardButton('204', callback_data='room_204')
    )

    # Этаж 3
    markup.row(
        types.InlineKeyboardButton('301', callback_data='room_301'),
        types.InlineKeyboardButton('302', callback_data='room_302'),
        types.InlineKeyboardButton('303', callback_data='room_303'),
        types.InlineKeyboardButton('304', callback_data='room_304')
    )

    # Этаж 4
    markup.row(
        types.InlineKeyboardButton('401', callback_data='room_401'),
        types.InlineKeyboardButton('402', callback_data='room_402'),
        types.InlineKeyboardButton('403', callback_data='room_403'),
        types.InlineKeyboardButton('404', callback_data='room_404')
    )

    # Этаж 5
    markup.row(
        types.InlineKeyboardButton('501', callback_data='room_501'),
        types.InlineKeyboardButton('502', callback_data='room_502'),
        types.InlineKeyboardButton('503', callback_data='room_503')
    )

    # Этаж 6
    markup.row(
        types.InlineKeyboardButton('601', callback_data='room_601'),
        types.InlineKeyboardButton('602', callback_data='room_602'),
        types.InlineKeyboardButton('603', callback_data='room_603')
    )

    # Получаем выбранный язык пользователя
    lang = user_language.get(message.chat.id, 'english')

    # Отправляем сообщение с предложением выбрать комнату на выбранном языке
    if lang == 'english':
        bot.send_message(message.chat.id, 'Please choose your room number:', reply_markup=markup)
    elif lang == 'russian':
        bot.send_message(message.chat.id, 'Пожалуйста, выберите номер вашей комнаты:', reply_markup=markup)
    elif lang == 'german':
        bot.send_message(message.chat.id, 'Bitte wählen Sie Ihre Zimmernummer:', reply_markup=markup)
    elif lang == 'spanish':
        bot.send_message(message.chat.id, 'Por favor, selecciona tu número de habitación:', reply_markup=markup)
    elif lang == 'serbian':
        bot.send_message(message.chat.id, 'Молимо вас да изаберете број своје собе:', reply_markup=markup)
    elif lang == 'montenegrin':
        bot.send_message(message.chat.id, 'Molimo izaberite broj svoje sobe:', reply_markup=markup)
    elif lang == 'francus':
        bot.send_message(message.chat.id, 'Veuillez choisir votre numéro de chambre:', reply_markup=markup)
    elif lang == 'polski':
        bot.send_message(message.chat.id, 'Proszę wybrać numer swojego pokoju:', reply_markup=markup)


@bot.message_handler()
def choose_problem(message):
    # Получаем выбранный язык пользователя
    lang = user_language.get(message.chat.id, 'english')

    # Создаем инлайн-клавиатуру для выбора проблемы
    markup = types.InlineKeyboardMarkup()

    # В зависимости от языка пользователя, добавляем соответствующие варианты и сообщения
    if lang == 'english':
        markup.add(types.InlineKeyboardButton('Room cleaning', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Technical problems', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('General issues - reception', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('I want to describe the issue myself', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Please choose your issue:', reply_markup=markup)

    elif lang == 'russian':
        markup.add(types.InlineKeyboardButton('Уборка номера', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Технические проблемы', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Общие вопросы - ресепшн', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Хочу описать проблему самостоятельно', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Пожалуйста, выберите ваш вопрос:', reply_markup=markup)

    elif lang == 'german':
        markup.add(types.InlineKeyboardButton('Zimmerreinigung', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Technische Probleme', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Allgemeine Fragen - Rezeption', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Ich möchte das Problem selbst beschreiben', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Bitte wählen Sie Ihr Problem:', reply_markup=markup)

    elif lang == 'spanish':
        markup.add(types.InlineKeyboardButton('Limpieza de habitación', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Problemas técnicos', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Asuntos generales - recepción', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Quiero describir el problema yo mismo', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Por favor, elige tu pregunta:', reply_markup=markup)

    elif lang == 'serbian':
        markup.add(types.InlineKeyboardButton('Чишћење собе', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Технички проблеми', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Општа питања - рецепција', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Желим сам описати проблем', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Молимо изаберите ваш проблем:', reply_markup=markup)

    elif lang == 'montenegrin':
        markup.add(types.InlineKeyboardButton('Čišćenje sobe', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Tehnički problemi', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Opšta pitanja - recepcija', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Želim sam opisati problem', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Molimo izaberite vaš problem:', reply_markup=markup)

    elif lang == 'francus':
        markup.add(types.InlineKeyboardButton('Nettoyage de chambre', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Problèmes techniques', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Questions générales - réception', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Je veux décrire le problème moi-même', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Veuillez choisir votre question:', reply_markup=markup)

    elif lang == 'polski':
        markup.add(types.InlineKeyboardButton('Sprzątanie pokoju', callback_data='Клининг'))
        markup.add(types.InlineKeyboardButton('Problemy techniczne', callback_data='Техник'))
        markup.add(types.InlineKeyboardButton('Ogólne pytania - recepcja', callback_data='Ресепшн'))
        markup.add(types.InlineKeyboardButton('Chcę opisać problem samodzielnie', callback_data='Сообщение'))
        bot.send_message(message.chat.id, 'Proszę wybrać swoje pytanie:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Клининг')
def clean(call):
    chat_id = call.message.chat.id
    # Создаем инлайн-клавиатуру для вариантов уборки номера
    markup = types.InlineKeyboardMarkup()

    # Получаем выбранный язык пользователя
    lang = user_language.get(chat_id, 'english')

    # В зависимости от языка, предлагаем различные опции уборки номера и соответствующие сообщения
    if lang == 'english':
        markup.add(types.InlineKeyboardButton('Clean the room', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Change bed linen', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Please choose a cleaning option:', reply_markup=markup)

    elif lang == 'russian':
        markup.add(types.InlineKeyboardButton('Убраться в номере', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Сменить белье', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Выберите опцию уборки номера:', reply_markup=markup)

    elif lang == 'german':
        markup.add(types.InlineKeyboardButton('Zimmer reinigen', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Bettwäsche wechseln', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Bitte wählen Sie eine Reinigungsoption:', reply_markup=markup)

    elif lang == 'spanish':
        markup.add(types.InlineKeyboardButton('Limpiar la habitación', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Cambiar la ropa de cama', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Por favor, elige una opción de limpieza:', reply_markup=markup)

    elif lang == 'serbian':
        markup.add(types.InlineKeyboardButton('Очистите собу', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Промените постељину', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Изаберите опцију чишћења собе:', reply_markup=markup)

    elif lang == 'montenegrin':
        markup.add(types.InlineKeyboardButton('Očistiti sobu', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Promijeniti posteljinu', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Molimo vas da izaberete opciju čišćenja sobe:', reply_markup=markup)

    elif lang == 'francus':
        markup.add(types.InlineKeyboardButton('Nettoyer la chambre', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Changer les draps', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Veuillez choisir une option de nettoyage:', reply_markup=markup)

    elif lang == 'polski':
        markup.add(types.InlineKeyboardButton('Wyczyścić pokój', callback_data='Убраться в номере'))
        markup.add(types.InlineKeyboardButton('Zmień pościel', callback_data='Сменить белье'))
        bot.send_message(chat_id, 'Proszę wybrać opcję czyszczenia:', reply_markup=markup)


# Обработчик для технических проблем
@bot.callback_query_handler(func=lambda call: call.data == 'Техник')
def technical_problems(call):
    chat_id = call.message.chat.id
    # Создание инлайн-клавиатуры для вариантов технических проблем
    markup = types.InlineKeyboardMarkup()

    # Получаем выбранный язык пользователя
    lang = user_language.get(chat_id, 'english')

    # В зависимости от языка, предлагаем различные опции технических проблем и соответствующие сообщения
    if lang == 'english':
        markup.add(types.InlineKeyboardButton('Lights not working', callback_data='Lights not working'))
        markup.add(types.InlineKeyboardButton('Door not opening', callback_data='Door not opening'))
        markup.add(types.InlineKeyboardButton('No water', callback_data='No water'))
        markup.add(types.InlineKeyboardButton('Air conditioner not working', callback_data='Air conditioner not working'))
        bot.send_message(chat_id, 'Please choose the technical issue:', reply_markup=markup)

    elif lang == 'russian':
        markup.add(types.InlineKeyboardButton('Не работает свет', callback_data='Не работает свет'))
        markup.add(types.InlineKeyboardButton('Не открывается дверь', callback_data='Не открывается дверь'))
        markup.add(types.InlineKeyboardButton('Нет воды', callback_data='Нет воды'))
        markup.add(types.InlineKeyboardButton('Не работает кондиционер', callback_data='Не работает кондиционер'))
        bot.send_message(chat_id, 'Выберите техническую проблему:', reply_markup=markup)

    elif lang == 'german':
        markup.add(types.InlineKeyboardButton('Licht funktioniert nicht', callback_data='Licht funktioniert nicht'))
        markup.add(types.InlineKeyboardButton('Tür öffnet sich nicht', callback_data='Tür öffnet sich nicht'))
        markup.add(types.InlineKeyboardButton('Wasser fehlt', callback_data='Wasser fehlt'))
        markup.add(types.InlineKeyboardButton('Klimaanlage funktioniert nicht',
                                              callback_data='Klimaanlage funktioniert nicht'))
        bot.send_message(chat_id, 'Bitte wählen Sie das technische Problem:', reply_markup=markup)

    elif lang == 'spanish':
        markup.add(types.InlineKeyboardButton('No funciona la luz', callback_data='No funciona la luz'))
        markup.add(types.InlineKeyboardButton('No se abre la puerta', callback_data='No se abre la puerta'))
        markup.add(types.InlineKeyboardButton('No hay agua', callback_data='No hay agua'))
        markup.add(types.InlineKeyboardButton('No funciona el aire acondicionado',
                                              callback_data='No funciona el aire acondicionado'))
        bot.send_message(chat_id, 'Por favor, elige el problema técnico:', reply_markup=markup)

    elif lang == 'serbian':
        markup.add(types.InlineKeyboardButton('Не ради свет', callback_data='Не ради свет'))
        markup.add(types.InlineKeyboardButton('Не отвара се врата', callback_data='Не отвара се врата'))
        markup.add(types.InlineKeyboardButton('Нема воде', callback_data='Нема воде'))
        markup.add(types.InlineKeyboardButton('Не ради клима уређај', callback_data='Не ради клима уређај'))
        bot.send_message(chat_id, 'Изаберите технички проблем:', reply_markup=markup)

    elif lang == 'montenegrin':
        markup.add(types.InlineKeyboardButton('Ne radi svjetlo', callback_data='Ne radi svjetlo'))
        markup.add(types.InlineKeyboardButton('Vrata se ne otvaraju', callback_data='Vrata se ne otvaraju'))
        markup.add(types.InlineKeyboardButton('Nema vode', callback_data='Nema vode'))
        markup.add(types.InlineKeyboardButton('Ne radi klima uređaj', callback_data='Ne radi klima uređaj'))
        bot.send_message(chat_id, 'Molimo izaberite tehnički problem:', reply_markup=markup)

    elif lang == 'francus':

        markup.add(types.InlineKeyboardButton('La lumière ne fonctionne pas', callback_data='La lumière ne fonctionne pas'))
        markup.add(types.InlineKeyboardButton('La porte ne s\'ouvre pas', callback_data='La porte ne s\'ouvre pas'))
        markup.add(types.InlineKeyboardButton('Pas d\'eau', callback_data='Pas d\'eau'))
        markup.add(types.InlineKeyboardButton('Le climatiseur ne fonctionne pas',
                                              callback_data='Le climatiseur ne fonctionne pas'))
        bot.send_message(chat_id, 'Veuillez choisir le problème technique:', reply_markup=markup)

    elif lang == 'polski':
        markup.add(types.InlineKeyboardButton('Światło nie działa', callback_data='Światło nie działa'))
        markup.add(types.InlineKeyboardButton('Drzwi się nie otwierają', callback_data='Drzwi się nie otwierają'))
        markup.add(types.InlineKeyboardButton('Brak wody', callback_data='Brak wody'))
        markup.add(types.InlineKeyboardButton('Klimatyzacja nie działa', callback_data='Klimatyzacja nie działa'))
        bot.send_message(chat_id, 'Proszę wybrać problem techniczny:', reply_markup=markup)


# Обработчик для общих проблем
@bot.callback_query_handler(func=lambda call: call.data == 'Ресепшн')
def reception(call):
    chat_id = call.message.chat.id
    # Создаем инлайн-клавиатуру для вариантов общих проблем
    markup = types.InlineKeyboardMarkup()

    # Получаем выбранный язык пользователя
    lang = user_language.get(chat_id, 'english')

    # В зависимости от языка, предлагаем варианты и сообщения
    if lang == 'english':
        markup.add(types.InlineKeyboardButton('Call a taxi', callback_data='Вызвать такси'))
        markup.add(types.InlineKeyboardButton('Please come to the room', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Please choose your option:', reply_markup=markup)

    elif lang == 'russian':
        markup.add(types.InlineKeyboardButton('Вызвать такси', callback_data='Вызвать такси'))
        markup.add(
            types.InlineKeyboardButton('Подойдите пожалуйста в номер', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Пожалуйста, выберите ваш вариант:', reply_markup=markup)

    elif lang == 'german':
        markup.add(types.InlineKeyboardButton('Taxi rufen', callback_data='Вызвать такси'))
        markup.add(
            types.InlineKeyboardButton('Bitte kommen Sie ins Zimmer', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Bitte wählen Sie Ihre Option:', reply_markup=markup)

    elif lang == 'spanish':
        markup.add(types.InlineKeyboardButton('Llamar a un taxi', callback_data='Вызвать такси'))
        markup.add(types.InlineKeyboardButton('Por favor, ven a la habitación',
                                              callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Por favor, elige tu opción:', reply_markup=markup)

    elif lang == 'serbian':
        markup.add(types.InlineKeyboardButton('Позвати такси', callback_data='Вызвать такси'))
        markup.add(types.InlineKeyboardButton('Молимо вас дођите до собе', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Молимо вас да изаберете своју опцију:', reply_markup=markup)

    elif lang == 'montenegrin':
        markup.add(types.InlineKeyboardButton('Pozvati taksi', callback_data='Вызвать такси'))
        markup.add(
            types.InlineKeyboardButton('Molimo vas da dođete do sobe', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Molimo vas izaberite vašu opciju:', reply_markup=markup)

    elif lang == 'francus':
        markup.add(types.InlineKeyboardButton('Appeler un taxi', callback_data='Вызвать такси'))
        markup.add(types.InlineKeyboardButton('S\'il vous plaît, venez à la chambre',
                                              callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Veuillez choisir votre option:', reply_markup=markup)

    elif lang == 'polski':
        markup.add(types.InlineKeyboardButton('Wezwać taksówkę', callback_data='Вызвать такси'))
        markup.add(types.InlineKeyboardButton('Proszę przyjdź do pokoju', callback_data='Подойдите пожалуйста в номер'))
        bot.send_message(chat_id, 'Proszę wybrać swoją opcję:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Сообщение')
def handle_special_query(call):
    chat_id = call.message.chat.id
    # Получаем выбранный язык пользователя
    lang = user_language.get(chat_id, 'english')

    # Предлагаем пользователю самостоятельно описать свою проблему на выбранном языке
    if lang == 'english':
        bot.send_message(chat_id, 'Please describe your issue:')
    elif lang == 'russian':
        bot.send_message(chat_id, 'Опишите свою проблему самостоятельно:')
    elif lang == 'german':
        bot.send_message(chat_id, 'Bitte beschreiben Sie Ihr Problem selbst:')
    elif lang == 'spanish':
        bot.send_message(chat_id, 'Por favor, describe tu problema:')
    elif lang == 'serbian':
        bot.send_message(chat_id, 'Молимо вас да сами опишете свој проблем:')
    elif lang == 'montenegrin':
        bot.send_message(chat_id, 'Molimo vas da sami opišete svoj problem:')
    elif lang == 'francus':
        bot.send_message(chat_id, 'Veuillez décrire votre problème vous-même:')
    elif lang == 'polski':
        bot.send_message(chat_id, 'Proszę opisać swój problem samodzielnie:')

    # Регистрируем следующий шаг для обработки ввода текста от пользователя
    bot.register_next_step_handler(call.message, process_user_message)


# Функция для обработки ввода текста от пользователя
def process_user_message(message):
    global client_message
    chat_id = message.chat.id
    # Получаем текст, введенный пользователем
    user_input = message.text

    # Получаем выбранный язык пользователя
    lang = user_language.get(chat_id, 'english')

    # Подтверждаем получение сообщения пользователя на его языке
    if lang == 'english':
        bot.send_message(chat_id, 'Your message has been received and recorded.')
    elif lang == 'russian':
        bot.send_message(chat_id, 'Ваше сообщение было принято и записано.')
    elif lang == 'german':
        bot.send_message(chat_id, 'Ihre Nachricht wurde empfangen und aufgezeichnet.')
    elif lang == 'spanish':
        bot.send_message(chat_id, 'Tu mensaje ha sido recibido y registrado.')
    elif lang == 'serbian':
        bot.send_message(chat_id, 'Ваша порука је примљена и забележена.')
    elif lang == 'montenegrin':
        bot.send_message(chat_id, 'Vaša poruka je primljena i zabeležena.')
    elif lang == 'francus':
        bot.send_message(chat_id, 'Votre message a été reçu et enregistré.')
    elif lang == 'polski':
        bot.send_message(chat_id, 'Twoja wiadomość została otrzymana i zarejestrowana.')

    # Отправляем введенное пользователем сообщение администратору (используем функцию send_to_admin)
    send_to_admin(user_input)
    global sending_message
    sending_message.append(user_input)
    if len(sending_message) > 3:
        send_to_admin(f'Из комнаты {sending_message[1]} пришло сообщение  : {sending_message[3]}')

        sending_message = []
        one_more_time(message, lang)


bot.polling(non_stop=True)