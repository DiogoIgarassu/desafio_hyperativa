from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, CadastraoCartao, LoteCartoes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CadastrarCartaoSerializer
from datetime import datetime

from .serializers import UserSerializer, LoginSerializer, LoteCartoesSerializer


class CadastrarLoteView(APIView):
    def post(self, request):
        arquivo_txt = request.FILES.get('arquivo_txt')

        if not arquivo_txt:
            return Response({'error': 'Por favor, '
                                      'forneça um arquivo TXT válido.'},
                            status=status.HTTP_400_BAD_REQUEST)

        num_cartoes = []

        for i, linha in enumerate(arquivo_txt):
            if i == 0:
                cabecalho = linha.strip().decode()
                nome = cabecalho[0:29]
                data = cabecalho[29:37]
                data_formatada = datetime.strptime(
                    data, '%Y%m%d').strftime('%d-%m-%Y')
                lote = cabecalho[41:45]
            else:
                numero_cartao = linha[7:27].strip().decode()
                if len(numero_cartao) > 10:
                    print('\033[91m', numero_cartao)
                    num_cartoes.append(numero_cartao)

        for numero_cartao in num_cartoes:
            CadastraoCartao.objects.create(numero=numero_cartao,
                                           lote=lote)

        lote = LoteCartoes.objects.create(
            usuario=request.user,
            quantidade=len(num_cartoes),
            nome=nome,
            data=data_formatada,
            numero=lote
        )

        serializer = LoteCartoesSerializer(lote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def criar_usuario(request):
    data = request.data.copy()
    super_user = data.pop('super', None)
    if super_user:
        super_user = super_user.lower() == 'true'

    data['super'] = super_user
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        if (User.objects.filter(email=email).exists() or
                User.objects.filter(username=username).exists()):
            return Response({'error': 'O email ou nome de usuário já existe'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_usuarios(request):
    usuarios = User.objects.all()
    print("AQUIIIII", User.objects.all())
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)


class LoginAPIView(generics.GenericAPIView):
    """ classe utlizada para fazer login e
    fornecer o token de acesso ao usuário """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CadastrarCartaoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CadastrarCartaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
