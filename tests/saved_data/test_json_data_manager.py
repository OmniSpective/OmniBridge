import os
from typing import Dict

import pytest

import omnibridge.saved_data.json_data_manager
from omnibridge.saved_data.json_data_manager import JsonConvertable, JsonDataManager, MODULE_DIR


TEST_FILE_NAME = ".saved_data_test.json"
TEST_FILE_PATH = os.path.join(MODULE_DIR, TEST_FILE_NAME)
omnibridge.saved_data.json_data_manager.FILE_PATH = TEST_FILE_PATH


class Person(JsonConvertable):
    def __init__(self, name: str, age: str):
        self.name = name
        self.age = age

    def to_json(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "age": self.age
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]):
        return Person(json_data['name'], json_data['age'])


def test_save_and_load_json_succeed():
    # Arrange
    my_person = Person(name="jack", age="45")

    # Act
    JsonDataManager.save(["my_person"], my_person)
    created_person = JsonDataManager.load(["my_person"], Person)

    # Assert
    assert my_person.age == created_person.age and my_person.name == created_person.name


def test_load_json_file_not_exist_fail():
    # Arrange
    if os.path.isfile(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)

    # Act + Assert
    with pytest.raises(FileNotFoundError):
        JsonDataManager.load(["my_person"], Person)


def test_load_json_key_not_exist_fail():
    # Arrange
    if os.path.isfile(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)

    person = Person("Bruce", "50")

    # Act + Assert
    JsonDataManager.save(["bruce"], person)

    with pytest.raises(KeyError):
        JsonDataManager.load(["wayne"], Person)


def test_save_and_load_multiple_items_json_succeed():
    # Arrange
    person1 = Person(name="jack", age="45")
    person2 = Person(name="Li", age="32")

    # Act
    JsonDataManager.save([person1.name], person1)
    JsonDataManager.save([person2.name], person2)
    created_person1 = JsonDataManager.load([person1.name], Person)
    created_person2 = JsonDataManager.load([person2.name], Person)

    # Assert
    assert created_person1.age == person1.age and created_person1.name == person1.name
    assert created_person2.age == person2.age and created_person2.name == person2.name


def test_save_and_load_multiple_nested_items_json_succeed():
    # Arrange
    person1 = Person(name="jack", age="45")
    person2 = Person(name="Li", age="32")

    # Act
    JsonDataManager.save(["employees", person1.name], person1)
    JsonDataManager.save(["managers", person2.name], person2)
    created_person1 = JsonDataManager.load(["employees", person1.name], Person)
    created_person2 = JsonDataManager.load(["managers", person2.name], Person)

    # Assert
    assert created_person1.age == person1.age and created_person1.name == person1.name
    assert created_person2.age == person2.age and created_person2.name == person2.name


def test_overwrite_json_succeed():
    old_person = Person(name="wrongly typed", age="")
    updated_person = Person(name="Gal", age="28")

    # Act
    JsonDataManager.save(["my_person"], old_person)
    JsonDataManager.save(["my_person"], updated_person)
    created_person = JsonDataManager.load(["my_person"], Person)

    # Assert
    assert updated_person.age == created_person.age and updated_person.name == created_person.name


def test_save_multiple_classes_json_succeed():
    # Arrange
    class Pet(JsonConvertable):
        def __init__(self, nickname: str):
            self.nickname = nickname

        def to_json(self) -> Dict[str, str]:
            return {
                'nickname': self.nickname
            }

        @classmethod
        def create_from_json(cls, json_key: str, json_data: Dict[str, str]):
            return Pet(json_data['nickname'])

    person = Person("owner", "32")
    pet = Pet("dogo")

    # Act
    JsonDataManager.save(["my_person"], person)
    JsonDataManager.save(["my_pet"], pet)
    loaded_person = JsonDataManager.load(["my_person"], Person)
    loaded_pet = JsonDataManager.load(["my_pet"], Pet)

    # Assert
    assert loaded_person.name == person.name and loaded_pet.nickname == pet.nickname
