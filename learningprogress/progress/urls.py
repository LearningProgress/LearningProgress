from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns(
    '',
    url(r'^$',
        login_required(views.SectionListView.as_view()),
        name='section_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(views.UserSectionRelationUpdateView.as_view()),
        name='usersectionrelation_update'),
    url(r'^export/$',
        login_required(views.UserSectionRelationExportView.as_view()),
        name='usersectionrelation_export'),
    url(r'^note-cards/$',
        login_required(views.PrintNoteCardsView.as_view()),
        name='print_note_cards'),
    url(r'^mock_exams/$',
        login_required(views.MockExamFormView.as_view()),
        name='mockexam_form'),
    url(r'^mock_exams/(?P<pk>\d+)/delete/$',
        login_required(views.MockExamDeleteView.as_view()),
        name='mockexam_delete'))
