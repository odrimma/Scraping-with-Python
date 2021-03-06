import json

from bs4 import BeautifulSoup

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re
def get_data(url):
   data_list = []
   # Проходимся с 1 по 9 странице, можно больше, но итак работет не очень быстро)))
   for item in range(1, 10):
      # Проверяем на наличие на сервере такой страницы и в принципе на наличие такого сервера
      try:
         html = urlopen(url + f'page{item}/')
      except HTTPError as e:
         return None
      except URLError as e:
         print('The server could not be found!')
         return None
      bs = BeautifulSoup(html.read(), 'html.parser')
      # Находим всех родителей, т.е. блоки со статьями
      perents = bs.find_all('article', {'class':'tm-articles-list__item'})
      # Проходим по всем родителям и получаем нужную нам информацию: автор статьи, название публикации, ссылка на статью и тэги статьи
      for perent in perents:
         autor = perent.find('span', {'class':'tm-user-info tm-article-snippet__author'})
         pub_name = perent.find('h2', {'class':'tm-article-snippet__title tm-article-snippet__title_h2'})
         Href = perent.find('a', {'class': 'tm-article-snippet__title-link'})
         tegs_list = []
         # Ищем только те статьи, в которых присутствует тэг - Python
         if perent.find('a', {'class': 'tm-article-snippet__hubs-item-link', 'href': re.compile('[/\S]+(Python|python)')}):
            tegs = perent.find_all('a', {'class': 'tm-article-snippet__hubs-item-link'})
            for teg in tegs:
               tegs_list.append('https://habr.com' + str(teg.attrs['href']).strip())
         if autor and pub_name and Href and tegs_list:
            data_list.append({
               'Автор': str(autor.text.strip()),
               'Название': str(pub_name.text.strip()),
               'Ссылка': 'https://habr.com' + str(Href.attrs['href'].strip()),
               'Тэги': tegs_list
            })
   return data_list

data_list = get_data('https://habr.com/ru/all/')

# Записываем в json
with open('result.json', 'a', encoding="utf-8") as file:
   json.dump(data_list, file, indent=4, ensure_ascii=False)

