import io
import xlsxwriter
import pandas as pd
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
import asyncio
from telebot import types, asyncio_filters
from sql_lib import *
from vahta_api import get_vahta

bot = AsyncTeleBot("6620833655:AAE7CLZqNE1Za0bJD_C9mBV2iZXe2VqmGI0", state_storage=StateMemoryStorage())


class States_reg(StatesGroup):
    reg_1 = State()
    reg_2 = State()
    reg_3 = State()
    reg_4 = State()


class States_admin_menu(StatesGroup):
    send_all_nots = State()


class States_anon_mes(StatesGroup):
    anon_mes_1 = State()


@bot.message_handler(state=States_reg.reg_1)
async def reg_1(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваша кімната:')
    await bot.set_state(message.from_user.id, States_reg.reg_2, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_1'] = message.text


@bot.message_handler(state=States_reg.reg_2)
async def reg_2(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваш номер телефону:')
    await bot.set_state(message.from_user.id, States_reg.reg_3, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_2'] = message.text


@bot.message_handler(state=States_reg.reg_3)
async def reg_3(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваш тег телеграм:')
    await bot.set_state(message.from_user.id, States_reg.reg_4, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_3'] = message.text


@bot.message_handler(state=States_reg.reg_4)
async def reg_4(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        sql_query(query_ins_active(message.from_user.id, data['reg_1'], data['reg_2'], data['reg_3'], message.text))

    m_text = "Привіт!\nДякуємо за реєстрацію!\nТримай всю потрібну інформацію про гуртожиток №1"
    await bot.send_message(message.chat.id, m_text, reply_markup=create_menu())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def start_in_reg(message):
    await bot.send_message(message.chat.id, "Помилка регистрації, пройдіть регистрацію повторно")
    await bot.send_message(message.chat.id, "Ваш ПІБ:")
    await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)


async def too_many_in_reg(message):
    await bot.send_message(message.chat.id, "Ви ввели дуже багато символів, пройдіть регистрацію повторно")
    await bot.send_message(message.chat.id, "Ваш ПІБ:")
    await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)


@bot.message_handler(state=States_anon_mes.anon_mes_1)
async def anon_mes_1(message):
    if message.text == "Вихід":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Меню", reply_markup=create_menu())
        return

    sql_query(query_ins_anon_mes(message.text))
    await bot.send_message(message.chat.id, "Звернення збережено", reply_markup=create_menu())
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=States_admin_menu.send_all_nots, content_types=['document', 'audio', 'text', 'photo', 'video_note', 'voice', 'video', 'caption'])
async def send_all(message):
    if message.text == "Вихід":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Меню", reply_markup=create_menu())
        return

    if message.content_type == "photo":

        photo_id = message.photo[-1].file_id
        for i in sel_all_id():
            await bot.send_photo(i[0], photo_id, caption=message.caption)

    elif message.content_type == "audio":

        file_info = await bot.get_file(message.audio.file_id)
        file_path = file_info.file_path
        audio_bytes = await bot.download_file(file_path)

        for i in sel_all_id():
            await bot.send_audio(i[0], audio_bytes, caption=message.caption)

    elif message.content_type == "text":
        for i in sel_all_id():
            await bot.send_message(i[0], message.text)

    elif message.content_type == "video_note":
        for i in sel_all_id():
            await bot.send_video_note(i[0], message.video_note.file_id)

    elif message.content_type == "document":
        for i in sel_all_id():
            await bot.send_document(i[0], message.document.file_id, caption=message.caption)

    elif message.content_type == "voice":
        for i in sel_all_id():
            await bot.send_voice(i[0], message.voice.file_id, caption=message.caption)

    elif message.content_type == "video":
        for i in sel_all_id():
            await bot.send_video(i[0], message.video.file_id, caption=message.caption)

    else:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Не підтримується такий вид файлу", reply_markup=create_menu())
        return

    await bot.send_message(message.chat.id, "Повідомлення відправлено всім користувачам!", reply_markup=create_menu())


@bot.message_handler(commands=['start'])
async def send_welcome(message):

    is_a, ans = name_db(message.from_user.id)

    if not is_a:
        await bot.send_message(message.chat.id, "Ваш ПІБ:")
        await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)

    else:
        m_text = "Привіт, тримай всю потрібну інформацію про гуртожиток №1"
        await bot.send_message(message.chat.id, m_text, reply_markup=create_menu())
        return


def create_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Правила перебування в гуртожитку")
    item2 = types.KeyboardButton("Контакти адміністрації/студради гуртожитка")
    item3 = types.KeyboardButton("Хто сьогодні на вахті")
    item4 = types.KeyboardButton("Контакти старост поверхів")
    item5 = types.KeyboardButton("Про студраду гуртожитка")
    item6 = types.KeyboardButton("Анонімне звернення/пропозиція")
    item7 = types.KeyboardButton("Інше")
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    return markup


async def starostu_poverhiv(message):
    await bot.send_message(message.chat.id, "Незабаром буде відкритий конкурс на старост поверхів")


async def admin_srg_contact(message):
    await bot.send_message(message.chat.id, "Комендант гуртожитка - Ганна Петрівна:\n"
                                            "  - Телефон: +380 67 377 86 86\n"
                                            "  - Телеграм: @Anna_Metryuk\n"
                                            "\n"
                                            "Заступник коменданта гуртожитка - Копчалюк Мар'ян\n"
                                            "  - Телефон: +380 99 789 27 17\n"
                                            "  - Телеграм: @schooltoss\n"
                                            "\n"
                                            "Голова СРГ - Стахова Анастасія\n"
                                            "  - Телеграм: @aloneEEeT\n"
                                            "\n"
                                            "Заступник Голови СРГ - Лазоренко Євгеній\n"
                                            "  - Телеграм: @zRAMPAz")


async def hostel_rule(message):
    with open('rule.pdf', 'rb') as file:
        await bot.send_document(message.chat.id, file)


async def about_srg(message):
    await bot.send_message(message.chat.id, "Головна ціль студентської ради гуртожитку - зробити життя мешканців кращим\n"
                                            "Якщо Вам цікаве студентське самоврядування, ви завжди можете написати головам Департаментів\n"
                                            "Голова СРГ - @aloneEEeT\n"
                                            "Заступник - @zRAMPAz\n"
                                            "Санітарний стан - @fulcrum27\n"
                                            "Фінансовий департамент - @Vov4ik_25\n"
                                            "Юридичний департамент - @m1sha200_3\n"
                                            "Культурний департамент( ІвентДеп ) - @anddre_irving\n"
                                            "Інформаційний департамент - @zxculitka\n"
                                            "Департамент швидкого реагування - @sofiamedvediuk\n"
                                            "Патріотичний департамент - @tar_qwerty123456789\n"
                                            "Спортивний департамент - @Furzil\n"
                                            "\n"
                                            "Канал Студентської Ради Гуртожитку - @knudorm1\n")


async def something_else(message):
    await bot.send_message(message.chat.id, "Реквізити для оплати:\n"
                                            "https://t.me/srs_knu/1556 \n")
    await bot.send_message(message.chat.id, "Чат гуртожитку\n"
                                            "https://t.me/+SvRAMAY8d140YjYy")

async def anon_mes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вихід")
    markup.add(item1)

    await bot.send_message(message.chat.id, "Ваше звернення буде повністю анонімне\n"
                                            "Дані про відправника не зберігаються і не обробляються\n"
                                            "Введіть ваше звернення:", reply_markup=markup)

    await bot.set_state(message.from_user.id, States_anon_mes.anon_mes_1, message.chat.id)


async def vahta(message):
    await bot.send_message(message.chat.id, get_vahta())


async def export_exel(message):
    df1 = sql_query('SELECT * FROM active')

    output = io.BytesIO()

    # Создание DataFrame из полученных данных
    df1 = pd.DataFrame(df1,
                       columns=['ID_Користувача', 'ПІБ', 'Кімната', 'Телефон', 'Телеграм'])


    # Создание нового Excel-файла с помощью XlsxWriter
    workbook = xlsxwriter.Workbook(output)

    # Создание нового листа
    worksheet1 = workbook.add_worksheet('Інформація про мешканців')  # Создание листа для первой таблицы


    # Запись данных из DataFrame в лист
    worksheet1.write_row(0, 0, df1.columns)  # Запись заголовков столбцов для первой таблицы
    for i, row in enumerate(df1.values, start=1):  # Запись данных из каждой строки DataFrame для первой таблицы
        worksheet1.write_row(i, 0, row)

    # Закрытие книги
    workbook.close()

    # Перевод буфера в режим чтения
    output.seek(0)

    buffer = output
    await bot.send_document(message.chat.id, buffer, visible_file_name='Base.xlsx')


@bot.message_handler(content_types=['text'])
async def menu(message):
    if message.chat.type == 'private':
        is_a, _ = name_db(message.from_user.id)
        if is_a:
            if message.text == "Правила перебування в гуртожитку":  # +
                await hostel_rule(message)

            elif message.text == "Контакти адміністрації/студради гуртожитка":  # +
                await admin_srg_contact(message)

            elif message.text == "Хто сьогодні на вахті":
                await vahta(message)

            elif message.text == "Контакти старост поверхів":  # +
                await starostu_poverhiv(message)

            elif message.text == "Про студраду гуртожитка":  # +
                await about_srg(message)

            elif message.text == "Анонімне звернення/пропозиція":  # +
                await anon_mes(message)

            elif message.text == "Інше":  # +
                await something_else(message)

            elif message.text == "panel.admin.checker.1357999675":  # +
                await export_exel(message)

            elif message.text == "panel.admin.to_all.mes.55553334":  # +
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Вихід")
                markup.add(item1)

                await bot.send_message(message.chat.id, "Введіть текст: ", reply_markup=markup)
                await bot.set_state(message.from_user.id, States_admin_menu.send_all_nots, message.chat.id)

            else:
                await bot.send_message(message.chat.id, "Не вірний текст")
        else:
            await bot.send_message(message.chat.id, "Ви не зарегистровані, зверніться до @zRAMPAz")


bot.add_custom_filter(asyncio_filters.StateFilter(bot))


async def main():
    loop = asyncio.get_running_loop()
    await asyncio.gather(bot.polling(non_stop=True))

asyncio.run(main())
