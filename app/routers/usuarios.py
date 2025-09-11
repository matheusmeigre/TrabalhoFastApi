# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, Body
from ..models import UsuarioLogin, UsuarioCadastro, UsuarioUpdate
from ..auth import get_usuario, gerar_hash, autenticar_usuario, criar_token, get_usuario_atual
from ..database import usuarios
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from ..viacep import buscar_cep


router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/test")
def test():
    return {"mensagem": "OK, tudo certo!"}

#Endpoint GET para listar todos os usuários
@router.get("/listar")
def listar_todos_usuarios():
    lista_usuarios = []
    for usuario in usuarios.find():
        usuario_dict = dict(usuario)
        usuario_dict.pop("password", None)
        usuario_dict.pop("_id", None)
        lista_usuarios.append(usuario_dict)
    return lista_usuarios

#Endpoint PUT para alterar dados de um usuário específico, de menos o username
@router.put("/editar/{username}")
def editar_usuario(username: str, usuario: UsuarioUpdate, dados: dict = Body(...)):
    if "username" in dados:
        raise HTTPException(status_code=400, detail="Não é permitido alterar o username.")
    usuario = usuarios.find_one({"username": username})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if "password" in dados:
        dados["password"] = gerar_hash(dados["password"])
    usuarios.update_one({"username": username}, {"$set": dados})
    return {"mensagem": "Dados do usuário atualizados com sucesso!"}

#Endpoint DELETE para excluir um usuário, exceto o usuário que está atualmente logado
@router.delete("/deletar/{username}")
def deletar_usuario(username: str, token: str):
    usuario_logado = get_usuario_atual(token)
    if not usuario_logado:
        raise HTTPException(status_code=401, detail="Token inválido ou usuário não autenticado.")
    if usuario_logado["username"] == username:
        raise HTTPException(status_code=403, detail="Não é permitido excluir o usuário atualmente logado.")
    resultado = usuarios.delete_one({"username": username})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"mensagem": f"Usuário '{username}' excluído com sucesso."}

@router.post("/registro")
def registrar(usuariox: UsuarioCadastro):
#def registrar(usuariox: UsuarioCadastro, usuario=Depends(get_usuario_atual)):
    userData = get_usuario(usuariox.username)
    if userData:
        raise HTTPException(status_code=400, detail='Usuário já existe')
    hash_senha = gerar_hash(usuariox.password)

    dadosCep = buscar_cep(usuariox.cep)
    # chamar o viacep
    # adicionar no insert_one os demais dados
    usuarios.insert_one({
        "username":usuariox.username, 
        "password": hash_senha,
        "cep": usuariox.cep,
        "numero": usuariox.numero,
        "complemento": usuariox.complemento,
        "logradouro": dadosCep["logradouro"],
        "bairro": dadosCep["bairro"],
        "localidade": dadosCep["localidade"],
        "uf": dadosCep["uf"],
        })

    return {"mensagem": "Usuário registrado com sucesso!"} 

@router.post("/login")
def logar(usuario: UsuarioLogin):
    autenticado = autenticar_usuario(usuario.username, usuario.password)

    if not autenticado:
        raise HTTPException(status_code=400, detail='Usuário ou Senha Inválidos')

    access_token = criar_token(
        data={"sub":autenticado["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"token": access_token, "expires": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)} 