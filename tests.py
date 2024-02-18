import pytest
from main import BooksCollector
import helper_funcs
from typings.age_rank_enum import AgeRank


class TestBooksCollector:

    # вспомогательные функции
    @staticmethod
    def add_2_new_books(collector):
        """
            Вспомогательная функция.
            Добавляет 2 книги в словарь с книгами
        """
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

    @staticmethod
    def get_dict_with_books_and_genres(collector: BooksCollector, age_rank: AgeRank = AgeRank.ALL) -> dict[str, str]:
        """
            Вспомогательная функция.
            Возвращает словарь с книгами по нужной возрастной категории
        """
        genres_list = []
        result_dict = dict()

        match age_rank:
            case AgeRank.CHILDREN:
                children_genres_list = list(set(collector.genre) - set(collector.genre_age_rating))
                genres_list = children_genres_list
            case AgeRank.ADULTS:
                genres_list = collector.genre_age_rating
            case AgeRank.ALL:
                genres_list = collector.genre

        for genre in genres_list:
            result_dict[f'Book title with {genre} genre'] = genre
        return result_dict

    # add_new_book tests
    def test_add_new_book_add_two_books_success(self):
        """
            Добавить 2 книги и проверить, что они успешно добавлены в словарь
        """
        collector = BooksCollector()
        self.add_2_new_books(collector)
        assert len(collector.books_genre) == 2

    def test_add_new_book_add_the_same_book_twice_added_once(self):
        """
            Проверить, что одна и та же книга добавляется в словарь только в единственном экземпляре
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 1 and list(collector.books_genre.keys()) == [book_name]

    @pytest.mark.parametrize(
        'name',
        [
            '',
            'Test book titleTest book titleTest book t',  # 41 symbols,
            'Test book titleTest book titleTest book titleTest book titleTest book titleTest book title'  # 90 symbols,
        ]
    )
    def test_add_new_book_0_or_more_than_40_symbols_title_failure(self, name):
        """
            Если название книги невалидное, т.е. длина 0 или больше 40 символов, то книга не добавлена в словарь
        """
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
        """
            Если название кники валидное, т.е. длина от 1 до 40 символов, то книга добавлена в словарь
        """
        collector = BooksCollector()
        collector.add_new_book(name)
        assert collector.books_genre.get(name) is not None

    def test_add_new_book_new_book_not_have_genre(self):
        """
            Новая книга добавляется в словарь с пустым жанром
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        assert collector.books_genre.get(book_name) == ''

    # set_book_genre tests
    def test_set_book_genre_existing_book_and_genre_success(self):
        """
            Если книга существует в словаре и жанр есть в genre, то функция успешно добавляет к книге жанр
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        genre = collector.genre[0]
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    def test_set_book_genre_not_existing_book_failure(self):
        """
            Если книга не существует в словаре, то функция не изменяет словарь
        """
        collector = BooksCollector()
        existing_book_title = 'existing'
        not_existing_book_title = 'not existing'
        genre = collector.genre[0]
        collector.add_new_book(existing_book_title)
        collector.set_book_genre(not_existing_book_title, genre)
        assert collector.books_genre[existing_book_title] == '' and len(collector.books_genre) == 1

    def test_set_book_genre_not_existing_genre_failure(self):
        """
            Если книга существует в словаре, а жанр не существует в списке genre, то функция не изменяет словарь
        """
        collector = BooksCollector()
        existing_book_title = 'existing'
        not_existing_genre = helper_funcs.generate_random_string()
        collector.add_new_book(existing_book_title)
        collector.set_book_genre(existing_book_title, not_existing_genre)
        assert collector.books_genre[existing_book_title] == '' and len(collector.books_genre) == 1

    def test_set_book_genre_not_existing_book_and_genre_failure(self):
        """
            Если книга  не существует в словаре и жанр не существует в списке genre, то функция не изменяет словарь
        """
        collector = BooksCollector()
        not_existing_book_title = 'not existing'
        not_existing_genre = helper_funcs.generate_random_string()
        collector.set_book_genre(not_existing_book_title, not_existing_genre)
        assert len(collector.books_genre) == 0

    # get_book_genre tests
    def test_get_book_genre_existing_book_returns_correct_genre(self):
        """
            Если в словарь добавлены книги, то для заданного названия книги функция возвращает правильный жанр.
        """
        collector = BooksCollector()
        self.add_2_new_books(collector)
        book_title = list(
            collector.books_genre.keys()
        )[0]
        book_genre = collector.books_genre[book_title]
        assert collector.get_book_genre(book_title) == book_genre

    def test_get_book_genre_not_existing_book_returns_none(self):
        """
            Если книга не существует в словаре, то для этой книги функция возвращает жанр = None
        """
        collector = BooksCollector()
        book_title = helper_funcs.generate_random_string()
        assert collector.get_book_genre(book_title) is None

    # get_books_with_specific_genre tests
    @pytest.mark.parametrize(
        'genre',
        BooksCollector().genre
    )
    def test_get_books_with_specific_genre_existing_genre_returns_specified_list(self, genre):
        """
            Если жанр существует с списке жанров, то функция возвращает список книг с этим жанром
        """
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        book_names_list = list(
            dict(
                filter(lambda item: item[1] == genre, collector.books_genre.items())
            )
        )
        assert collector.get_books_with_specific_genre(genre) == book_names_list

    def test_get_books_with_specific_genre_not_existing_genre_empty_result(self):
        """
            Если жанр не существует с списке жанров, то функция возвращает  пустой список
        """
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        not_existing_genre = helper_funcs.generate_random_string()
        assert collector.get_books_with_specific_genre(not_existing_genre) == []

    # get_books_genre tests
    def test_get_books_genre_not_empty_books_dict_returns_all_books_dict(self):
        """
            Если словарь с книгами не пустой, то функция возвращает словарь со всеми добавленными книгами
        """
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        assert collector.get_books_genre() == collector.books_genre

    def test_get_books_genre_empty_books_dict_returns_empty_dict(self):
        """
            Если словарь с книгами пустой, то функция возвращает пустой словарь
        """
        collector = BooksCollector()
        assert collector.get_books_genre() == collector.books_genre

    # get_books_for_children tests
    def test_get_books_for_children_existing_books_for_children_success(self):
        """
            проверяем, что функция возвращает список книг, соответствующих детскому возрастному ограничению 
        """
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector)
        children_books_dict = self.get_dict_with_books_and_genres(collector, AgeRank.CHILDREN)
        assert sorted(collector.get_books_for_children()) == sorted(list(children_books_dict))

    def test_get_books_for_children_not_existing_children_books_returns_empty_list(self):
        """
            если в словаре нет книг для детей, то возвращается пустой список
        """
        collector = BooksCollector()
        collector.books_genre = self.get_dict_with_books_and_genres(collector, AgeRank.ADULTS)
        assert sorted(collector.get_books_for_children()) == []

    # test_add_book_in_favorites tests
    def test_add_book_in_favorites_existing_book_success(self):
        """
            если книга есть в словаре, то функция добавляет книгу в список favorites
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert collector.favorites == [book_name]

    def test_add_book_in_favorites_not_existing_book_failure(self):
        """
            если книги нет в словаре, то функция не добавляет книгу в список favorites
        """
        collector = BooksCollector()
        existing_book_name = 'Test book title 1'
        not_existing_book_name = 'Test book title 2'
        collector.add_new_book(existing_book_name)
        collector.add_book_in_favorites(not_existing_book_name)
        assert collector.favorites == []

    # delete_book_from_favorites tests
    def test_delete_book_from_favorites_existing_book_success(self):
        """
            Если книга есть в словаре, то функция удаляет книгу из favorites
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert collector.favorites == []

    # get_list_of_favorites_books tests
    def test_get_list_of_favorites_books_no_favorite_books_returns_empty_list(self):
        """
            Если список избранных книг пустой, то функция возвращает пустой список
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_have_favorite_books_returns_favorites_list(self):
        """
            Если список избранных книг непустой, то функция возвращает пустой список
        """
        collector = BooksCollector()
        book_name = 'Test book title 1'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert collector.get_list_of_favorites_books() == [book_name]
