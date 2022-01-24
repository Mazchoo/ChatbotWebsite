from django.db.models import Model
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import pdb

from main.globalParams import *


class ChatBot(Model):
    name         = models.CharField(max_length=20)
    path         = models.CharField(max_length=20)
    icon_name    = models.TextField(null=True)
    public_vocab = models.JSONField(null=True)

    def __str__(self):
        return self.name


class ChatLog(Model):
    author       = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    text_content = models.JSONField(null=True)
    name         = models.CharField(max_length=MAX_TITLE_LENGTH)

    def __str__(self):
        return 'User - {}: Title - {}'.format(self.author, self.name)


class VocabAlteration(Model):
    author      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name        = models.CharField(max_length=MAX_TITLE_LENGTH)
    bot         = models.ForeignKey(ChatBot, on_delete=models.CASCADE)
    alterations = models.JSONField(null=True)

    def __str__(self):
        return 'Vocab - {}: Bot - {}'.format(self.name, self.bot)


class UserProfileInfo(Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    nr_stories  = models.PositiveIntegerField(default=0)
    nr_vocabs   = models.PositiveIntegerField(default=0)
    profile_pic = models.ImageField(blank=True, upload_to='profilePics')

    def __str__(self):
        if 'user' in self.__dict__.keys():
            return self.user.username
        else:
            return 'empty user info'
