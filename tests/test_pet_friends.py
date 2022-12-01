from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_with_invalid_log_data(email="", password=""):
    """ Проверяем невозможность получения ключа без заполнения строк email и password"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key_with_invalid_log_data(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print('\nТакого пользователя нет в системе!')

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем невозможность получения списка питомцев при использовании невалидного ключа """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    _, auth_key = pf.get_api_key(email='', password='')
    status, result = pf.get_list_of_pets_with_invalid_key(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print('\nТакого пользователя нет в системе!')

def test_get_all_pets_with_wrong_parameter(filter='my_pet'):
    """ Проверяем ответ от сервера при указании невалидного значения фильтра """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    _, auth_key = pf.get_api_key(email = valid_email, password = valid_password)
    status, result = pf.get_list_of_pets_with_invalid_parameter(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 500
    print('\nВы указали неверный фильтр!')

def test_create_pet_simple(name='Ниня', animal_type='Ориентальная кошка', age='1'):
    """ Проверяем что можно добавить питомца без фото """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_pet_photo(pet_photo='images/Ninya2.jpg'):
    """ Проверяем что можно добавить фото питомца к уже созданной записи """

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если есть питомец, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_pet_photo_with_invalid_format(pet_photo='images/textfile.docx'):
    """ Проверяем невозможность добавления текстового файла вместо изображения """

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если есть питомец, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo_with_invalid_format(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 500
        assert status == 500
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_with_valid_data(name='Ниня', animal_type='Ориентальная кошка',
                                     age='1', pet_photo='images/Ninya1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    
def test_add_new_pet_without_pet_data(name='', animal_type='',
                                     age='', pet_photo='images/Ninya1.jpg'):
    """ Проверяем что можно добавить питомца с некорректными данными """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем возможность добавления питомца по заданным параметрам
    if pf.add_new_pet(auth_key, name, animal_type, age, pet_photo):
        pass
    else:
        # если поля пустые - вызываем ошибку
        raise FileNotFoundError("Заполните обязательные поля!")

def test_add_new_pet_without_pet_photo(name='Ниня', animal_type='Ориентальная кошка',
                                     age='1', pet_photo=''):
    """ Проверяем что можно добавить питомца без фото """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем на ошибку
    with pytest.raises(FileNotFoundError):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Плюша', animal_type='Британская кошка', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
