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
