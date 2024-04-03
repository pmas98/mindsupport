from django.test import TestCase
from api.models import Usuario, Sala, Tema


class UserTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(
            email="fulaninho12221@mail.com",
            password="testpassword",
        )

    def test_user_creation(self):
        user_exists = Usuario.objects.filter(
            email="fulaninho12221@mail.com", password="testpassword"
        ).exists()
        self.assertEqual(user_exists, True)

        user = Usuario.objects.get(
            email="fulaninho12221@mail.com", password="testpassword"
        )
        user.delete()


class SaveMessageTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create(
            email="fulaninho12221@mail.com",
            password="testpassword",
        )
        Tema.objects.create(name="Teste")
        Sala.objects.create(theme=Tema.objects.get(name="Teste"))
