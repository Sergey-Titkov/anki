#!/usr/local/bin/python
# coding: utf-8
import sqlite3
from datetime import datetime, date, time, timedelta

if __name__ == "__main__":
    # Создаем соединение с нашей базой данных
    # В нашем примере у нас это просто файл базы
    conn = sqlite3.connect('c:\\Users\\Sergey.Titkov\\Documents\\Anki\\1-й пользователь\\collection.anki2')

    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    # ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
    # КОД ДАЛЬНЕЙШИХ ПРИМЕРОВ ВСТАВЛЯТЬ В ЭТО МЕСТО

    # Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
    cursor.execute("""
        select count(distinct nid) as card from cards
        where did = 1461164719264
    """)
    results = cursor.fetchall()
    print('Карточек: {0}'.format(results[0][0]))
    print("")

    print("======= Неделя =============")
    cursor.execute("""
        select 
          strftime('%Y-%m-%d', round(id/1000/86400,0)*86400, 'unixepoch') date, 
          sum(time)/1000/60 spend_tine,
          sum(time)/1000/60/25 tomato
        from revlog 
        where (id/1000)>=CAST(strftime('%s', 'now', 'start of day', '-14 days') as decimal) 
        group by strftime('%W', round(id/1000/86400,0)*86400, 'unixepoch')
        order by id desc    
    """)

    # Получаем результат сделанного запроса
    results = cursor.fetchall()
    for row in results:
        dt = datetime.strptime(row[0], '%Y-%m-%d')
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        print('{0}-{1} {2}'.format(start.strftime('%d'), end.strftime('%d.%m.%Y'), row[2]))

    print("")
    print("======== Месяц ============")

    cursor.execute("""
        select 
          strftime('%m.%Y', round(id/1000), 'unixepoch') date, 
          sum(time)/1000/60 spend_tine,
          sum(time)/1000/60/25 tomato
        from revlog 
        where (id/1000)>=CAST(strftime('%s', 'now', 'start of day', '-60 days') as decimal) 
        group by strftime('%Y-%m', round(id/1000), 'unixepoch')
        order by id desc
    """)

    # Получаем результат сделанного запроса
    results = cursor.fetchall()
    for row in results:
        print('{0} {1}'.format(row[0], row[2]))

    conn.rollback()
    # Не забываем закрыть соединение с базой данных
    conn.close()

