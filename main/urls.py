from django.contrib import admin
from django.urls import path
import main.views as views

app_name = 'main'

urlpatterns = [
    path('', views.homePage, name='homepage'),
    path('login', views.logInUser, name='login'),
    path('logout', views.logOutUser, name='logout'),
    path('register', views.register, name='register'),
    path('write', views.writeStory, name='write-story'),
    path('vocab', views.selectVocabToAlter, name='alter-vocab-select'),
    path('vocab/<str:bot_path>/', views.alterVocab, name='alter-vocab'),
    path('saved', views.savedStories, name='saved-content'),
    path('loadStory', views.loadSavedStory, name='load-story'),
    path('loadVocab', views.loadSavedVocab, name='load-vocab'),
    path('ajax/talk-to/', views.talkToServer, name='talk-to'),
    path('ajax/save-story/', views.saveStory, name='save-story'),
    path('ajax/save-vocab/', views.saveVocabAlteration, name='save-vocab'),
]
