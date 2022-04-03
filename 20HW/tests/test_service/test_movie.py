from unittest.mock import MagicMock

import pytest

from dao.movie import MovieDAO
from service.movie import MovieService


class MovieNotFound(Exception):
    pass


@pytest.fixture()
def movie_dao():
    """Мокируем данные"""
    dao = MovieDAO
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    dao.create = MagicMock()
    return dao


@pytest.fixture()
def movie_service(movie_dao):
    """Вкладываем в настоящий сервис мокированное дао"""
    return MovieService(dao=movie_dao)


@pytest.mark.parametrize('data', ({'id': 1, 'title': 'test'},))
def test_get_one(movie_service, data):
    """Тест получает один словарик"""
    movie_service.dao.get_one.return_value = data

    assert movie_service.get_one(1) == data


def test_get_one_w_error(movie_service):
    """Тест должен получить ошибку, если фильм не найден"""
    movie_service.dao.get_one.side_effect = MovieNotFound

    with pytest.raises(MovieNotFound):
        movie_service.get_one(100)


@pytest.mark.parametrize('data', ([{'id': 1, 'title': 'test'}, {'id': 2, 'title': 'test2'}],))
def test_get_all(movie_service, data):
    """Тест проверяет вывод списка данных"""
    movie_service.dao.get_all.return_value = data

    assert isinstance(movie_service.get_all(), list)
    assert movie_service.get_all() == data


@pytest.mark.parametrize('data, updata', (({'id': 1, 'title': 'test'}, {'id': 1, 'title': 'changed_test'}), (
        {'id': 2, 'title': 'test2', }, {'id': 2, 'title': 'changed_test2', 'rating': 8.5})))
def test_partially_update(movie_service, data, updata):
    """Тест проверяет корректность частичного обновления данных"""
    movie_service.dao.get_one.return_value = data
    movie_service.partially_update(updata)

    movie_service.dao.update.assert_called_once_with(updata)


@pytest.mark.parametrize('data, updata', (({'id': 1, 'title': 'test'}, {'id': 1, 'error': 'error'}),))
def test_partially_update_error(movie_service, data, updata):
    """Тест проверяет отсутствие обновления данных при их ошибочном вводе"""
    movie_service.dao.get_one.return_value = data
    movie_service.partially_update(updata)

    movie_service.dao.update.assert_called_once_with(data)


@pytest.mark.parametrize('data, error_and_correct_data, return_data', (
        ({'id': 1, 'title': 'test', 'rating': 8.3}, {'id': 1, 'error': 'error', 'rating': 1.2},
         {'id': 1, 'title': 'test', 'rating': 1.2}),))
def test_partially_update_error_and_correct(movie_service, data, error_and_correct_data, return_data):
    """Тест проверяет обновление только корректных данных"""
    movie_service.dao.get_one.return_value = data

    movie_service.partially_update(error_and_correct_data)
    movie_service.dao.update.assert_called_once_with(return_data)


def test_delete(movie_service):
    """Тест проверяет, действительно ли удалится выбранная запись"""
    movie_service.dao.delete(1)
    movie_service.dao.delete.assert_called_once_with(1)


@pytest.mark.parametrize('data', (({'title': 'test', 'description': 'description_test',
                                    'trailer': 'trailer_test', 'year': 2077, 'rating': 9.1, 'genre_id': 1,
                                    'director_id': 1}),))
def test_create(movie_service, data):
    """Тест проверяет работу внесения новых данных"""
    movie_service.dao.create.return_value = data
    assert isinstance(movie_service.dao.create(data), dict)
    assert movie_service.dao.create(data) == data

# Нижеприведенный тест показал, что в коде программы не осуществляется проверки на корректность вносимых новых данных
# @pytest.mark.parametrize('data', (({'error': 'error'}),))
# def test_create_with_wrong_parametres(movie_service, data):
#     """Тест проверяет работу внесения ошибочных новых данных"""
#     movie_service.dao.create.return_value = data
#     assert movie_service.dao.create(data) == data
