# qa_python_4

* Для запуска тестов используется команда 
```pytest tests.py -v```
* Для оценки покрытия ```pytest --cov```

********* 

## Аннотация к тестам из файла tests.py
1. add_new_book(name)
   - test_add_new_book_add_two_books_success() -- Добавить 2 книги и проверить, что они успешно добавлены в словарь
   - test_add_new_book_add_the_same_book_twice_added_once() -- Проверить, что одна и та же книга добавляется в словарь только в единственном экземпляре
   - test_add_new_book_0_or_more_than_40_symbols_title_failure(name) -- Параметризованный тест. Если название книги невалидное, т.е. длина 0 или больше 40 символов, то книга не добавлена в словарь
   - test_add_new_book_1_to_40_symbols_title_success(name) -- Параметризованный тест. Если название кники валидное, т.е. длина от 1 до 40 символов, то книга добавлена в словарь
   - test_add_new_book_new_book_not_have_genre() -- Новая книга добавляется в словарь с пустым жанром
   
2. set_book_genre(name, genre)
   - test_set_book_genre_existing_book_and_genre_success() -- Если книга существует в словаре и жанр есть в genre, то функция успешно добавляет к книге жанр
   - test_set_book_genre_not_existing_book_failure() -- Если книга не существует в словаре, то функция не изменяет словарь
   - test_set_book_genre_not_existing_genre_failure() --Если книга существует в словаре, а жанр не существует в списке genre, то функция не изменяет словарь
   - test_set_book_genre_not_existing_book_and_genre_failure() -- Если книга  не существует в словаре и жанр не существует в списке genre, то функция не изменяет словарь
   
3. get_book_genre(name)
   - test_get_book_genre_existing_book_returns_correct_genre() -- Если в словарь добавлены книги, то для заданного названия книги функция возвращает правильный жанр.
   - test_get_book_genre_not_existing_book_returns_none() -- Если книга не существует в словаре, то для этой книги функция возвращает жанр = None
   
4. get_books_with_specific_genre(genre)
   - test_get_books_with_specific_genre_existing_genre_returns_specified_list(genre) -- Если жанр существует с списке жанров, то функция возвращает список книг с этим жанром
   - test_get_books_with_specific_genre_not_existing_genre_empty_result() -- Если жанр не существует с списке жанров, то функция возвращает  пустой список
   
5. get_books_genre()
   - test_get_books_genre_not_empty_books_dict_returns_all_books_dict() -- Если словарь с книгами не пустой, то функция возвращает словарь со всеми добавленными книгами
   - test_get_books_genre_empty_books_dict_returns_empty_dict() -- Если словарь с книгами пустой, то функция возвращает пустой словарь
   
6. get_books_for_children()
   - test_get_books_for_children_existing_books_for_children_success() -- проверяем, что функция возвращает список книг, соответствующих детскому возрастному ограничению 
   - test_get_books_for_children_not_existing_children_books_returns_empty_list() -- если в словаре нет книг для детей, то возвращается пустой список
   
7. add_book_in_favorites(name)
   - test_add_book_in_favorites_existing_book_success() -- если книга есть в словаре, то функция добавляет книгу в список favorites
   - test_add_book_in_favorites_not_existing_book_failure() -- если книги нет в словаре, то функция не добавляет книгу в список favorites

8. delete_book_from_favorites(name)
   - test_delete_book_from_favorites_existing_book_success() -- Если книга есть в словаре, то функция удаляет книгу из favorites
   
9. get_list_of_favorites_books()
   - test_get_list_of_favorites_books_no_favorite_books_returns_empty_list() -- Если список избранных книг пустой, то функция возвращает пустой список
   - test_get_list_of_favorites_books_have_favorite_books_returns_favorites_list() -- Если список избранных книг непустой, то функция возвращает пустой список
