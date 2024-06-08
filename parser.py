import re
import requests
from bs4 import BeautifulSoup

from database.cruds.theme.crud import ThemeCRUD
from database.cruds.author.crud import AuthorCRUD
from database.cruds.comment.crud import CommentCRUD


class Parser:
    def __init__(self, main_url):
        self.url = main_url
        self.session = requests.Session()

    def fetch_html(self, url: str = None):
        print(f'Fetching HTML from {self.url}')
        response = self.session.get(url if url else self.url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def parse_pages_number(html: str) -> int:
        print(f'Parsing pages numbers from {html}')
        soup = BeautifulSoup(html, 'html.parser')
        number = soup.find_all(class_='nav_page')
        return int(number[-2].text) if len(number) > 1 else 1

    def parse_topics(self, pages_number: int = 1):
        for page in range(pages_number):
            print(f'Parsing topics from page {page}')
            html = self.fetch_html(f'{self.url}.{page*20}')
            soup = BeautifulSoup(html, 'html.parser')
            topics = soup.find_all(class_='windowbg')

            for topic in topics:
                print(f'Parsing topic {topic}')
                topic_head = topic.find(id=re.compile('^msg_')).find('a')

                topic_author = topic.find(class_='floatleft').find('a')
                topic_author_id = int(topic_author['href'].split(';u=')[1])
                topic_author_name = topic_author.text

                if not AuthorCRUD().find_one(id=topic_author_id):
                    print(f'adding author {topic_author_name}')
                    AuthorCRUD().insert(id=topic_author_id, name=topic_author_name)

                topic_href = topic_head['href']
                topic_title = topic_head.text
                topic_id = int(topic_href.split('topic=')[1][:-2])

                print(f'adding theme {topic_id}')
                ThemeCRUD().insert(id=topic_id, name=topic_title)

                self.parse_topic_messages(topic_href, topic_id)

    def parse_topic_messages(self, url: str, theme: int):
        print(f'Parsing topic messages from {url}')
        page_html = self.fetch_html(url)
        pages_number = self.parse_pages_number(page_html)

        for page in range(pages_number):
            print(f'Parsing topic messages from page {page}')
            html = self.fetch_html(f'{url[:-2]}.{page*15}')
            soup = BeautifulSoup(html, 'html.parser')
            comments = soup.find_all(class_='windowbg')
            for comment in comments:
                print(f'Parsing data from {comment}')
                poster = comment.find('div', class_='poster').find('a')
                poster_id = int(poster['href'].split(';u=')[1])
                poster_name = poster.text

                if not AuthorCRUD().find_one(id=poster_id):
                    print(f'adding author {poster_id}')
                    AuthorCRUD().insert(id=poster_id, name=poster_name)

                post = comment.find('div', {'class': 'post'})
                post_id = int(comment['id'][3:])
                post_text = post.text.strip()

                post_quote = None
                if answer := post.find('cite'):
                    if 'href' not in str(answer):
                        continue
                    post_quote = int(answer.find('a')['href'].split('msg=')[1])

                print(f'adding post data {post_id}')
                CommentCRUD().insert(id=post_id,
                                     theme_id=theme,
                                     author_id=poster_id,
                                     quote_id=post_quote,
                                     comment_text=post_text)
