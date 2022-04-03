from unittest.mock import MagicMock

import pytest

from dao.genre import GenreDAO
from service.genre import GenreService


class GenreNotFound(Exception):
    pass


@pytest.fixture()
def genre_dao():
    """Мокируем данные"""
    dao = GenreDAO
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao


@pytest.fixture()
def genre_service(genre_dao):
    """Вкладываем в настоящий сервис мокированное дао"""
    return GenreService(dao=genre_dao)


@pytest.mark.parametrize('data', ({'id': 1, 'name': 'test'},))
def test_get_one(genre_service, data):
    """Тест получает один словарик"""
    genre_service.dao.get_one.return_value = data

    assert genre_service.get_one(1) == data


def test_get_one_w_error(genre_service):
    """Тест должен получить ошибку, если жанр не найден"""
    genre_service.dao.get_one.side_effect = GenreNotFound

    with pytest.raises(GenreNotFound):
        genre_service.get_one(100)


@pytest.mark.parametrize('data', ([{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'test2'}],))
def test_get_all(genre_service, data):
    """Тест проверяет вывод списка данных"""
    genre_service.dao.get_all.return_value = data

    assert isinstance(genre_service.get_all(), list)
    assert genre_service.get_all() == data


@pytest.mark.parametrize('data, updata', (({'id': 1, 'name': 'test'}, {'id': 1, 'name': 'changed_test'}),))
def test_partially_update(genre_service, data, updata):
    """Тест проверяет корректность частичного обновления данных"""
    genre_service.dao.get_one.return_value = data
    genre_service.partially_update(updata)

    genre_service.dao.update.assert_called_once_with(updata)


@pytest.mark.parametrize('data, updata', (({'id': 1, 'name': 'test'}, {'id': 1, 'error': 'error'}),))
def test_partially_update_error(genre_service, data, updata):
    """Тест проверяет отсутствие обновления данных при их ошибочном вводе"""
    genre_service.dao.get_one.return_value = data
    genre_service.partially_update(updata)

    genre_service.dao.update.assert_called_once_with(data)


def test_delete(genre_service):
    """Тест проверяет, действительно ли удалится выбранная запись"""
    genre_service.dao.delete(1)
    genre_service.dao.delete.assert_called_once_with(1)
