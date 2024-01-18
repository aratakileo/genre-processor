from typing import Sequence


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
    'super power': 'superpower',
    'dementia': 'madness',
    'reincarnation': 'isekai',

    # RU
    'психология': 'психологическое',
    'супер сила': 'суперсила',
    'фэнтэзи': 'фэнтези',
    'сёнен': 'сёнэн',
    'сенен': 'сёнэн',
    'сёдзе': 'сёдзё',
    'седзе': 'сёдзё',
    'bl': 'сёнэн-ай',
    'сёнен-ай': 'сёнэн-ай',
    'сенен-ай': 'сёнэн-ай',
    'gl': 'сёдзё-ай',
    'сёдзе-ай': 'сёдзё-ай',
    'седзе-ай': 'сёдзё-ай',
    'сэйнен': 'сэйнэн',
    'сейнен': 'сэйнэн',
    'дзёсей': 'дзёсэй',
    'дзесей': 'дзёсэй',
    'сверхестественное': 'сверхъестественное',
    'гг женщина': 'главная героиня',
    'гг мужчина': 'главный герой',
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


def get_genres(text: str) -> tuple[str]:
    text = text.lower()

    for ignorable_genre in ignorable_genre_prefixes:
        text = text.replace(ignorable_genre, '')

    for old_substr, new_substr in wrong_genre_name_to_correct.items():
        text = text.replace(old_substr, new_substr)

    found_genres = []

    for genre in [*genre_names.keys(), *genre_names.values()]:
        if genre not in text:
            continue

        if genre in derived_genre_names and (
                derived_genre := derived_genre_names[genre]
        ) in text and (
                derived_genre_index := text.index(derived_genre)
        ) != -1 and derived_genre_index == text.index(genre):
            continue

        found_genres.append(genre)

    return *found_genres,


def get_direction_by_genres(genres: Sequence[str]):
    has_bl = has_gl = False

    if 'shounen ai' in genres or 'сёнэн-ай' in genres or 'yaoi' in genres or 'яой' in genres:
        has_bl = True

    if 'shoujo ai' in genres or 'сёдзё-ай' in genres or 'yuri' in genres or 'юри' in genres:
        has_gl = True

    if has_bl and has_gl:
        return 'Mixed'

    if has_bl:
        return 'BL'

    if has_gl:
        return 'GL'

    return 'Hetero'


def convert_genres(genres: Sequence[str], to_lang='en') -> tuple[str]:
    found_genres = []

    for en_genre, ru_genre in genre_names.items():
        if en_genre not in genres and ru_genre not in genres:
            continue

        found_genres.append(en_genre if to_lang == 'en' else ru_genre)

    return *found_genres,


def display_genres(genres: Sequence[str], from_lang='en'):
    if not genres:
        return ''

    output_text = ''

    for genre in genres:
        output_text += ', '

        if from_lang == 'en':
            output_text += genre.title()
        else:
            output_text += genre.capitalize()

    return output_text[2:]


def display_data(source_text: str):
    genres = get_genres(source_text)

    print('Intended direction:', get_direction_by_genres(genres))

    en_genres = display_genres(convert_genres(genres, 'en'), 'en')
    ru_genres = display_genres(convert_genres(genres, 'ru'), 'ru')

    print('Genres [EN]:', en_genres if en_genres else '-')
    print('Genres [RU]:', ru_genres if ru_genres else '-')


is_reading_genres = False
inputted_text = ''

print(
    'Welcome to the Genre Processor!\n\n'
    'How to use:\n'
    '- just insert the list of genres in any form '
    '(with the exception of no more than one newline between the elements)\n'
    '- to start processing, enter double newline (press enter twice)\n'
    '- to apply new genres to an already formed list, insert a `+` before the new input\n'
    '- to exit the program, enter newline (press enter) without any other input\n'
)

while True:
    if not is_reading_genres:
        print('Insert input below:')

    inputted_value = input().strip()

    if inputted_value.startswith('+'):
        inputted_text += inputted_value

        is_reading_genres = True
    elif not inputted_value:
        if not is_reading_genres:
            inputted_text = ''

        if inputted_text:
            display_data(inputted_text)

        is_reading_genres = False
    else:
        if not is_reading_genres:
            inputted_text = ''

        is_reading_genres = True
        inputted_text += inputted_value

    if not inputted_text:
        exit()
