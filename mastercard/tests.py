from django.test import TestCase
from .models import User, CadastraoCartao, LoteCartoes
from rest_framework.exceptions import AuthenticationFailed
from .serializers import (
    UserSerializer,
    LoginSerializer,
    CadastrarCartaoSerializer,
    LoteCartoesSerializer
)


class UserSerializerTest(TestCase):
    def test_create_user(self):
        # Criar um usuário normal
        data = {'username': 'test_user', 'email': 'test@example.com',
                'password': 'test_password'}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('test_password'))

    def test_create_superuser(self):
        # Criar um super usuário
        data = {'username': 'super_user', 'email': 'super@example.com',
                'password': 'super_password', 'super': True}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'super_user')
        self.assertEqual(user.email, 'super@example.com')
        self.assertTrue(user.check_password('super_password'))
        self.assertTrue(user.is_superuser)


class LoginSerializerTest(TestCase):
    def test_login_valid_credentials(self):
        User.objects.create_user(username='test_user',
                                 email='test@example.com',
                                 password='test_password')
        data = {'email': 'test@example.com', 'password': 'test_password'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['username'], 'test_user')
        self.assertEqual(validated_data['email'], 'test@example.com')

    def test_login_invalid_credentials(self):
        data = {'email': 'nonexistent@example.com',
                'password': 'wrong_password'}
        serializer = LoginSerializer(data=data)
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)


class CadastrarCartaoSerializerTest(TestCase):
    def test_cadastrar_cartao(self):
        # Testar cadastro de cartão
        data = {'numero': '1234567890123456'}
        serializer = CadastrarCartaoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        card = serializer.save()
        self.assertIsNotNone(card)
        self.assertEqual(card.numero, '1234567890123456')


class LoteCartoesSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        email='test@example.com')

    def test_lote_cartoes(self):
        # Testar serialização de lote de cartões
        data = {'usuario': self.user.pk, 'quantidade': 10, 'nome': 'Teste',
                'data': '20220101', 'numero': '0001'}
        serializer = LoteCartoesSerializer(data=data)
        if not serializer.is_valid():
            print('\033[94m', serializer.errors)
        self.assertTrue(serializer.is_valid())
        lote = serializer.save()
        self.assertIsNotNone(lote)
        self.assertEqual(lote.nome, 'Teste')
        self.assertEqual(lote.data, '20220101')  # Verifique o formato da data
        self.assertEqual(lote.numero, '0001')


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser', email='test@example.com',
            password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com',
            password='adminpassword')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class CadastraoCartaoModelTest(TestCase):
    def test_create_cadastrao_cartao(self):
        cadastrao_cartao = CadastraoCartao.objects.create(
            numero='1234567890123456', lote='00000001')
        self.assertEqual(cadastrao_cartao.numero,
                         '1234567890123456')
        self.assertEqual(cadastrao_cartao.lote,
                         '00000001')


class LoteCartoesModelTest(TestCase):
    def test_create_lote_cartoes(self):
        user = User.objects.create_user(
            username='testuser', email='test@example.com',
            password='testpassword')
        lote_cartoes = LoteCartoes.objects.create(
            usuario=user, quantidade=10, nome='Teste',
            data='20220506', numero='00000001')
        self.assertEqual(lote_cartoes.usuario, user)
        self.assertEqual(lote_cartoes.quantidade, 10)
        self.assertEqual(lote_cartoes.nome, 'Teste')
        self.assertEqual(lote_cartoes.data, '20220506')
        self.assertEqual(lote_cartoes.numero, '00000001')
