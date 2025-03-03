# AQUI VOCÊ CRIAS AS ROTAS OU VIEMS (links) DO SEU SITE 
from fakepinterest import app, database, bcrypt
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=["GET", "POST"])
def home():
    # A VARIAVEL formlogin PASSA A SER O FormLogin()  
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
      #FILTRANDO NO BANCO DE DADOS SE TEM O EMAIL INFORMADO NO FORMULÁRIO
      usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
      login_user(usuario, remember=True)
      return redirect(url_for("perfil", id_usuario=usuario.id))    

    return render_template("home.html", form=formlogin)



@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form_criar_conta = FormCriarConta()

    # VERIFICANDO SE O FORMULARIO CRIAR CONTA FOI PREENCHIDO E VALIDADO 
    if form_criar_conta.validate_on_submit():
        # CRIPTOGRAFANDO A SENHA
        senha_criptografada = bcrypt.generate_password_hash(form_criar_conta.senha.data)
       
        # CRIANDO A VARIAVEL QUE VAI PASSAR PARA O BANCO DE DADOS O username, senha, email
        usuario = Usuario(username=form_criar_conta.username.data,
                           senha=senha_criptografada,
                             email=form_criar_conta.email.data)
        
        # ABRINDO UMA SESSÃO NO BANCO DE DADOS PARA ADICIONAR O USUÁRIO
        database.session.add(usuario)
        # commit SALVANDO AS INFORMAÇÕES NO BANCO DE DADOS
        database.session.commit()

        # FAZENDO O LOGIN DO USUÁRIO
        login_user(usuario, remember=True)

        # REDIRECIONANDO O USUARIO PARA A PAGINA DO SEU PERFIL 
        # PARA PASSAR UM PARAMETRO PARA UM REDIRECIONAMENTO BASTA PASSAR 
        # O REDIRECIONAMENTO=PARAMENTRO EXEMPLO usuario=usuario.username
        # PARAMETRO USUÁRIO RECEBE O USUARIO.DATA QUE É O NOME PREENCHIDO NO FORMULARIO DE CRIAR CONTA
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("criarconta.html", form=form_criar_conta)



# @app.route("/perfil/<usuario>") CRIA UMA PAGINA DINAMICA
# PASSANDO <id_usuario> PASSA PARA FUNÇÃO INFORMAÇÕES DO USUARIO
@app.route("/perfil/<id_usuario>", methods=['GET', 'POST'])
@login_required
# @login_manager.user_loader IMPEDE QUE USUÁRIO ACESSE A PAGINA SE NÃO ESTIVER LOGADO
def perfil(id_usuario):
    
    # VERIFICA SE O ID DO USUÁRIO É O MESMO DO CURRENT USER
    if int(id_usuario) == int(current_user.id):
      #PASSANDO O FORMULÁRIO DE FOTO PARA VARIÁVEL
      form_foto = FormFoto()
      
      #VERIFICANDO SE O FORMULÁRIO FOTO FOI VALIDADO
      if form_foto.validate_on_submit():
        arquivo = form_foto.foto.data
        # MUDANDO O NOME DO ARQUIVO PARA UM NOME SEGURO 
        nome_seguro = secure_filename(arquivo.filename)
        #SALVAR O ARQUIVO NA PASTA FOTOS POST
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          app.config['UPLOAD_FOLDER'],
                          nome_seguro)
        arquivo.save(caminho)
        #REGISTRAR O NOME DO ARQUIVO NO BANCO DE DADOS
        foto = Foto(imagem=nome_seguro , id_usuario=current_user.id)
        database.session.add(foto)
        database.session.commit()





      return render_template("perfil.html", usuario=current_user, form=form_foto)  
    
    else:
      usuario = Usuario.query.get(int(id_usuario))
      # form = None SE O USUÁRIO NÃO ESTIVER NO PERFIL DELE NÃO CARREGA O FORMULÁRIO
      return render_template("perfil.html", usuario=usuario, form=None)


# FUNÇÃO DE LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/feed')
@login_required
def feed():
   fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
   return render_template('feed.html', fotos=fotos)

@app.route('/post/<id_post>', methods=['GET', 'POST'])
@login_required
def post(id_post):
  post = Foto.query.get(int(id_post))
  usuario = Usuario.query.filter_by(id=post.id_usuario).first()
  if request.method == "POST":
     if "excluir" in request.form:
        post_excluir = database.session.query(Foto).filter_by(id=id_post).first()
        database.session.delete(post_excluir)     
        database.session.commit()
        return redirect(url_for("perfil", id_usuario=current_user.id))       
  return render_template("post.html", post=post, usuario=usuario)
   

