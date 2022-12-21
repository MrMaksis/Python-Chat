#Program name: Python chat; Version: 1.0; Auther: vk.com/mr_maksis, youtube.com/HowdyhoNet

import asyncio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

chat_msgs = []                                                                                                           #Объявления массива сообщений
online_users = set()                                                                                                     #Объявления множества, сообщений

MAX_MESSAGES_COUNT = 100                                                                                                 #Максимальное количество сообщений в чате

async def main():
    global chat_msgs                                                                                                     #Присваиваем модификатор доступа к переменной массива сообщений
    
    put_markdown("## 🧊 Добро пожаловать в онлайн чат!\nИсходный код данного чата укладывается в 100 строк кода!")      #Форматированный текст markDown

    msg_box = output()                                                                                                   #Присваиваем глобальному массиву сообщений, функцию вывода сообщений

    put_scrollable(msg_box, height=300, keep_bottom=True)                                                                #Задаем область прокручивания по вертикали

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя", validate=lambda n:                      #Создаем переменную ника, и базовую проверку на существование
    "Такой ник уже используется!" if n in online_users or n == '📢' else None)

    online_users.add(nickname)                                                                                           #Добавляем ник в множество

    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!'))                                                     #Добавление сообщения в чат
    msg_box.append(put_markdown(f'📢 `{nickname}` присоединился к чату'))

    refresh_task = run_async(refresh_msg(nickname, msg_box))                                                            #Создаем переменную и записываем туда результат асинхронного метода

    while True:
        data = await input_group("💭 Новое сообщение", [                                                                #Создаем переменную и помещаем туда элементы управления 
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate = lambda m: ('msg', "Введите текст сообщения!") 
        if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:                                                                                                #Проверка на пустоту (если сообщение пустое, прерывается соединение с сервером)
            break

        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))                                                    #Добавление финального сообщения пользователя в чат
        chat_msgs.append((nickname, data['msg']))                                                                       #Также присваиваем значение финального сообщения в множество 

    refresh_task.close()                                                                                                #Закрываем асинхронный метод

    online_users.remove(nickname)                                                                                       #Удаление пользователя из множества (если он покинул чат)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))                                         #Вывод сообщение в чат
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))                                                #Сохранения сообщения в множество

    put_buttons(['Перезайти'], onclick=lambda btn:run_js('window.location.reload()'))                                  #Создания кнопки перезагрузки страницы

async def refresh_msg(nickname, msg_box):                                                                              #Метод обновления сообщений
    global chat_msgs                                                                                                   #Присваиваем модификатор доступа к переменной массива сообщений
    last_idx = len(chat_msgs)                                                                                          #Запись длины чата

    while True:                                                                                                        #Цикл обновления сообщений у других пользователей
        await asyncio.sleep(1)
        
        for m in chat_msgs[last_idx:]:                                                                                #Цикл обновления сообщений у других пользователей
            if m[0] != nickname:                                                                                      #Проверка на валидность пользователя
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))                                                     #Вывод сообщения в чат
        
        
        if len(chat_msgs) > MAX_MESSAGES_COUNT:                                                                       #Удаление неактуальных сообщений
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]
        
        last_idx = len(chat_msgs)                                                                                     #Присвоить индекс последнего сообщения

if __name__ == "__main__":                                                                                            #Запуск веб-сервера
    start_server(main, debug=True, port=8080, cdn=False)