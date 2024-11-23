import os

from api import PetFrends
from settings import valid_email, valid_password, invalid_password, invalid_email

pf = PetFrends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Получение api ключа  с валидными данными.'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_key_negative(email=invalid_email, password=valid_password):
    '''Проверяем получение ключа с недействительным имейлом.'''
    status, result = pf.get_api_key(email, password)

    # Сверяем, что статус код равен 403.
    assert result.status_code == 403


def test_get_key_negative_2(email=valid_email, password=invalid_password):
    '''Проверяем получение ключа с недействительным поролем.'''
    status, result = pf.get_api_key(email, password)

    # Сверяем, что статус код равен 403.
    assert result.status_code == 403


def test_get_all_pets_with_valid_key(filter=''):
    '''Получение списка всех животных с действительным ключем.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Обезьян', animal_type='шимпанзе', age='4', pet_photo='images/cat1.jpg'):
    '''Добавление питомца с действительными данными.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


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
    status, result = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(self, name='Барс', animal_type='кот', age=2):
    """Проверяем возможность добавления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(self, auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_negative_add_new_pet_with_empty_name():
    '''Проверяем, что нельзя добавить питомца с пустым именем.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, '', 'dog', '2', 'images/dog1.jpeg')

    # Если статус 200 то это баг сервера
    # Проверяем что статус ответа = 400
    assert status == 400


def test_negative_add_new_pet_with_empty_anymal_type(status=None):
    '''Проверяем, что нельзя добавить питомца без указания породы.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(auth_key, 'Барбос', '', 'images/dog1.jpeg')

    # Проверяем что статус ответа = 400
    assert status == 400


def test_successful_add_pet_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pet_id, 'pet_photo')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('ops')


def test_get_all_pets_with_invalid_key(filter=''):
    '''Проверяем, что запрос списка питомцев с невалидным ключом возвращает ошибку.'''
    # Создаем заведомо невалидный auth_key
    invalid_auth_key = {"key": "invalid_auth_key"}

    # Пробуем получить список питомцев с невалидным ключом
    status, result = pf.get_list_of_pets(invalid_auth_key, filter)

    # Проверяем, что статус ответа соответствует ошибке доступа
    assert status == 403, "API должно возвращать статус 403 при невалидном auth_key"


def test_add_pet_with_name_exceeding_max_length():
    """Проверяем невозможность добавления питомца с именем длиной более 255 символов"""
    # Генерируем имя длиной 256 символов
    long_name = "A" * 256
    animal_type = "dog"
    age = "4"

    # Получаем auth_key для авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца с слишком длинным именем
    status, result = pf.add_new_pet(auth_key, long_name, animal_type, age, None)

    # Проверяем, что API возвращает ошибку
    assert status == 400, "API должно возвращать статус 400 для имени длиннее 255 символов"
    assert "error" in result, "Ответ должен содержать сообщение об ошибкe"


def test_add_pet_with_negative_age():
    """Проверяем невозможность добавления питомца с отрицательным значением возраста"""

    name = "Бобик"
    animal_type = "dog"
    negative_age = "-5"

    # Получаем auth_key для авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца с отрицательным возрастом
    status, result = pf.add_new_pet(auth_key, name, animal_type, negative_age, None)

    # Проверяем, что API возвращает ошибку
    assert status == 400, "API должно возвращать статус 400 для отрицательного возраста"
    assert "error" in result, "Ответ должен содержать сообщение об ошибке"


def test_update_pet_with_invalid_pet_id():
    """Проверяем невозможность обновления информации питомца с невалидным pet_id"""

    invalid_pet_id = "invalid_pet_id_123"
    new_name = "Рекс"
    new_animal_type = "собака"
    new_age = "5"

    # Получаем auth_key для авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся обновить данные питомца с невалидным pet_id
    status, result = pf.update_pet_info(auth_key, invalid_pet_id, new_name, new_animal_type, new_age)

    # Проверяем, что API возвращает ошибку
    assert status == 400
