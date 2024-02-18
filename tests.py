import pytest
from main import BooksCollector
import helper_funcs
from typings.age_rank_enum import AgeRank


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # вспомогательная функция
    @staticmethod
    def add_2_new_books(collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

    @staticmethod
    def get_dict_with_books_and_genres(collector, with_children_genres_only = False) -> dict[str, str]:
        result_dict = dict()
        genres_list = collector.genre
        if with_children_genres_only:
            children_genres_list = list(set(collector.genre) - set(collector.genre_age_rating))
            genres_list = children_genres_list
        for genre in genres_list:
            result_dict[f'Book title with {genre} genre'] = genre
        return result_dict

    # add_new_book tests
    def test_add_new_book_add_two_books_success(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        self.add_2_new_books(collector)

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.books_genre) == 2

    # книгу можно добавить только 1 раз
    def test_add_new_book_add_book_twice_false(self):
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize(
        'name',
        [
            '',
            'Test book titleTest book titleTest book t',  # 41 symbols,
            'Test book titleTest book titleTest book titleTest book titleTest book titleTest book title'  # 90 symbols,
        ]
    )
    def test_add_new_book_0_or_more_than_40_symbols_title_failure(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert collector.books_genre.get(name) is None

    @pytest.mark.parametrize(
        'name',
        [
            'T',
            'Te',
            'Test book title',  # 15 symbols,
            'Test book titleTest book titleTest book',  # 39 symbols,
            'Test book titleTest book titleTest book '  # 40 symbols,
        ]
    )
    def test_add_new_book_1_to_40_symbols_title_success(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert collector.books_genre.get(name) is not None

    def test_add_new_book_new_book_not_have_genre(self):
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        assert collector.books_genre.get(book_name) == ''

    # set_book_genre tests
    def test_set_book_genre_existing_book_and_genre_success(self):
        collector = BooksCollector()
        book_name = 'Test book title 1'
        genre = collector.genre[0]
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    def test_set_book_genre_not_existing_book_failure(self):
        collector = BooksCollector()
        existing_book_title = 'existing'
        not_existing_book_title = 'not existing'
        genre = collector.genre[0]
        collector.add_new_book(existing_book_title)
        collector.set_book_genre(not_existing_book_title, genre)
        assert collector.books_genre[existing_book_title] == '' and len(collector.books_genre) == 1

    def test_set_book_genre_not_existing_genre_failure(self):
        collector = BooksCollector()
        existing_book_title = 'existing'
        not_existing_genre = helper_funcs.generate_random_string()
        collector.add_new_book(existing_book_title)
        collector.set_book_genre(existing_book_title, not_existing_genre)
        assert collector.books_genre[existing_book_title] == '' and len(collector.books_genre) == 1

    def test_set_book_genre_not_existing_book_and_genre_failure(self):
        collector = BooksCollector()
        not_existing_book_title = 'not existing'
        not_existing_genre = helper_funcs.generate_random_string()
        collector.set_book_genre(not_existing_book_title, not_existing_genre)
        assert len(collector.books_genre) == 0

    # get_book_genre tests
    def test_get_book_genre_existing_book_success(self):
        collector = BooksCollector()
        self.add_2_new_books(collector)
        book_title = list(
            collector.books_genre.keys()
        )[0]
        book_genre = collector.books_genre[book_title]
        assert collector.get_book_genre(book_title) == book_genre

    def test_get_book_genre_not_existing_book_failure(self):
        collector = BooksCollector()
        # self.add_2_new_books(collector)
        book_title = helper_funcs.generate_random_string()
        assert collector.get_book_genre(book_title) is None

    # get_books_with_specific_genre tests
    @pytest.mark.parametrize(
        'genre',
        BooksCollector().genre
    )
    def test_get_books_with_specific_genre_existing_genre_success(self, genre):
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        book_names_list = list(
            dict(
                filter(lambda item: item[1] == genre, collector.books_genre.items())
            )
        )
        assert collector.get_books_with_specific_genre(genre) == book_names_list

    def test_get_books_with_specific_genre_not_existing_genre_empty_result(self):
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        not_existing_genre = helper_funcs.generate_random_string()
        assert collector.get_books_with_specific_genre(not_existing_genre) == []

    # get_books_genre tests
    def test_get_books_genre_not_empty_books_dict_success(self):
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        assert collector.get_books_genre() == collector.books_genre

    def test_get_books_genre_empty_books_dict_success(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == collector.books_genre

    # get_books_for_children tests
    def test_get_books_for_children_existing_books_for_children_success(self):
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        children_books_dict = self.get_dict_with_books_and_genres(collector, True)
        assert sorted(collector.get_books_for_children()) == sorted(list(children_books_dict))

    def test_get_books_for_children_not_existing_books_for_children_success(self):
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        children_books_dict = self.get_dict_with_books_and_genres(collector, True)
        assert sorted(collector.get_books_for_children()) == sorted(list(children_books_dict))



