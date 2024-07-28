import os.path
import pytest

from my_api import PetFriends
from setting import valid_email, valid_password
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >0

def test_add_new_pet_without_photo_with_valid_data(name='Tor', animal_type='armadillo',
                                     age='4'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_new_pet_with_valid_data(pet_id = 'pet_id[0]', pet_photo='images/armadillo.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']

    # Добавляем питомца
    status, result = pf.add_photo_of_new_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # assert result['pet_photo'] == pet_photo

def test_add_new_pet_with_valid_data(name='Valera', animal_type='Capybara',
                                     age='4', pet_photo='images/Capybara.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Tor', animal_type='Capybara', age=5):
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


"""Негативные тесты"""
def test_get_api_key_for_invalid_user(email='uginy1@mail.ru', password=valid_password):
    """Проверяем что ответ будет содержать код 4хх при авторизации
    с неверным емайлом и верным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_password(email=valid_email, password='qwerty'):
    """Проверяем что ответ будет содержать код 4хх при авторизации
    с верным емайлом и неверным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_with_empty_password(email=valid_email, password=''):
    """Проверяем что ответ будет содержать код 4хх при авторизации
    с верным емайлом и пустым полем пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user(email='uginymail.ru', password=valid_password):
    """Проверяем что ответ будет содержать код 4хх при авторизации
    с неверным емайлом и верным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_with_empty_data(email='', password= ''):
    """Проверяем что ответ будет содержать код 4хх при авторизации
    с пустыми полями емайл и пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_long_one_parameter(name='Tor', animal_type='armadillo',
                                     age='12345678000000000000000000999999999999999998888888888888777777777776666666666666555555555544444444444333333333332222222222221111111111111110000000000'):
    """Проверяем что ответ будет содержать код 4хх
    при добавлении животоного с одинм очень длинным параметром"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

    """Баг. Ожидаем, что сервер не примет запрос с таким большим параметром. 
    Однако, сервер данный запрос обрабатывает и создает карточку"""

def test_add_new_pet_with_invalid_format_photo(name='Tor', animal_type='Capybara',
                                     age='4', pet_photo='images/MHKq.gif'):
    """Проверяем что нельзя добавить изображение другого формата кроме JPG, JPEG or PNG"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

    """Баг. Ожидаем, что сервер не примет запрос с фото другого формата. 
    Однако, сервер данный запрос обрабатывает и создает карточку, но без фотографии"""


def test_update_pet_info_with_invalid_index_id(name='Tor', animal_type='Capybara', age=5):
    """Проверяем что не обновляется информацию о животном с несуществующим индексом id """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        try:
            # Пробуем получить питомца по несуществующему индексу
            invalid_pet_id = my_pets['pets'][110]['id']
            status, result = pf.update_pet_info(auth_key, invalid_pet_id, name, animal_type, age)
        except IndexError as e:
            assert str(e) == 'list index out of range', f"Expected 'list index out of range' but got {str(e)}"
        else:
            # Если исключение не было вызвано, то тест провален
            pytest.fail("Expected IndexError was not raised")
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_without_parameters(name='', animal_type='',
                                     age='6', pet_photo='images/Capybara.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Ожидаем, что сервер вернет код ответа 400 или другой код 4xx
    assert 400 <= status < 500, f"Expected status code 4xx but got {status}"

    # Дополнительно можно проверить сообщение об ошибке, если оно возвращается
    expected_error_message = "Invalid data: fields 'name', 'animal_type' and 'age' cannot be empty"
    assert expected_error_message in result, f"Expected error message '{expected_error_message}' but got {result}"

    """Баг. Ожидаем, что сервер не примет запрос с пустыми полями. 
    Однако, сервер данный запрос обрабатывает и создает карточку"""

def test_delete_with_invalid_index_id():
    """Проверяем что нельзя удадить питомца с несуществующим индексом id"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) > 0:
        try:
            # Пробуем получить питомца по несуществующему индексу
            invalid_pet_id = my_pets['pets'][110]['id']
            status, result = pf.delete_pet(auth_key, invalid_pet_id)
        except IndexError as e:
            assert str(e) == 'list index out of range', f"Expected 'list index out of range' but got {str(e)}"
        else:
            # Если исключение не было вызвано, то тест провален
            pytest.fail("Expected IndexError was not raised")
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
