genre_names = {
    'shounen ai': 'сёнэн-ай',
    'shounen': 'сёнэн',
    'shoujo ai': 'сёдзё-ай',
    'shoujo': 'сёдзё',
    'school': 'школа',
    'supernatural': 'сверхъестественное',
    'yaoi': 'яой',
    'yuri': 'юри',
    'isekai': 'исекай',
    'magic': 'магия',
    'action': 'экшен',
    'sci-fi': 'фантастика',
    'superpower': 'суперсила',
    'slice of life': 'повседневность',
    'comedy': 'комедия',
    'drama': 'драма',
    'romance': 'романтика',
    'fantasy': 'фэнтези',
    'psychological': 'психологическое',
    'sport': 'спорт',
    'adventure': 'приключения',
    'military': 'военное',
    'demons': 'демоны',
    'mystery': 'детектив',
    'thriller': 'триллер',
    'horror': 'ужасы',
    'harem': 'гарем',
    'martial arts': 'боевые искусства',
    'gourmand': 'гурман',
    'game': 'игры',
    'ecchi': 'этти',
    'historical': 'историческое',
    'seinen': 'сэйнэн',
    'music': 'музыка',
    'mecha': 'меха',
    'madness': 'безумие',
    'vampire': 'вампиры',
    'parody': 'пародия',
    'aristocracy': 'аристократия',
    'male main': 'главный герой',
    'female main': 'главная героиня',
    'biography': 'биография',
    'samurai': 'самураи',
    'josei': 'дзёсэй',
    'omegaverse': 'омегаверс',
    'police': 'полиция',
    'middle ages': 'средневековье',
}

wrong_genre_name_to_correct = {
    # EN
    'psycological': 'psychological',
    'psyhological': 'psychological',
    'psychology': 'psychological',
    'psyhology': 'psychological',
    'psycology': 'psychological',
    'psychologic': 'psychological',
    'psyhologic': 'psychological',
    'psycologic': 'psychological',
    'super power': 'superpower',
    'dementia': 'madness',
    'reincarnation': 'isekai',
    'bl': 'shounen ai',
    'gl': 'shoujo ai',

    # RU
    'психология': 'психологическое',
    'супер сила': 'суперсила',
    'фэнтэзи': 'фэнтези',
    'сёнен': 'сёнэн',
    'сенен': 'сёнэн',
    'сёдзе': 'сёдзё',
    'седзе': 'сёдзё',
    'гей': 'сёнэн-ай',
    'сёнен-ай': 'сёнэн-ай',
    'сенен-ай': 'сёнэн-ай',
    'сёдзе-ай': 'сёдзё-ай',
    'седзе-ай': 'сёдзё-ай',
    'сэйнен': 'сэйнэн',
    'сейнен': 'сэйнэн',
    'дзёсей': 'дзёсэй',
    'дзесей': 'дзёсэй',
    'сверхестественное': 'сверхъестественное',
    'гг женщина': 'главная героиня',
    'гг мужчина': 'главный герой',
    'ггшка': 'главная героиня',
    'гг': 'главный герой',
    'игра': 'игры',
    'мистика': 'детектив',
    'боевик': 'экшен',
    'реинкарнация': 'исекай',
    'воспоминания из другого мира': 'исекай'
}

derived_genre_names = {
    'shounen': 'shounen ai',
    'shoujo': 'shoujo ai',
    'сёнэн': 'сёнэн-ай',
    'сёдзё': 'сёдзё-ай',
}

ignorable_genre_prefixes = ('спортив',)


class GenreProcessor:
    def __init__(self, text: str):
        text = text.lower()

        for ignorable_genre in ignorable_genre_prefixes:
            text = text.replace(ignorable_genre, '')

        for old_substr, new_substr in wrong_genre_name_to_correct.items():
            text = text.replace(old_substr, new_substr)

        self._en_genres = ()

        for en_genre, ru_genre in genre_names.items():
            if en_genre not in text and ru_genre not in text:
                continue

            current_genre = ru_genre if ru_genre in text else en_genre

            if current_genre in derived_genre_names and (
                    derived_genre := derived_genre_names[current_genre]
            ) in text and (
                    derived_genre_index := text.index(derived_genre)
            ) != -1 and derived_genre_index == text.index(current_genre):
                continue

            self._en_genres = (*self._en_genres, en_genre)

    def get_direction(self):
        has_bl = has_gl = False

        if 'shounen ai' in self._en_genres or 'yaoi' in self._en_genres:
            has_bl = True

        if 'shoujo ai' in self._en_genres or 'yuri' in self._en_genres:
            has_gl = True

        if has_bl and has_gl:
            return 'Mixed'

        if has_bl:
            return 'BL'

        if has_gl:
            return 'GL'

        return 'Hetero'

    def get_genres(self, lang='en'):
        return self._en_genres if lang != 'ru' else [genre_names[genre_en] for genre_en in self._en_genres]

    def get_displayed_genres(self, lang='en'):
        genres = self.get_genres(lang)

        if not genres:
            return ''

        output_text = ''

        for genre in genres:
            output_text += ', '

            if lang != 'ru':
                output_text += genre.title()
            else:
                output_text += genre.capitalize()

        return output_text[2:]

    def get_displayed(self):
        return (
            f'Intended direction: {self.get_direction()}\n'
            f'Genres [EN]: {self.get_displayed_genres("en")}\n'
            f'Genres [RU]: {self.get_displayed_genres("ru")}'
        )


is_reading_genres = False
inputted_text = ''

print(
    'Welcome to the Genre Processor!\n\n'
    'How to use:\n'
    '- just insert the list of genres in any form '
    '(with the exception of no more than one newline between the elements)\n'
    '- to start processing, enter double newline (press enter twice)\n'
    '- to apply new genres to an already formed list, insert a `+` before the new input\n'
    '- to exit the program, enter newline (press enter) without any other input'
)

while True:
    if not is_reading_genres:
        print('\nInsert input below:')

    inputted_value = input().strip()

    if inputted_value.startswith('+'):
        inputted_text += inputted_value

        is_reading_genres = True
    elif not inputted_value:
        if not is_reading_genres:
            inputted_text = ''

        if inputted_text:
            print(GenreProcessor(inputted_text).get_displayed())

        is_reading_genres = False
    else:
        if not is_reading_genres:
            inputted_text = ''

        is_reading_genres = True
        inputted_text += inputted_value

    if not inputted_text:
        exit()
