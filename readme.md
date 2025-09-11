# Calculadora FastAPI

## Instruções para rodar a API

1. Instale as dependências:
	 ```bash
	 pip install -r requirements.txt
	 ```
2. Execute o servidor:
	 ```bash
	 uvicorn app.main:app --reload
	 ```

## Endpoints e exemplos de requisições

### Registro de usuário
- **POST /usuarios/registro**
```json
{
	"username": "usuario1",
	"password": "senha123",
	"cep": "01001-000",
	"numero": "123",
	"complemento": "Apto 1"
}
```

### Login (gera token)
- **POST /usuarios/login**
```json
{
	"username": "usuario1",
	"password": "senha123"
}
```
Resposta:
```json
{
	"token": "<seu_token_aqui>",
	"expires": "0:30:00"
}
```

### Listar todos os usuários (sem token)
- **GET /usuarios/listar**

### Editar dados de um usuário (com token)
- **PUT /usuarios/editar/{username}**
Headers: `JWT`
Body:
```json
{
	"password": "novaSenha",
	"cep": "01001-000",
	"numero": "456",
	"complemento": "Casa"
}
```

### Deletar usuário (com token)
- **DELETE /usuarios/deletar/{username}**
Headers: `JWT`

## Tentativa de deleção do usuário

1. Fazer login e obter o token
2. Enviar uma requisição DELETE para `/usuarios/deletar/{username}` usando o token do próprio usuário.
3. A resposta será:
```json
{
	"detail": "Não é permitido excluir o usuário atualmente logado."
}
```
# readme.md
```
calculadorav6/
| --app/
|  | --__init__.py
|  | --main.py
|  | --config.py
|  | --auth.py
|  | --database.py
|  | --models.py
|  | --routers/
|  |   | -- __init__.py
|  |   | -- calculadora.py
|  |   | -- usuarios.py
|--requirements.txt
|--readme.md
```