# support_bot
Коммандный проект по созданию бота поддержки

## Установка

1) Клонировать проект:
```
git clone https://github.com/Rikoze777/support_bot.git
```

2) Установить зависимости:
```
pip install -r requiremenets.txt
```

3) Создать `.env` файл для ваших секретных ключей:
```
touch .env
```

4) Записать в .env следующие переменные:
* TG_TOKEN='Ваш телеграм токен'  [Получают при создании у отца ботов](https://t.me/botfather)
* USER_ID='ID вашей личной страницы Telegram' [узнать можно тут](https://t.me/username_to_id_bot)

5) Создать файл БД `support.db`:
```
touch support.db
```

6) Для заполнения бд таблицами выполните команду
```
python3 create_tables.py
```


## Запуск бота
* Telegram бот
```
python3 bot.py
```