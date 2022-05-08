import os
from jinja2 import Environment, select_autoescape, FileSystemLoader

TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(
    loader=FileSystemLoader(TEMPLATE_ROOT),
    autoescape=select_autoescape(['html', 'xml'])
)


def get_html(data, file_name):
    template = env.get_template(file_name)
    rendered = template.render(data)

    with open('templates/test.html', 'w', encoding='UTF-8') as file:
        file.write(rendered)
    return rendered


data_confirm_email = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_for_confirm_email',
    'user': 'Иван иванович Иванов'
}
data_bookmarks = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_new_series',
    'user': 'Иван петрович Иванов',
    'serial_name': 'Санта-Барбара'
}
data_individual_letter = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_new_series',
    'user': 'Иван васильевич Иванов',
    'message_body': 'Здесь может быть любая чушь от менеджера'
}

data_personal_selection = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_new_series',
    'user': 'Иван михайлович Иванов',
    'selection': 'Здесь должна быть крутая подборка'
}

data_tip = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_new_series',
    'user': 'Иван геннадьевич Иванов',
    'movie_name': 'Грань будущего II',
    'poster': 'Картинка, описание и т.п.',
    'link_movie': 'link_to_movie'
}

data_statistics = {
    'link_out': 'https://pastseason.ru/',
    'link': 'this_is_link_new_series',
    'user': 'Иван сергеевич Иванов',
    'count_movies': '13',
    'count_serials': '7',
    'month': 'мае',
    'count_films': '11',
    'count_genre_max': '9',
    'genre_max': 'фантастика'
}

# играться строго по очереди. Не более одного принта за раз. Результать смотреть в браузере: test.html

# print(get_html(data_confirm_email, 'welcome.html'))
# print(get_html(data_bookmarks, 'bookmarks.html'))
# print(get_html(data_individual_letter, 'mail.html'))
# print(get_html(data_personal_selection, 'personal_selection.html'))
# print(get_html(data_tip, 'tip.html'))
print(get_html(data_statistics, 'statistics.html'))
