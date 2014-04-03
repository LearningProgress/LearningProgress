from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from learningprogress.accounts.models import User


class Register(TestCase):
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
        self.assertFormError(response, form='form', field='password2', errors="Passwords don't match")
        self.assertFalse(User.objects.filter(username='username_mae0weiGh2eid5keejah').exists())


class Update(TestCase):
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


class Delete(TestCase):
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
