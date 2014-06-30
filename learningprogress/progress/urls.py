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
    url(r'^print-comments/$',
        login_required(views.PrintCommentsView.as_view()),
        name='print_comments'),
    url(r'^mock_exams/$',
        login_required(views.MockExamFormView.as_view()),
        name='mockexam_form'),
    url(r'^mock_exams/(?P<pk>\d+)/delete/$',
        login_required(views.MockExamDeleteView.as_view()),
        name='mockexam_delete'))
