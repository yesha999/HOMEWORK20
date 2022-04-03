from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from service.director import DirectorService


class DirectorNotFound(Exception):
    pass


@pytest.fixture()
def director_dao():
    """Мокируем данные"""
    dao = DirectorDAO
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao


@pytest.fixture()
def director_service(director_dao):
    """Вкладываем в настоящий сервис мокированное дао"""
    return DirectorService(dao=director_dao)


@pytest.mark.parametrize('data', ({'id': 1, 'name': 'test'},))
def test_get_one(director_service, data):
    """Тест получает один словарик"""
    director_service.dao.get_one.return_value = data

    assert director_service.get_one(1) == data


def test_get_one_w_error(director_service):
    """Тест должен получить ошибку, если режиссер не найден"""
    director_service.dao.get_one.side_effect = DirectorNotFound

    with pytest.raises(DirectorNotFound):
        director_service.get_one(100)


@pytest.mark.parametrize('data', ([{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'test2'}],))
def test_get_all(director_service, data):
    """Тест проверяет вывод списка данных"""
    director_service.dao.get_all.return_value = data

    assert isinstance(director_service.get_all(), list)
    assert director_service.get_all() == data


@pytest.mark.parametrize('data, updata', (({'id': 1, 'name': 'test'}, {'id': 1, 'name': 'changed_test'}),))
def test_partially_update(director_service, data, updata):
    """Тест проверяет корректность частичного обновления данных"""
    director_service.dao.get_one.return_value = data
    director_service.partially_update(updata)

    director_service.dao.update.assert_called_once_with(updata)


@pytest.mark.parametrize('data, updata', (({'id': 1, 'name': 'test'}, {'id': 1, 'error': 'error'}),))
def test_partially_update_error(director_service, data, updata):
    """Тест проверяет отсутствие обновления данных при их ошибочном вводе"""
    director_service.dao.get_one.return_value = data
    director_service.partially_update(updata)

    director_service.dao.update.assert_called_once_with(data)


def test_delete(director_service):
    """Тест проверяет, действительно ли удалится выбранная запись"""
    director_service.dao.delete(1)
    director_service.dao.delete.assert_called_once_with(1)