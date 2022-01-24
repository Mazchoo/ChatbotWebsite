from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core import validators

from main.models import *
from main.htmlCleaner.RemoveHTMLTags import *

from tinymce.widgets import TinyMCE

import pdb
from enum import Enum


class Content(Enum):
    pgraph  = 'pgraph'
    chapter = 'chapter'
    title   = 'title'


class TinyMCEComponent(ModelForm):

    text_content = forms.CharField(widget=TinyMCE(
        attrs={'cols': 80, 'rows': 30, 'required': False}
    ), max_length=MAX_PARAGRAPH_LENGTH)

    class Meta:
        model = ChatLog
        fields = '__all__'


class ChatBotLogEditor(ModelForm):

    class Meta:
        model = ChatLog
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) == 0:
            raise forms.ValidationError("Story name must be atleast one char.")

        return name


class VocabAlterationForm(ModelForm):

    class Meta:
        model = VocabAlteration
        fields = '__all__'


class CreateNewUser(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateNewVocab(ModelForm):
    '''
        Use the command form.save(commit=True) to save a
        validated form as the underlying model in the database.

        "fields = '__all__'" is the same as same as "exclude = []"
    '''

    class Meta:
        model = VocabAlteration
        fields = '__all__'


class ChangeProfileInfo(ModelForm):

    class Meta:
        model  = UserProfileInfo
        fields = ['profile_pic']


class ChatInput(Form):
    last_sentence = forms.CharField(max_length=MAX_INPUT_SENTENCE_LENGTH)
    chatbot_name  = forms.CharField(max_length=20)
    temperature   = forms.CharField(max_length=3)
    vocab_id      = forms.IntegerField(required=False)
    user_id       = forms.IntegerField(required=False)

    def clean_last_sentence(self):
        sentence = self.cleaned_data['last_sentence']

        return removeAllTags(sentence)

    def clean_chatbot_name(self):
        bot_name = self.cleaned_data['chatbot_name']

        for chat_bot in ChatBot.objects.all():
            if bot_name == chat_bot.path:
                return bot_name

        raise forms.ValidationError("Chatbot name is not valid.")

    def clean_temperature(self):
        temperature = self.cleaned_data['temperature']

        if not temperature.isnumeric():
            raise forms.ValidationError("Temperature is not numeric.")

        temperature = float(temperature)
        if temperature < 10.:
            raise forms.ValidationError("Temperature is too low.")
        if temperature > 100.:
            raise forms.ValidationError("Temperature is too high.")

        return temperature / 100.

    def clean(self):
        all_clean_data = super().clean()

        if all_clean_data["vocab_id"] and all_clean_data["vocab_id"] >= 0:
            vocab_id = all_clean_data["vocab_id"]

            if not VocabAlteration.objects.filter(id=vocab_id).exists():
                raise forms.ValidationError("Unknown vocab alteration.")

            vocab_alteration = VocabAlteration.objects.get(id=vocab_id)

            bot_name = all_clean_data['chatbot_name']
            bot_id = ChatBot.objects.get(path=bot_name).id
            if bot_id != vocab_alteration.bot_id:
                raise forms.ValidationError("Vocabulary bot does not match.")

            if all_clean_data["user_id"] != vocab_alteration.author_id:
                raise forms.ValidationError("Vocabulary not owned by user.")
            all_clean_data["vocab_alteration"] = vocab_alteration


class ChatParagraph(Form):

    text_content = forms.CharField(
        max_length=MAX_PARAGRAPH_LENGTH + PARAGRAPH_LENGTH_LEYWAY + 4,
        min_length=4,
    )

    def clean_text_content(self):
        text = self.cleaned_data['text_content']
        text = removeSquareBrackets(text)
        text = removeScriptTag(text)
        text = removeHTMLTag(text)

        return text


class ChatChapter(Form):

    text_content = forms.CharField(max_length=CHAPTER_MAX_LENGTH, min_length=4)

    def clean_text_content(self):
        text = self.cleaned_data['text_content']
        text = removeSquareBrackets(text)
        text = removeScriptTag(text)

        return text


class ChatTitle(Form):

    title = forms.CharField(max_length=MAX_TITLE_LENGTH, min_length=4)

    def clean_title(self):
        title = self.cleaned_data['title']
        title = removeSquareBrackets(title)
        title = removeAllTags(title)

        if len(title) == 0:
            raise forms.ValidationError("Title is not valid.")

        return title


class ChatExists(Form):

    text_content = forms.CharField(max_length=5, min_length=4)

    def clean(self):
        all_clean_data = super().clean()
        if 'text_content' not in all_clean_data.keys():
            raise forms.ValidationError("Exists cannot be parsed.")
        existOk = all_clean_data['text_content']

        try:
            existOk = existOk[0].upper() + existOk[1:]
            existBool = eval(existOk)
        except:
            raise forms.ValidationError("Exists cannot be parsed.")

        if not type(existBool) == bool:
            raise forms.ValidationError("Exists is not boolean.")

        all_clean_data['exists_okay'] = existBool


class VocabTitle(Form):

    title = forms.CharField(max_length=MAX_TITLE_LENGTH, min_length=1)

    def clean_title(self):
        title = self.cleaned_data['title']
        title = removeAllTags(title)

        if len(title) == 0:
            raise forms.ValidationError("Title is not valid.")

        return title


class ChatSaveContent(Form):
    name = forms.CharField(max_length=25)

    def clean(self):
        all_clean_data = super().clean()
        if 'name' not in all_clean_data.keys():
            raise forms.ValidationError('Invalid name for save content.')

        name = all_clean_data['name']
        names = getParagraphTypeIndex(name)

        if len(names) != 1 or len(names[0]) != 2:
            raise forms.ValidationError('Unidentified save content type.')

        contentType, contentInd = names[0]
        if contentType not in Content.__members__:
            raise forms.ValidationError('Save content invalid type.')

        all_clean_data['content_type']  = contentType
        all_clean_data['content_index'] = contentInd


class WordAlteration(Form):
    base_word   = forms.CharField(min_length=10)
    new_word    = forms.CharField(max_length=MAX_WORD_SIZE, min_length=5)

    def clean_new_word(self):
        word = self.cleaned_data['new_word']
        word = word[2:-2]

        if not checkValidUserWord(word):
            raise forms.ValidationError("Word contains invalid characters.")

        return word

    def clean_base_word(self):
        word = self.cleaned_data['base_word']

        if word[:7] != "content":
            raise forms.ValidationError('Not part of save content.')

        word = word[8:-1]

        if not checkValidUserWord(word):
            raise forms.ValidationError('Word contains invalid characters.')

        return word

    def clean(self):
        all_clean_data = super().clean()

        if 'base_word' not in all_clean_data.keys():
            raise forms.ValidationError("Base word is missing.")

        if 'new_word' not in all_clean_data.keys():
            raise forms.ValidationError("New word is missing.")

        if all_clean_data['base_word'] == all_clean_data['new_word']:
            raise forms.ValidationError("Base word and new word are the same.")


class SavedStory(Form):
    story_id = forms.IntegerField()

    def clean(self):
        all_clean_data = super().clean()
        if 'story_id' not in all_clean_data.keys():
            raise forms.ValidationError("Story Id not specified.")
        story_id = all_clean_data['story_id']

        if not ChatLog.objects.filter(id=story_id).exists():
            raise forms.ValidationError("Story refered to does not exist.")

        all_clean_data['story'] = ChatLog.objects.get(id=story_id)


class SavedVocab(Form):
    vocab_id = forms.IntegerField()

    def clean(self):
        all_clean_data = super().clean()
        if 'vocab_id' not in all_clean_data.keys():
            raise forms.ValidationError("Vocab Id not specified.")
        vocab_id = all_clean_data['vocab_id']

        if not VocabAlteration.objects.filter(id=vocab_id).exists():
            raise forms.ValidationError("Vocab refered to does not exist.")

        all_clean_data['vocab'] = VocabAlteration.objects.get(id=vocab_id)
