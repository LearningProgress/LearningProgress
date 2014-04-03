from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from learningprogress.accounts.models import User


class CreateTest(TestCase):
    """
    Tests user creation via admin.
    """
    def setUp(self):
        User.objects.create_superuser(
            username='username_Ohk8up1vae9esaerahro',
            email='email_OewooNoangeengee6pae@example.com',
            password='password_OewooNoangeengee6pae')
        self.client = Client()
        self.client.login(
            username='username_Ohk8up1vae9esaerahro',
            password='password_OewooNoangeengee6pae')

    def test_get(self):
        response = self.client.get(reverse('admin:accounts_user_add'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        response = self.client.post(
            reverse('admin:accounts_user_add'),
            {'username': 'username_zei5iejoo1vigh5Bau2x',
             'password1': 'password_Oohoo2zipaequa3dae1g',
             'password2': 'password_Oohoo2zipaequa3dae1g',
             'exam': '20082',
             '_addanother': ''})
        self.assertRedirects(response, expected_url=reverse('admin:accounts_user_add'))
        self.assertTrue(User.objects.filter(username='username_zei5iejoo1vigh5Bau2x').exists())

    def test_post_invalid(self):
        response = self.client.post(
            reverse('admin:accounts_user_add'),
            {'username': 'username_Ohk8up1vae9esaerahro',
             'password1': 'password_ahn6pu8EoWeeg0axie2O',
             'password2': 'password_ahn6pu8EoWeeg0axie2O',
             'exam': '20082',
             '_save': ''})
        self.assertContains(response, text='<p class="errornote">')
