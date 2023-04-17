import streamlit as st
import database as db
import mongo as mongo_db
import pandas as pd
import numpy as np
import datetime

import config
from client import Client
from worker import Worker
from application import Application

db_connection = db.create_connection()


def entry_user(login, password):
    client = db.select_client(db_connection, login, password)
    worker = db.select_worker(db_connection, login, password)
    if client:
        return 'client'
    elif worker:
        if worker[0][1] == 2:
            return 'brigadier'
        elif worker[0][1] == 3:
            return 'operator'
        else:
            return 'admin'
    else:
        return None


def main_page():
    # db.create_db_tables(db_connection)
    tab1, tab2 = st.tabs(['Вход', 'Регистрация'])
    with tab1:
        st.header('Вход в аккаунт')
        login = st.text_input("Логин")
        password = st.text_input("Пароль", type='password')
        entry_btn = st.checkbox('Войти')
        if entry_btn:
            menu = entry_user(login, password)
            if menu is None:
                st.error('Вы ввели неправильные данные')
            elif menu == 'client':
                st.title("Меню клиента")
                client_id = db.select_client_id(db_connection, login, password)
                reply_types = ['По телефону', 'По почте']
                urgency_names = ['Срочно', 'В течение дня', 'На этой неделе']
                services = db.select_services(db_connection)
                service_names = [x[1] for x in services]
                foundations = mongo_db.foundations.find({})
                fences = mongo_db.fences.find({})
                houses = mongo_db.houses.find({})
                application_data = ''
                service_choice = st.selectbox('Выберите интересующую услугу', service_names)
                if service_choice == service_names[0]:
                    service_choice_id = 1
                    fundament_choice = st.selectbox('Выберите тип фундамента', [x['name'] for x in foundations])
                    application_data = 'Тип фундамента: ' + fundament_choice
                elif service_choice == service_names[1]:
                    service_choice_id = 2
                    fence_choice = st.selectbox('Выберите тип забора', [x['name'] for x in fences])
                    fence_length = st.slider('Выберите длину забора', 0, 300)
                    application_data = 'Длина забора: ' + str(fence_length) + ', тип забора: ' + fence_choice
                elif service_choice == service_names[2]:
                    service_choice_id = 3
                    house_choice = st.selectbox('Выберите дом', [x['name'] for x in houses])
                    house_square = st.slider('Выберите размер дома', 0, 300)
                    application_data = 'Название дома: ' + house_choice + ', размер дома: ' + str(house_square)
                reply_type = st.radio('Способ обратной связи', reply_types)
                urgency_choice = st.selectbox('Как быстро с вами связаться', urgency_names)

                if urgency_choice == urgency_names[0]:
                    urgency_choice_id = 1
                elif urgency_choice == urgency_names[1]:
                    urgency_choice_id = 2
                else:
                    urgency_choice_id = 3

                if reply_type == reply_types[0]:
                    reply_type_id = 1
                elif reply_type == reply_types[1]:
                    reply_type_id = 2

                request_feedback = st.button('Оставить заявку')
                if request_feedback:
                    new_application = Application(client_id[0], 1, reply_type_id, urgency_choice_id,
                                                  service_choice_id, application_data, datetime.date.today())
                    db.insert_application(db_connection, new_application)
                    st.success('Заявка успешно создана')
            elif menu == 'brigadier':
                st.title("Меню бригадира")
            elif menu == 'operator':
                st.title("Меню оператора")
                applications = db.select_applications(db_connection)
                applications = sorted(applications, key=lambda application: application[4])
                df_appls = pd.DataFrame(applications, columns=['id', 'client_id', 'application_status_id',
                                                                      'reply_type_id', 'urgency_id', 'service_id',
                                                                      'application_data', 'date'])
                df_appls = df_appls.drop(['client_id'], axis=1)
                df_appls['application_status_id'] = df_appls['application_status_id'].map(
                    {1: 'Заявка активна', 2: 'Обработка заявки', 3: 'Обслужена'})
                df_appls['reply_type_id'] = df_appls['reply_type_id'].map(
                    {1: 'По телефону', 2: 'По почте'})
                df_appls['urgency_id'] = df_appls['urgency_id'].map(
                    {1: 'Срочно', 2: 'В течение дня', 3: 'На этой неделе'})
                df_appls['service_id'] = df_appls['service_id'].map(
                    {1: 'Изготовление фундамента', 2: 'Установка забора', 3: 'Стоительство дома'})
                status_choices = st.selectbox('Статус заявки', ['Заявка активна', 'Обработка заявки', 'Обслужена'])
                if status_choices == 'Заявка активна':
                    df_table_appls = df_appls[df_appls['application_status_id'] == 'Заявка активна']
                elif status_choices == 'Обработка заявки':
                    df_table_appls = df_appls[df_appls['application_status_id'] == 'Обработка заявки']
                elif status_choices == 'Обслужена':
                    df_table_appls = df_appls[df_appls['application_status_id'] == 'Обслужена']
                st.table(df_table_appls)
                df_appls_id = sorted(df_table_appls['id'].tolist())
                st.button('Обновить таблицу')
                col1, col2 = st.columns(2)
                with col1:
                    appl_choosed = st.selectbox('Выберите id заявки', df_appls_id)
                    if st.button('Обработать заявку'):
                        db.set_application_status(db_connection, int(appl_choosed), int(2))
                    if st.button('Завершить обработку заявки'):
                        db.set_application_status(db_connection, int(appl_choosed), int(3))
                    if st.button('Удалить заявка'):
                        db.delete_application(db_connection, int(appl_choosed))
                with col2:
                    client_id = 0
                    choice = appl_choosed
                    for appl in applications:
                        if appl[0] == choice:
                            client_id = appl[1]
                    client_info = db.select_client_by_id(db_connection, client_id)
                    df_client_info = pd.DataFrame(client_info, columns=['id', 'name', 'surname', 'email', 'phone',
                                                                        'login', 'password'])
                    df_client_info = df_client_info.drop(['id', 'login', 'password'], axis=1)
                    df_client_info = df_client_info.transpose()
                    st.table(df_client_info)

            elif menu == 'admin':
                st.title("Меню Админа")
                choice = st.selectbox('Выберите таблицу с данными', ['Applications', 'Works', 'Clients', 'Workers',
                                                                     'Services', 'Materials', 'Wall_materials',
                                                                     'Foundations', 'Houses', 'Fences', 'Suppliers'])
                if choice == 'Applications':
                    applications = db.select_applications(db_connection)
                    df = pd.DataFrame(applications, columns=['id', 'client_id', 'application_status_id',
                                                             'reply_type_id', 'urgency_id', 'service_id',
                                                             'application_data', 'date'])
                    st.table(df)
                if choice == 'Works':
                    works = db.select_works(db_connection)
                    workers = db.select_workers(db_connection)
                    df_workers = pd.DataFrame(workers, columns=['id', 'role_id', 'name', 'surname', 'email', 'phone',
                                                                'login', 'password', 'experience'])
                    df_brigadiers = df_workers[df_workers['role_id'] == 2]
                    clients = db.select_clients(db_connection)
                    df_clients = pd.DataFrame(clients, columns=['id', 'name', 'surname', 'email', 'phone', 'login', 'password'])
                    with st.form(key='new_worker', clear_on_submit=True):
                        st.subheader('Создание нового аккаунта работника')
                        work_brigadier = st.selectbox('Выберите Бригадира', ['Саня Ким'])
                        work_client = st.selectbox('Выберите клиента', ['vasya'])
                        services = db.select_services(db_connection)
                        service_names = [x[1] for x in services]
                        work_service = st.selectbox('Выбрать сервис', service_names)
                        work_status = 1
                        address = st.text_input('Введите адрес')
                        create_btn = st.form_submit_button('Создать работу')
                        if create_btn:
                            #client_id = work_client.split()[0]
                            #work_brigadier = work_brigadier.split()[0]
                            st.success('Вы добавили новую работу')
                elif choice == 'Clients':
                    clients = db.select_clients(db_connection)
                    df = pd.DataFrame(clients, columns=['id', 'name', 'surname', 'email', 'phone', 'login', 'password'])
                    df = df.drop(['id', 'login', 'password'], axis=1)
                    st.table(df)
                elif choice == 'Workers':
                    workers = db.select_workers(db_connection)
                    workers = sorted(workers, key=lambda worker: worker[1])
                    roles = db.select_roles(db_connection)
                    df_workers = pd.DataFrame(workers, columns=['id', 'role_id', 'name', 'surname', 'email', 'phone',
                                                                'login', 'password', 'experience'])
                    df_roles = pd.DataFrame(roles, columns=['id', 'role_name'])
                    df_workers['role_id'] = df_workers['role_id'].map({1: 'Админ', 2: 'Бригадир', 3: 'Оператор'})
                    df_workers = df_workers.drop(['id'], axis=1)

                    st.table(df_workers)
                    st.button('Обновить таблицу работников')
                    with st.form(key='new_worker', clear_on_submit=True):
                        st.subheader('Создание нового аккаунта работника')
                        worker_role = st.selectbox('Выберите роль работника', ['Бригадир', 'Оператор'])
                        worker_name = st.text_input("Имя")
                        worker_surname = st.text_input("Фамилия")
                        worker_email = st.text_input('Почта')
                        worker_phone = st.text_input('Телефон')
                        worker_login = st.text_input('Логин')
                        worker_password = st.text_input('Пароль')
                        worker_experience = st.slider('Выберите опыт работника', 0, 50)
                        worker_role_id = 2 if worker_role == 'Бригадир' else 3
                        signup_btn = st.form_submit_button('Создать нового работника')
                        if signup_btn:
                            new_worker = Worker(worker_role_id, worker_name, worker_surname, worker_email, worker_phone,
                                                worker_login, worker_password, worker_experience)
                            db.insert_worker(db_connection, new_worker)
                elif choice == 'Services':
                    services = db.select_services(db_connection)
                    df = pd.DataFrame(services, columns=['id', 'service_name', 'collection_name'])
                    st.table(df)
                elif choice == 'Materials':
                    materials = mongo_db.materials.find({})
                    df = pd.DataFrame(materials)
                    st.table(df)
                elif choice == 'Wall_materials':
                    wall_materials = mongo_db.walls.find({})
                    df = pd.DataFrame(wall_materials)
                    df_conn = df.copy()
                    df_conn['material_id'] = df_conn['material_id'].apply(
                        lambda x: mongo_db.materials.find_one({"_id": int(x)})['name'])
                    check = st.checkbox('Связать id с названиями')
                    if not check:
                        st.table(df)
                    else:
                        st.table(df_conn)
                elif choice == 'Foundations':
                    foundations = mongo_db.foundations.find({})
                    df = pd.DataFrame(foundations)
                    df_conn = df.copy()
                    df_conn['material_id'] = df_conn['material_id'].apply(
                        lambda x: mongo_db.materials.find_one({"_id": int(x)})['name'])
                    check = st.checkbox('Связать id с названиями')
                    if not check:
                        st.table(df)
                    else:
                        st.table(df_conn)
                elif choice == 'Houses':
                    houses = mongo_db.houses.find({})
                    df = pd.DataFrame(houses)
                    df_conn = df.copy()
                    df_conn['foundation_id'] = df_conn['foundation_id'].apply(
                        lambda x: mongo_db.foundations.find_one({"_id": int(x)})['name'])
                    df_conn['roof_id'] = df_conn['roof_id'].apply(
                        lambda x: mongo_db.roofs.find_one({"_id": int(x)})['name'])
                    df_conn['wall_id'] = df_conn['wall_id'].apply(
                        lambda x: mongo_db.walls.find_one({"_id": int(x)})['name'])
                    check = st.checkbox('Связать id с названиями')
                    if not check:
                        st.table(df)
                    else:
                        st.table(df_conn)
                elif choice == 'Fences':
                    fences = mongo_db.fences.find({})
                    df = pd.DataFrame(fences)
                    df_conn = df.copy()
                    df_conn['material_id'] = df_conn['material_id'].apply(lambda x: mongo_db.materials.find_one({"_id": int(x)})['name'])
                    check = st.checkbox('Связать id с названиями')
                    if not check:
                        st.table(df)
                    else:
                        st.table(df_conn)
                elif choice == 'Suppliers':
                    fences = mongo_db.suppliers.find({})
                    df = pd.DataFrame(fences)
                    st.table(df)
    with tab2:
        st.header('Создание нового пользователя')
        st.subheader('Введите ваши данные')
        with st.form(key='signup', clear_on_submit=True):
            new_client_name = st.text_input("Ваше имя")
            new_client_surname = st.text_input("Ваша фамилия")
            new_client_email = st.text_input('Ваша почта')
            new_client_phone = st.text_input('Ваш телефон')
            new_client_login = st.text_input('Логин для входа')
            new_client_password = st.text_input('Пароль для входа')
            signup_btn = st.form_submit_button('Зарегистрироваться')
        if signup_btn:
            new_client: Client = Client(new_client_name, new_client_surname, new_client_email,
                                        new_client_phone, new_client_login, new_client_password)
            is_reg = db.registrate_client(db_connection, new_client)
            if is_reg:
                st.success('Новый пользователь успешно создан')
            else:
                st.error('Не удалось созать нового пользователя. Проверьте введенные данные')


main_page()
