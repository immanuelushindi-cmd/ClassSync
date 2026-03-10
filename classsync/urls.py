from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home,              name='home'),
    path('create/',                       views.create_session,    name='create_session'),
    path('join/',                         views.join_session,      name='join_session'),
    path('history/',                      views.session_history,   name='session_history'),
    path('session/<str:pin>/teacher/',    views.teacher_dashboard, name='teacher_dashboard'),
    path('session/<str:pin>/student/',    views.student_room,      name='student_room'),
    path('session/<str:pin>/analytics/',  views.session_analytics, name='session_analytics'),
    path('session/<str:pin>/end/',        views.end_session,       name='end_session'),
    path('session/<str:pin>/qr/',         views.session_qr,        name='session_qr'),
    path('session/<str:pin>/submit/',     views.submit_doubt,      name='submit_doubt'),
    path('session/<str:pin>/api/',        views.live_doubts_api,   name='live_doubts_api'),
    path('session/<str:pin>/ping/',       views.presence_ping,     name='presence_ping'),
    path('doubt/<int:doubt_id>/upvote/',  views.upvote_doubt,      name='upvote_doubt'),
    path('doubt/<int:doubt_id>/answer/',  views.mark_answered,     name='mark_answered'),
]
