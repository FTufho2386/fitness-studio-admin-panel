from database import get_connect


def execute_query(sql_query, params=None, is_select=True):
    conn = get_connect()
    if not conn:
        return []

    result = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)
            if is_select:
                result = cursor.fetchall()
            else:
                conn.commit()

    except Exception as e:
        print(f'Ошибка выполнения запроса {e}')
        return []

    finally:
        conn.close()

    return result


def get_all_members():
    return execute_query('SELECT id, name, phone_number, email, balance FROM members;')


def freeze_membership(membership_id):
    sql_query = ('UPDATE memberships SET is_frozen = TRUE WHERE id = %s')
    execute_query(sql_query, (membership_id,), is_select=False)


def disable_membership(membership_id):
    sql_query = ('UPDATE memberships SET is_active = FALSE WHERE id = %s;')
    execute_query(sql_query, (membership_id,), is_select=False)


def book_workout(schedule_id, membership_id):
    sql_member = '''
        SELECT m.id, m.balance 
        FROM members m
        JOIN memberships ms ON ms.member_id = m.id
        WHERE ms.id = %s;
    '''
    member_data = execute_query(sql_member, (membership_id,))

    if not member_data:
        return {'status': 'error', 'message': 'Абонемент или клиент не найден!'}

    member_id = member_data[0][0]  # Настоящий ID клиента
    current_balance = member_data[0][1]  # Его баланс

    price_data = execute_query('SELECT price FROM schedule WHERE id = %s;', (schedule_id,))
    if not price_data:
        return {'status': 'error', 'message': 'Занятие не найдено!'}
    workout_price = price_data[0][0]

    if current_balance >= workout_price:
        execute_query('UPDATE members SET balance = balance - %s WHERE id = %s;', (workout_price, member_id))

        execute_query('INSERT INTO workout_bookings (schedule_id, membership_id) VALUES (%s, %s);',
                      (schedule_id, membership_id))

        return {'status': 'success', 'message': 'Запись прошла успешно, деньги списаны!'}
    else:
        return {'status': 'error', 'message': 'Недостаточно денег на балансе!'}


def cancel_booking(schedule_id, membership_id):
    sql_query = ('DELETE FROM workout_bookings WHERE schedule_id = %s AND membership_id = %s;')
    execute_query(sql_query, (schedule_id, membership_id), is_select=False)


def add_new_member(name, phone_number, email):
    sql_query = ('INSERT INTO members (name, phone_number, email) VALUES (%s, %s, %s);')
    execute_query(sql_query, (name, phone_number, email), is_select=False)


def update_member_profile(member_id, name, phone_number, email):
    sql_query = '''UPDATE members SET name = %s, phone_number = %s, email = %s where id = %s'''
    execute_query(sql_query, (name, phone_number, email, member_id), is_select=False)


def change_balance(amount, member_id):
    sql_query = ('UPDATE members set balance = balance + %s WHERE id = %s')
    execute_query(sql_query, (amount, member_id), is_select=False)


def show_workout_attendance(schedule_id):
    sql_query = '''
    SELECT m.name, m.phone_number, m.email
    FROM workout_bookings wb
    JOIN memberships ms ON wb.membership_id = ms.id
    JOIN members m ON ms.member_id = m.id
    WHERE wb.schedule_id = %s;
    '''
    return execute_query(sql_query, (schedule_id,))


if __name__ == '__main__':
    add_new_member('Петр Петров', '+79995554433', 'petrov@mail.ru')
    all_members = get_all_members()
    for member in all_members:
        print(member)