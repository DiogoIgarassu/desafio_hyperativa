from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import CadastraoCartao
from .models import LoteCartoes


class LoteCartoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteCartoes
        fields = '__all__'


class CadastrarCartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastraoCartao
        fields = ['numero']


class UserSerializer(serializers.ModelSerializer):
    super = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        error_messages = {
            'email': {
                'required': "E-mail é obrigatório.",
            }
        }

    def create(self, validated_data):
        print("OPA", validated_data)
        is_superuser = validated_data.pop('super', False)

        if is_superuser:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        print('\033[91m', "AQUIIIII", User.objects.all())
        user = User.objects.filter(email=email).first()
        print('\033[93m', email, user)
        if user is None:
            raise AuthenticationFailed('Credenciais inválidas, '
                                       'tente novamente')

        if not user.check_password(password):
            raise AuthenticationFailed('Credenciais inválidas, '
                                       'tente novamente')

        if not user.is_active:
            raise AuthenticationFailed('Conta desativada, entre '
                                       'em contato com o administrador')

        if not user.is_verified:
            raise AuthenticationFailed('Email não está verificado')

        user.last_login = timezone.now()
        user.save()

        return {
            'username': user.username,
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens,
        }
