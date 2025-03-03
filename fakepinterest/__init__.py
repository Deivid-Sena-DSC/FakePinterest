# AQUI VOCÊ CRIA SEU APP, AS CONFIGURAÇÕES DO APP 
# E O BANCO DE DADOS DO APP

from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

#AQUI VOCÊ CRIA O APLICATIVO
app = Flask(__name__)

# AQUI VOCÊ CONFIGURA O SEU BANCO DE DADOS 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# AQUI O NOME DA VARIAVEL QUE SERÁ SEU BANCO DE DADOS
database = SQLAlchemy(app)

#CRIANDO UMA CHAVE SECRETA ULTILIZADA PADA CODIFICAR A SENHA 
app.config["SECRET_KEY"] = "7013cdac4620e3c095d9888a870a363f"

#CONFIGURANDO O CAMINHO PARA UPLOAD DE FOTOS
app.config['UPLOAD_FOLDER'] = "static/fotos_post"

#CRIANDO A ENCRIPTAÇÃO DO SITE COM O BCRYPT
# bcrypt FAZ A CRIPTOGRAFIA DA SENHA  
bcrypt = Bcrypt(app)

# AQUI VOCÊ DEFINE PARA ONDE O USUARIO SERÁ DIRECIONADO
# CASO ELE TENTE ENTRAR EM UM PAGINA QUE EXIJA ESTAR LOGADO
login_manager = LoginManager(app)
login_manager.login_view = "home"

from fakepinterest import routes