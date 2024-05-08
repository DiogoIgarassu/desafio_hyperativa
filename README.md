# Desafio Hyperativa

## Sobre o Desafio
Este projeto implementa uma API para a criação e consulta de números de cartões de crédito completos. A API utiliza autenticação e permite inserção de dados tanto individualmente quanto por arquivos em lote.

## Configuração do Ambiente

### Criar e Ativar o Ambiente Virtual
Para configurar um ambiente virtual Python, siga os passos abaixo no terminal:
```bash
python -m venv venv
source venv/bin/activate  # On Unix or MacOS
venv\Scripts\activate  # On Windows
```

### Rodar com Docker Compose
Para rodar o projeto usando Docker Compose, utilize o comando:
```bash
docker-compose up
```

## Acesso Local

### Criar Usuário
Para criar um usuário, acesse a rota:
```
http://127.0.0.1:8000/criar-usuario/
```
Envie um POST com o seguinte JSON:
```json
{
    "username": "novo_usuario",
    "password": "admin123",
    "email": "novo_usuario@exemplo.com",
    "super": "true"
}
```
O atributo "super": "true" indica que o usuário terá acesso ao painel administrativo.

### Login
Para fazer login, utilize a rota:
```
http://127.0.0.1:8000/login/
```
e passe o seguinte JSON:
```json
{
    "password": "admin123",
    "email": "novo_usuario@exemplo.com"
}
```
O retorno será algo como:
```json
{
    "id": 1,
    "email": "novo_usuario@exemplo.com",
    "username": "novo_usuario",
    "tokens": {
        "refresh": "<token>",
        "access": "<token>"
    }
}
```

### Cadastrar Cartões e Lotes
Utilize o token de acesso do login como Bearer Token para autenticar as seguintes operações:
- **Cadastrar cartão:** POST para `http://127.0.0.1:8000/cadastrar-cartao/` com o JSON `{"numero": "4456897912999992"}`.
- **Cadastrar lote:** POST para `http://127.0.0.1:8000/cadastrar-lote/` selecionando o arquivo em form-data.

### Consultas
- **Todos os usuários cadastrados:** GET `http://127.0.0.1:8000/usuarios`
- **Todos os cartões cadastrados:** GET `http://127.0.0.1:8000/consulta-cartoes`
- **Todos os lotes cadastrados:** GET `http://127.0.0.1:8000/consulta-lotes`

## Testes e Qualidade de Código
- **Flake8 para estilo de código:** Execute \`flake8 mastercard\`
- **Testes unitários:** Execute \`python manage.py test\`
