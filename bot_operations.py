import phonenumbers
import sqlite3


db = sqlite3.connect('support.db')


def validate_phonenumber(number):
    try:
        parsed_number = phonenumbers.parse(number, 'RU')
        return phonenumbers.is_valid_number_for_region(parsed_number, 'RU')
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def is_new_user(number):
    sql = 'SELECT EXISTS (SELECT 1 FROM users WHERE number = ?)'
    db.execute(sql, (number,))
    return db.fetchone()[0]


def save_user(number):
    cursor = db.cursor()
    cursor.execute(f"insert into users(number) values ({number})")
    db.commit()
    db.close()
