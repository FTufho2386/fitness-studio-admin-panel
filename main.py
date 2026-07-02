from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from queries import (
    get_all_members,
    freeze_membership,
    disable_membership,
    book_workout,
    cancel_booking,
    add_new_member,
    update_member_profile,
    change_balance,
    show_workout_attendance
)

app = FastAPI(title='Fitness Club Administration')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/members')
def route_get_members():
    '''Получить список всех клиентов клуба'''
    members = get_all_members()
    return {'status': 'success', 'data': members}


@app.post('/members/add')
def route_add_member(name: str, phone_number: str, email: str):
    '''Добавить нового клиента (баланс по умолчанию 0)'''
    add_new_member(name, phone_number, email)
    return {'status': 'success', 'message': f'Клиент {name} успешно добавлен!'}


@app.post('/members/update')
def route_update_profile(member_id: int, name: str, phone_number: str, email: str):
    '''Обновить личные данные клиента по его ID'''
    update_member_profile(member_id, name, phone_number, email)
    return {'status': 'success', 'message': f'Профиль клиента с ID {member_id} успешно обновлен!'}


@app.post('/members/freeze')
def route_freeze_membership(member_id: int):
    '''Заморозить абонемент клиента'''
    freeze_membership(member_id)
    return {'status': 'success', 'message': f'Абонемент ID {member_id} заморожен.'}


@app.post('/members/disable')
def route_disable_membership(member_id: int):
    '''Заблокировать абонемент клиента'''
    disable_membership(member_id)
    return {'status': 'success', 'message': f'Абонемент ID {member_id} успешно деактивирован.'}


@app.post('/members/balance')
def route_change_balance(member_id: int, amount: int):
    '''Изменить баланс клиента (можно передавать как положительные, так и отрицательные числа)'''
    change_balance(amount, member_id)
    return {'status': 'success', 'message': f'Баланс клиента ID {member_id} изменен на {amount} руб.'}


@app.post('/bookings/book')
def route_book_workout(schedule_id: int, membership_id: int):
    '''Записать клиента на тренировку со списанием денег'''
    result = book_workout(schedule_id, membership_id)
    return result


@app.post('/bookings/cancel')
def route_cancel_booking(schedule_id: int, membership_id: int):
    '''Отменить запись клиента на тренировку'''
    cancel_booking(schedule_id, membership_id)
    return {'status': 'success', 'message': 'Запись на тренировку успешно отменена.'}


@app.get('/workouts/attendance')
def route_workout_attendance(schedule_id: int):
    '''Посмотреть список имён и телефонов клиентов, записанных на конкретную тренировку'''
    attendees = show_workout_attendance(schedule_id)
    return {'status': 'success', 'data': attendees}