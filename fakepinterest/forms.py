# AQUI VOCÊ CRIA AS CLASSES COM OS FORMULÁRIOS
from flask_wtf import FlaskForm
from fakepinterest import bcrypt
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario


# FORMULÁRIO DE LOGIN
# PASSANDO O FlasForm PARA A CLASSE PARA INFORMAR QUE É UM FORMULARIO DO FLASK
class FormLogin(FlaskForm):
    # OS VALIDATOR VOCÊ PARSSA DENTRO DO PARENTESES
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_login = SubmitField("Fazer Login")

    def validate_senha(self, field):
        # VERIFICA SE O USUÁRIO EXISTE NO BANCO DE DADOS
        usuario = Usuario.query.filter_by(email=self.email.data).first()
       
        # ERROU SE O USUÁRIO NÃO EXISTIR
        if not usuario:
            raise ValidationError('Usuário inexistente, crie uma conta.')
                 
        # ERRO SE A SENHA ESTIVER INCORRETA
        if not bcrypt.check_password_hash(usuario.senha, field.data):
            raise ValidationError('Senha incorreta.')

                 
# FORMULÁRIO CRIAR CONTA
class FormCriarConta(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confimacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo('senha')])
    botao_criarconta = SubmitField("Criar Conta")

    #FUNÇÃO PARA VALIDAR O EMAIL
    def validate_email(self, email):
        # email.data RETORNA O VALOR INSERIDO NO FORMULÁRIO 
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            # RETORNA UMA MENSAGEM DE ERRO SE A VARIAVEL USUÁRIO ENCONTRAR ALGUM EMAIL
            raise ValidationError('Email já cadastrado. Faça Login para continuar')


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_foto = SubmitField('Enviar')