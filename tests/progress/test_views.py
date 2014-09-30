import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from learningprogress.accounts.models import User
from learningprogress.progress.models import MockExam, MockExamBranch, Section, UserSectionRelation


class SectionListViewTest(TestCase):
    """
    Tests view with all sections (SectionListView).
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='username_biejoogheXaeh2hu8jee',
            password='password_hiXeuSh1Oohie7veeshe')
        self.client = Client()
        self.client.login(
            username='username_biejoogheXaeh2hu8jee',
            password='password_hiXeuSh1Oohie7veeshe')

    def test_get(self):
        response = self.client.get(reverse('section_list'))
        self.assertTemplateUsed(response, template_name='progress/section_list.html')

    def test_get_two_sections(self):
        section = Section.objects.create(name='ahy2ni9iixaecohwei2U')
        section2 = Section(name='oiriem0saoyiej0eiK8g')
        section2.insert_at(section, position='first-child', save=True)
        UserSectionRelation.objects.create(user=self.user, section=section, progress=1)
        response = self.client.get(reverse('section_list'))
        self.assertTemplateUsed(response, template_name='progress/section_list.html')

    def test_export_json_link(self):
        response = self.client.get(reverse('section_list'))
        self.assertContains(response, 'href="%s"' % reverse('usersectionrelation_export'))

    def test_export_note_cards_link(self):
        response = self.client.get(reverse('section_list'))
        self.assertContains(response, 'href="%s"' % reverse('print_note_cards'))


class UserSectionRelationUpdateViewTest(TestCase):
    """
    Tests view for a single relation between an user and a section
    (UserSectionRelationUpdateView).
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='username_jeir9Aec6ahgooyooVie',
            password='password_INgaxohchohs7oChugh4')
        self.client = Client()
        self.client.login(
            username='username_jeir9Aec6ahgooyooVie',
            password='password_INgaxohchohs7oChugh4')

    def test_get(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='ETh4ong7eiya6gohg7ai')
        response = self.client.get(reverse('usersectionrelation_update', kwargs={'pk': '1'}))
        self.assertTemplateUsed(response, template_name='progress/usersectionrelation_form.html')
        self.assertTrue(UserSectionRelation.objects.filter(user=self.user, section=section).exists())

    def test_post_valid(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='eeGoo7eaceiShoo1pa8a')
        response = self.client.post(
            reverse('usersectionrelation_update', kwargs={'pk': section.pk}),
            {'progress': '1',
             'comment': 'comment_ni5eothohnee3eecueXa'})
        self.assertRedirects(response, expected_url=reverse('section_list'))
        usersectionrelation = UserSectionRelation.objects.get(user=self.user, section=section)
        self.assertEqual(usersectionrelation.comment, 'comment_ni5eothohnee3eecueXa')

    def test_post_invalid(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='aGh6Quon6ich4hahngo')
        response = self.client.post(
            reverse('usersectionrelation_update', kwargs={'pk': section.pk}),
            {'progress': 'invalid',
             'comment': 'comment_reNguPiecahv4aihahQu'})
        self.assertEqual(response.status_code, 200)
        usersectionrelation = UserSectionRelation.objects.get(user=self.user, section=section)
        self.assertNotEqual(usersectionrelation.comment, 'comment_reNguPiecahv4aihahQu')

    def test_get_invalid(self):
        section = Section.objects.create(name='Aikahnareefai5toh7eZ')
        section2 = Section(name='foo5oi2AoT5equ0wei8o')
        section2.insert_at(section, position='first-child', save=True)
        response = self.client.get(reverse('usersectionrelation_update', kwargs={'pk': section.pk}))
        self.assertEqual(response.status_code, 404)

    def test_get_ajax(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='Iu1dahPai2tai0bioj2o')
        response = self.client.get(
            reverse('usersectionrelation_update', kwargs={'pk': section.pk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf8'))
        self.assertTrue('<button type="button" class="close"' in data['html'])
        self.assertTrue(UserSectionRelation.objects.filter(user=self.user, section=section).exists())

    def test_post_ajax_valid(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='AhGhai1Oim3kie3satai')
        response = self.client.post(
            reverse('usersectionrelation_update', kwargs={'pk': section.pk}),
            {'progress': '1',
             'comment': 'comment_eepoo9ae3Woo3eicheil'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response['Content-Type'], 'application/json')
        usersectionrelation = UserSectionRelation.objects.get(user=self.user, section=section)
        self.assertEqual(usersectionrelation.comment, 'comment_eepoo9ae3Woo3eicheil')

    def test_post_ajax_invalid(self):
        self.assertFalse(UserSectionRelation.objects.exists())
        section = Section.objects.create(name='ki2faecaey7Xi2ahngoh')
        response = self.client.post(
            reverse('usersectionrelation_update', kwargs={'pk': section.pk}),
            {'progress': 'invalid',
             'comment': 'comment_oc4Yei1ique3ub2PhaiM'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf8'))
        self.assertTrue(data['form_errors']['progress'])
        usersectionrelation = UserSectionRelation.objects.get(user=self.user, section=section)
        self.assertNotEqual(usersectionrelation.comment, 'comment_oc4Yei1ique3ub2PhaiM')


class UserSectionRelationExportView(TestCase):
    pass
    # TODO


class PrintNoteCardsViewTest(TestCase):
    """
    Tests view to export all user's section comments in a printable format
    (PDF).
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='username_Aej8oodoh2yawohgh5ie',
            password='password_Oo6pe0vukiethaequa6i')
        self.client = Client()
        self.client.login(
            username='username_Aej8oodoh2yawohgh5ie',
            password='password_Oo6pe0vukiethaequa6i')

    # TODO
    # def test_get(self):
        # assert False
        # section1 = Section.objects.create(name='ohh7Ohhesoot2aikae6h')
        # section2 = Section.objects.create(name='Mu2xie7ung2ea4paeC7n')
        # self.client.post(
        #     reverse('usersectionrelation_update', kwargs={'pk': section1.pk}),
        #     {'progress': '1',
        #      'comment': 'comment_iz9weng9neigoh5Jeish'})
        # response = self.client.get(reverse('print_comments'))
        # self.assertContains(response, 'ohh7Ohhesoot2aikae6h')
        # self.assertNotContains(response, 'Mu2xie7ung2ea4paeC7n')
        # self.assertContains(response, 'comment_iz9weng9neigoh5Jeish')


class MockExamFormViewTest(TestCase):
    """
    Tests view for mock exams (MockExamFormView).
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='username_ahPh1ahgheewoo2aixah',
            password='password_oni2Oishaeth9aeziugh')
        self.client = Client()
        self.client.login(
            username='username_ahPh1ahgheewoo2aixah',
            password='password_oni2Oishaeth9aeziugh')

    def test_get(self):
        response = self.client.get(reverse('mockexam_form'))
        self.assertTemplateUsed(response, template_name='progress/mockexam_form.html')

    def test_post(self):
        self.assertFalse(MockExam.objects.filter(user=self.user).exists())
        branch = MockExamBranch.objects.create(name='branch_gua4eeco5uu9ohNafani')
        response = self.client.post(
            reverse('mockexam_form'),
            {'branch': branch.pk,
             'mark': 12,
             'date': '2014-07-20'})
        self.assertRedirects(response, expected_url=reverse('mockexam_form'))
        self.assertTrue(MockExam.objects.filter(user=self.user).exists())


class MockExamDeleteViewTest(TestCase):
    """
    Tests deletion of mock exams (MockExamDeleteView).
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='username_ohkaechoomoh5oof4Rei',
            password='password_chet7ooj7uo6le2Athae')
        self.client = Client()
        self.client.login(
            username='username_ohkaechoomoh5oof4Rei',
            password='password_chet7ooj7uo6le2Athae')

    def test_get_valid(self):
        mockexam = MockExam.objects.create(
            user=self.user,
            branch=MockExamBranch.objects.create(name='branch_miThee6migei1iD4nua6'),
            mark=12,
            date='2013-07-20')
        response = self.client.get(reverse('mockexam_delete', kwargs={'pk': mockexam.pk}))
        self.assertTemplateUsed(response, template_name='progress/mockexam_confirm_delete.html')

    def test_get_invalid_1(self):
        response = self.client.get(reverse('mockexam_delete', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_2(self):
        mockexam = MockExam.objects.create(
            user=User.objects.create(username='username_ahch0xieYooc4mei9chu'),
            branch=MockExamBranch.objects.create(name='branch_Voos3xahGh7jahbahxol'),
            mark=12,
            date='2013-07-20')
        response = self.client.get(reverse('mockexam_delete', kwargs={'pk': mockexam.pk}))
        self.assertEqual(response.status_code, 403)

    def test_post_valid(self):
        mockexam = MockExam.objects.create(
            user=self.user,
            branch=MockExamBranch.objects.create(name='branch_Engaegohghe1ahgaipo5'),
            mark=12,
            date='2013-07-20')
        self.assertTrue(MockExam.objects.exists())
        response = self.client.post(
            reverse('mockexam_delete', kwargs={'pk': mockexam.pk}), {})
        self.assertRedirects(response, expected_url=reverse('mockexam_form'))
        self.assertFalse(MockExam.objects.exists())
