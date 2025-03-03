# AQUI VOCÊ CRIA A ESTRUTURA DO BANCO DE DADOS
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# CRIANDO AS CLASS PARA CRIAR AS TEBELAS DO BANCO DE DADOS É NECESSARIO PASSAR PARA CLASS
# A VARIALVEL QUE VOCÊ DEFINIU COMO NOME DO SEU BANCO DE DADOS EXEMPLO ( database.Model ) 

#CRIANDO A FUNÇÃO PARA CARREGAR O USUÁRIO É UMA FUNÇÃO OBRIGATÓRIA PARA ESTRUTURA DE LOGIN
# @login_manager.user_loader DECORATER NECESSARIO PARA FUNÇÃO LOGIN 
@login_manager.user_loader
def load_usuario(id_usuario):
    # FAZENDO A BUSCA DO id_usuario NA TABELA Usuario DO BANDO DE DADOS
    return Usuario.query.get(int(id_usuario))



# CRIANDO A TABELA USUARIO
# UserMixin INFORMA QUAL A class ("QUAL TABELA") QUE VAI GERENCIAR O LOGIN DE USUARIO   
class Usuario(database.Model, UserMixin):

    # CRIANDO AS COLUNAS 
    # COLUNA COM A CHAVE PRIMARIA
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    # COLUNA DE RELAÇÃO ENTRE AS TABELAS USUARIO E FOTO

    # NO PRIMEIRO ARGUMENTO VOCÊ DEFINE O NOME DA TABALE DE RELAÇÃO
    # NO SEGUNDO ARGUMENTO VOCÊ DEFINE O NOME DA SEGUNDA TABELA DE RELAÇÃO 
    # LAZY=TRUE SERVA PARA OTIMIZAR A BUSCA
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

# CRIANDO A TABELA FOTO
class Foto(database.Model):
    
    # CRIANDO AS COLUNAS
    # COLUNA DA CHAVE PRIMARIA
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    # AQUI VOCÊ CRIA A COLUNA QUE ARMAZENA O ID DO USUÁRIO QUE CRIOU O POST
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)