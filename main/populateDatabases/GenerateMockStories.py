import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatBotWebsite.settings')
sys.path[0] = 'D:/Websites/StoryWebsite'

import django
django.setup()

from faker import Faker
from main.models import ChatBot, ChatLog
from main.forms import Content

import random

fake_gen = Faker()


def addChatLog(nr = 5):
    for entry in range(nr):
        fake_text = '<p>' + fake_gen.text() + '</p>'
        fake_title = ' '.join(fake_gen.text().split(' ')[:3])

        text_content = {
            Content.chapter._value_ + '1': fake_title,
            Content.pgraph._value_ + '2': fake_text,
        }

        field_input = {
            'name': fake_title,
            'text_content': text_content,
            'author_id': 1,
        }

        story = ChatLog.objects.get_or_create(**field_input)[0]
        story.save()

if __name__ == '__main__':
    print('populating script...')
    addChatLog(5)
    print('population complete!')
