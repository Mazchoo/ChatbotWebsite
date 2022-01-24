import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatBotWebsite.settings')
cwd = 'D:/Websites/StoryWebsite'
sys.path[0] = cwd

import django
django.setup()

from main.models import ChatBot
from main.corpusModels.corpusGeneratorFactory import CorpusGeneratorFactory

bot_names = {
    'movie_dialog': 'Movie Dialogue',
    'lord_of_ring': 'Lord of the Rings',
}
bot_icons = {
    'movie_dialog': 'cloak.png',
    'lord_of_ring': 'ring.png',
}

os.chdir(cwd)
corpus_factory = CorpusGeneratorFactory()

if __name__ == '__main__':
    ChatBot.objects.all().delete()
    for bot_name, corpus_generator in corpus_factory:

        chatbot_fields = {
            'name': bot_names[bot_name],
            'path': bot_name,
            'icon_name': bot_icons[bot_name],
            'public_vocab': corpus_generator.vocab,
        }

        chatbot = ChatBot.objects.get_or_create(**chatbot_fields)[0]
        chatbot.save()
