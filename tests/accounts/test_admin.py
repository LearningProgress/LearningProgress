from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from learningprogress.accounts.models import User
from learningprogress.progress.models import Section, UserSectionRelation


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

    def test_get_using_staff_account(self):
        user = User.objects.create_user(
            username='username_eipohShied2xaeth4Eeh',
            password='password_ahxoog6nu7eer1aiSaif')
        client = Client()
        client.login(
            username='username_eipohShied2xaeth4Eeh',
            password='password_ahxoog6nu7eer1aiSaif')
        response = client.get(reverse('admin:accounts_user_changelist'))
        self.assertTemplateUsed(response, 'admin/login.html')
        user.is_staff = True
        user.save()
        response = client.get(reverse('admin:index'))
        self.assertTemplateUsed(response, 'admin/index.html')
        self.assertContains(response, 'Accounts')


class ChangeListTest(TestCase):
    """
    Tests the change list view in the admin.
    """
    def test_progress_objects_info(self):
        """
        Tests the appearance of the progress objects info column
        """
        user = User.objects.create_user(
            username='username_aibi1tahqu9eishozo5A',
            password='password_AiShee8Fibo0chu0thie')
        user.is_staff = True
        user.save()
        client = Client()
        client.login(
            username='username_aibi1tahqu9eishozo5A',
            password='password_AiShee8Fibo0chu0thie')
        section_1 = Section.objects.create(name='section_eequ7eiXoiXaid0Zai9s')
        section_2 = Section.objects.create(name='section_EeleijeiPhee4Kaef7eg')
        section_3 = Section.objects.create(name='section_Gaix9dapeen3eeshidah')
        response = client.get(reverse('admin:accounts_user_changelist'))
        self.assertContains(response, '0 / 0 / 0')
        UserSectionRelation.objects.create(user=user, section=section_1, progress=1)
        UserSectionRelation.objects.create(user=user, section=section_2, progress=2)
        UserSectionRelation.objects.create(user=user, section=section_3, progress=3)
        response = client.get(reverse('admin:accounts_user_changelist'))
        self.assertContains(response, '1 / 1 / 1')
