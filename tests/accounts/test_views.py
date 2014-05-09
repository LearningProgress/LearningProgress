import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.translation import ugettext as _

from learningprogress.accounts.models import ExamDate, User


class RegisterTest(TestCase):
    """
    Tests registration (UserCreateView).
    """
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('user_create'))
        self.assertTemplateUsed(response, template_name='accounts/user_create_form.html')

    def test_post_valid(self):
        exam = (timezone.now().year + 1) * 10 + 1
        response = self.client.post(
            reverse('user_create'),
            {'username': 'username_haingeixohKaik1ookie',
             'email': 'email_look8eici7Nie8bainge@example.com',
             'password1': 'password_Thookooyei3odahwiYoo',
             'password2': 'password_Thookooyei3odahwiYoo',
             'exam': str(exam)})
        self.assertRedirects(response, expected_url=reverse('home'))
        self.assertTrue(User.objects.filter(username='username_haingeixohKaik1ookie').exists())

    def test_post_invalid_password(self):
        exam = (timezone.now().year + 1) * 10 + 1
        response = self.client.post(
            reverse('user_create'),
            {'username': 'username_mae0weiGh2eid5keejah',
             'email': 'email_yiadau3ahtho4Cheelei@example.com',
             'password1': 'password_foolooMie2eireiFaeLi',
             'password2': 'invalid',
             'exam': str(exam)})
        self.assertTemplateUsed(response, template_name='accounts/user_create_form.html')
        self.assertFormError(response, form='form', field='password2', errors=_("Passwords don't match"))
        self.assertFalse(User.objects.filter(username='username_mae0weiGh2eid5keejah').exists())


class UpdateTest(TestCase):
    """
    Tests update (UserUpdateView).
    """
    def setUp(self):
        exam = (timezone.now().year - 2) * 10 + 1
        User.objects.create_user(
            username='username_eZo3xo8Eevie3Xacho9b',
            password='password_aesh6daem6sahx7aePho',
            exam=exam)
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(reverse('user_update'))
        expected_url = '%s?next=%s' % (reverse('login'), reverse('user_update'))
        self.assertRedirects(response, expected_url=expected_url)

    def test_get(self):
        self.client.login(
            username='username_eZo3xo8Eevie3Xacho9b',
            password='password_aesh6daem6sahx7aePho')
        response = self.client.get(reverse('user_update'))
        self.assertTemplateUsed(response, template_name='accounts/user_update_form.html')

    def test_post(self):
        self.client.login(
            username='username_eZo3xo8Eevie3Xacho9b',
            password='password_aesh6daem6sahx7aePho')
        exam = (timezone.now().year + 2) * 10 + 1
        response = self.client.post(
            reverse('user_update'),
            {'username': 'username_UCheengaiHohj5iequoo',
             'email': '',
             'exam': str(exam)})
        self.assertRedirects(response, expected_url=reverse('home'))
        self.assertFalse(User.objects.filter(username='username_eZo3xo8Eevie3Xacho9b').exists())
        self.assertTrue(User.objects.filter(username='username_UCheengaiHohj5iequoo').exists())

    def test_post_2(self):
        exam = (timezone.now().year - 2) * 10 + 2
        User.objects.create_user(
            username='username_ahquou3oumohSeij1foh',
            password='password_pha4equ9CieGah7bahza',
            exam=exam)
        self.client.login(
            username='username_ahquou3oumohSeij1foh',
            password='password_pha4equ9CieGah7bahza')
        response = self.client.post(
            reverse('user_update'),
            {'username': 'username_gooV4Ieloh8ojuech7Qu',
             'email': '',
             'exam': str(exam)})
        self.assertRedirects(response, expected_url=reverse('home'))
        self.assertFalse(User.objects.filter(username='username_ahquou3oumohSeij1foh').exists())
        self.assertTrue(User.objects.filter(username='username_gooV4Ieloh8ojuech7Qu').exists())

    def test_post_3(self):
        exam = (timezone.now().year + 50) * 10 + 2
        User.objects.create_user(
            username='username_oLoog9Keeh8juethi2za',
            password='password_gooV4Ieloh8ojuech7Qu',
            exam=exam)
        self.client.login(
            username='username_oLoog9Keeh8juethi2za',
            password='password_gooV4Ieloh8ojuech7Qu')
        response = self.client.post(
            reverse('user_update'),
            {'username': 'username_oR4aefiCei6teiyacheo',
             'email': '',
             'exam': str(exam)})
        self.assertRedirects(response, expected_url=reverse('home'))
        self.assertFalse(User.objects.filter(username='username_oLoog9Keeh8juethi2za').exists())
        self.assertTrue(User.objects.filter(username='username_oR4aefiCei6teiyacheo').exists())


class DeleteTest(TestCase):
    """
    Tests delete (UserDeleteView).
    """
    def setUp(self):
        User.objects.create_user(
            username='username_mieth0johy6yegouHa1y',
            password='password_Xai8eixee3ahDiehahno')
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(reverse('user_delete'))
        expected_url = '%s?next=%s' % (reverse('login'), reverse('user_delete'))
        self.assertRedirects(response, expected_url=expected_url)

    def test_get(self):
        self.client.login(
            username='username_mieth0johy6yegouHa1y',
            password='password_Xai8eixee3ahDiehahno')
        response = self.client.get(reverse('user_delete'))
        self.assertTemplateUsed(response, template_name='accounts/user_confirm_delete.html')

    def test_post(self):
        self.client.login(
            username='username_mieth0johy6yegouHa1y',
            password='password_Xai8eixee3ahDiehahno')
        response = self.client.post(reverse('user_delete'))
        self.assertRedirects(response, expected_url=reverse('home'))
        self.assertFalse(User.objects.filter(username='username_mieth0johy6yegouHa1y').exists())


@override_settings(LANGUAGE_CODE='en')
class ExamDateNoteTest(TestCase):
    """
    Tests note “Still ... days until exam.”.
    """
    def setUp_user(self):
        self.user = User.objects.create_user(
            username='username_hee3ooc7oh8Pooqu8doe',
            password='password_ooHaidoo1di9ohX5Ev4o',
            exam='20082')
        self.client = Client()
        self.client.login(
            username='username_hee3ooc7oh8Pooqu8doe',
            password='password_ooHaidoo1di9ohX5Ev4o')

    def test_str_spring(self):
        exam_date = ExamDate.objects.create(key=20141, date=datetime.date(2014,2,18))
        self.assertEqual(str(exam_date), 'Spring 2014 (2014-02-18)')

    def test_str_autumn(self):
        exam_date = ExamDate.objects.create(key=20082, date=datetime.date(2008,8,21))
        self.assertEqual(str(exam_date), 'Autumn 2008 (2008-08-21)')

    def test_get(self):
        self.setUp_user()
        exam_date = ExamDate.objects.create(key=20082, date=datetime.date(2008,8,21))
        days_object = exam_date.date - timezone.now().date()
        response = self.client.get('/progress/')
        self.assertContains(response, 'Still %d days until exam.' % days_object.days)

    def test_get_undefined(self):
        self.setUp_user()
        response = self.client.get('/progress/')
        self.assertNotContains(response, 'days until exam.')
