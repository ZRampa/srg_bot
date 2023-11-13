import sqlite3


def query_sel_all_id():
    query = f"SELECT user_id FROM active;"
    return query


def query_name_db(user_id):
    query = f"SELECT * FROM active WHERE user_id = '{user_id}';"
    return query


def sel_all_id():
    ans = sql_query(query_sel_all_id())
    return ans


def query_ins_active(user_id, full_name, room, phone, telegram_tag):
    query = f"INSERT INTO active VALUES ('{user_id}', '{full_name}', '{room}', '{phone}', '{telegram_tag}');"
    return query


def query_ins_anon_mes(message):
    query = f"INSERT INTO anon_mes VALUES ('{message}');"
    return query


def name_db(user_id):
    ans = sql_query(query_name_db(user_id))
    if len(ans) > 0:
        return True, ans
    else:
        return False, ans


def sql_query(query):
    conn = sqlite3.connect('SRG_TELEBOT.db')
    cursor = conn.cursor()

    ans = cursor.execute(query)
    ans = ans.fetchall()

    conn.commit()
    conn.close()

    return ans

