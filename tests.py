import pytest


class TestBooksCollector:

    @pytest.mark.parametrize(
        'book',
        [
            'Гордость и предубеждение и зомби',
            'Что делать, если ваш кот хочет вас убить',
        ]
    )
    def test_add_new_book_adds_book_without_genre(self, collector, book):
        collector.add_new_book(book)

        assert collector.get_books_genre() == {book: ''}

    def test_add_new_book_does_not_add_book_with_name_longer_than_40_characters(self, collector):
        book = 'а' * 41

        collector.add_new_book(book)

        assert collector.get_books_genre() == {}

    def test_add_new_book_does_not_add_duplicate_book(self, collector):
        book = 'Книга'

        collector.add_new_book(book)
        collector.add_new_book(book)

        assert collector.get_books_genre() == {book: ''}


    @pytest.mark.parametrize(
        'genre',
        [
            'Фантастика',
            'Ужасы',
            'Детективы',
            'Мультфильмы',
            'Комедии',
        ]
    )
    def test_set_book_genre_sets_valid_genre(self, collector, genre):
        book = 'Название книги'

        collector.add_new_book(book)
        collector.set_book_genre(book, genre)

        assert collector.get_book_genre(book) == genre

    def test_set_book_genre_does_not_set_genre_for_unknown_book(self, collector):

        collector.set_book_genre('Неизвестная книга', 'Фантастика')

        assert collector.get_books_genre() == {}

    def test_get_book_genre_returns_book_genre(self, collector):
        book = 'Марсианин'

        collector.add_new_book(book)
        collector.set_book_genre(book, 'Фантастика')

        assert collector.get_book_genre(book) == 'Фантастика'

    def test_get_books_with_specific_genre_returns_books_of_selected_genre(self, collector):
        first_book = 'Марсианин'
        second_book = 'Оно'
        third_book = 'Шерлок Холмс'

        collector.add_new_book(first_book)
        collector.add_new_book(second_book)
        collector.add_new_book(third_book)

        collector.set_book_genre(first_book, 'Фантастика')
        collector.set_book_genre(second_book, 'Ужасы')
        collector.set_book_genre(third_book, 'Детективы')

        assert collector.get_books_with_specific_genre('Ужасы') == [second_book]

    def test_get_books_genre_returns_all_books_and_their_genres(self, collector):
        first_book = 'Марсианин'
        second_book = 'Оно'

        collector.add_new_book(first_book)
        collector.add_new_book(second_book)
        collector.set_book_genre(first_book, 'Фантастика')
        collector.set_book_genre(second_book, 'Ужасы')

        assert collector.get_books_genre() == {
            first_book: 'Фантастика',
            second_book: 'Ужасы',
        }

    def test_get_books_for_children_does_not_return_age_restricted_books(self, collector):
        fantasy_book = 'Марсианин'
        horror_book = 'Оно'
        detective_book = 'Шерлок Холмс'

        collector.add_new_book(fantasy_book)
        collector.add_new_book(horror_book)
        collector.add_new_book(detective_book)

        collector.set_book_genre(fantasy_book, 'Фантастика')
        collector.set_book_genre(horror_book, 'Ужасы')
        collector.set_book_genre(detective_book, 'Детективы')

        assert collector.get_books_for_children() == [fantasy_book]

    def test_add_book_in_favorites_adds_book_only_once(self, collector):
        book = 'Марсианин'

        collector.add_new_book(book)
        collector.add_book_in_favorites(book)
        collector.add_book_in_favorites(book)

        assert collector.get_list_of_favorites_books() == [book]

    def test_delete_book_from_favorites_removes_book(self, collector):
        book = 'Марсианин'

        collector.add_new_book(book)
        collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book)

        assert collector.get_list_of_favorites_books() == []

    @pytest.mark.parametrize(
        'favorite_books',
        [
            [],
            ['Марсианин'],
            ['Марсианин', 'Оно'],
        ],
        ids=['empty', 'one_book', 'multiple_books'],
    )
    def test_get_list_of_favorites_books_returns_favorites(self, collector, favorite_books):
        for book in favorite_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        assert collector.get_list_of_favorites_books() == favorite_books
