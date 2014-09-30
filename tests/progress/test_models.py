from django.test import TestCase

from learningprogress.accounts.models import User
from learningprogress.progress.models import MockExam, MockExamBranch, Section, UserSectionRelation


class SectionTest(TestCase):
    """
    Tests Section model.
    """
    def test_str(self):
        section = Section.objects.create(name='ieGah3cheepo1kaeSuo8')
        self.assertEqual(str(section), 'ieGah3cheepo1kaeSuo8')

    def test_serialize_one(self):
        user = User.objects.create(username='username_Taey0Ieve9keipequ5ae')
        section = Section.objects.create(name='name_lee1sahh8Giem9an3jai', notes='notes_Ood3eulae2hoh4aeJie0')
        UserSectionRelation.objects.create(
            user=user,
            section=section,
            progress=3,
            comment='comment_LahhoyipieX9sei2eesh')
        self.assertEqual(
            Section.objects.get(pk=1).serialize(user=user),
            dict(
                name='name_lee1sahh8Giem9an3jai',
                scores=1,
                notes='notes_Ood3eulae2hoh4aeJie0',
                progress=3,
                comment='comment_LahhoyipieX9sei2eesh'))

    def test_serialize_two(self):
        user = User.objects.create(username='username_iiY3gas0Ai5ieBee5pha')
        Section.objects.create(name='name_mov7OhV5aishiedee5vu', notes='notes_tohyaoth9faghia5Oed0')
        self.assertEqual(
            Section.objects.get(pk=1).serialize(user=user),
            dict(
                name='name_mov7OhV5aishiedee5vu',
                scores=1,
                notes='notes_tohyaoth9faghia5Oed0',
                progress=0,
                comment=''))


class UserSectionRelationTest(TestCase):
    """
    Tests UserSectionRelation model.
    """
    def test_str(self):
        usersectionrelation = UserSectionRelation(
            user=User.objects.create(username='username_ij8Aeca3cho4eb9eph2e'),
            section=Section.objects.create(name='ahxiu7faeva0ahZooche'))
        self.assertEqual(
            str(usersectionrelation),
            'username_ij8Aeca3cho4eb9eph2e – ahxiu7faeva0ahZooche')


class MockExamTest(TestCase):
    """
    Tests MockExam model.
    """
    def test_str(self):
        mockexam = MockExam.objects.create(
            user=User.objects.create(username='username_aeju8Aemeesa0kieng5e'),
            branch=MockExamBranch.objects.create(name='branch_yie9eigh5gaega6Doogh'),
            mark=12,
            date='2013-07-20')
        self.assertEqual(
            str(mockexam),
            'username_aeju8Aemeesa0kieng5e – branch_yie9eigh5gaega6Doogh')
