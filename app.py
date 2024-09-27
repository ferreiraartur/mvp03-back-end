from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask,flash, request, redirect, url_for, render_template, send_file
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from models import Session, Course, Category, Cupom
from logger import logger
from schemas import *
from flask_cors import CORS
from config import Config
app2 = Flask(__name__)
app2.config.from_object(Config)
from werkzeug.utils import secure_filename
import os
import io

info = Info(title="API Back-End", version="1.0.0")
app = OpenAPI(__name__,info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
course_tag = Tag(name="Curso", description="Adição, visualização e remoção de cursos à base")
category_tag = Tag(name="Category", description="Adição, visualização e remoção de categorias à base")
cupom_tag = Tag(name="Cupom", description="Adição, visualização e remoção de cupons à base")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#@app.put('/course', tags=[course_tag],
#         responses={"200": CourseSchema, "409": ErrorSchema, "400": ErrorSchema})
#def update_course(form: CourseSchema):
#     """ Atualiza um Curso à base de dados
#     """
#     print (form)
#     logger.info(f"Atualizando o curso de nome:")
#     try:
          


@app.post('/course', tags=[course_tag],
          responses={"200": CourseSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_course(form: CourseSchema):
    """ Adiciona um novo Curso à base de dados

    Retorna uma representação dos cursos associados.
    """
   
    print(form)
    logger.info(f"Adicionando o curso de nome:")
    
    try:
          #if not os.path.exists(app.config['UPLOAD_FOLDER']):
             #  os.makedirs(app.config['UPLOAD_FOLDER'])
          if  'file' not in request.files:
               flash('no file part')
               return redirect(request.url)
          file = request.files['file']
          # if user does not select file, browser also
          # submit an empty part without filename
          if file.filename == '':
               flash('No selected file')
               return redirect(request.url)
          if file and allowed_file(file.filename):
               print('Testando')
               print (file.filename)
               
               # salvar o arquivo
               filename = secure_filename(file.filename)
               print ("filename",filename)
               filepath = os.path.join(app2.config['UPLOAD_FOLDER'], filename)
               print ("filepath",filepath)
               #file.save(filepath)
               print (filename)
               print (filepath)


               image_data = file.read()
               print ("teste image",image_data)

               
               course = Course(
                    title=form.title,
                    price=form.price,
                    content=form.content,
                    imageURL=form.imageURL,
                    filename=filename,
                    filepath=filepath,
                    image_data=image_data        
               )
    
               
               print ("teste", course)
               
               # conexão com a base

               session = Session()
               # adicionar curso
               session.add(course)
               # adiciona o curso na tabela
               session.commit()
               logger.info("Adicionado curso: %s"% course)
               return apresenta_course(course), 200
    except IntegrityError as e:
          # como a duplicidade do nome é a provável razão do IntegrityError
          error_msg = "Curso de mesmo nome já salvo na base :/"
          logger.warning(f"Erro ao adicionar curso , {error_msg}")
          return {"mesage": error_msg}, 409   
    except Exception as e:
               # caso um erro fora do previsto
               error_msg = "Não foi possível salvar novo curso :/"
               logger.warning(f"Erro ao adicionar curso, {error_msg}")
               return {"mesage": error_msg}, 400


@app.get('/courses', tags=[course_tag],
         responses={"200": CoursesListSchema, "404": ErrorSchema})
def get_courses():
     """Faz a busca por todos os courses cadastrados

     Retorna uma representação da listagem de courses.
     """
     logger.info(f"Listing courses ")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     courses = session.query(Course).all()

     if not courses:
          # se não há courses cadastrados
          return {"courses": []}, 200
     else:
        logger.info(f"%d courses econtrados" % len(courses))
        # retorna a representação de produto
        return apresenta_courses(courses), 200
     
@app.get('/images',tags=[course_tag],
         responses={"200": CourseViewSchema, "404": ErrorSchema})
def get_file(query: FindCourseByIdSchema):
    
     course_id = query.id
     logger.info(f"Coletando dados sobre course #{course_id}")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     course = session.query(Course).filter(Course.id == course_id).first()
     return send_file(io.BytesIO(course.image_data), mimetype='image/jpeg')


@app.get('/course', tags=[course_tag],
         responses={"200": CourseViewSchema, "404": ErrorSchema})
def get_course(query: FindCourseByIdSchema):
     """Faz a busca por um Course a partir do id do course
        Retorna uma represetação dos courses.
     """
     course_id = query.id
     logger.info(f"Coletando dados sobre course #{course_id}")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     course = session.query(Course).filter(Course.id == course_id).first()
     

     if not course:
          # se o course não foi encontrado
          error_msg = "Course não encontrado na base :/"
          logger.warning(f"Erro ao buscar course: %s" % course)
          # retora a representação de course
          return {"mesage": error_msg}, 404
     else:
          logger.info("Course encontrado: %s" % course)
          # retorna a representação de course
          return apresenta_course(course), 200


@app.delete('/course', tags=[course_tag],
            responses={"200": CourseDelSchema, "404": ErrorSchema})
def del_course(query: FindCourseByIdSchema):
     """Deleta um Course a partir do id informado
     
        Retorna uma mensagem de confirmação da remoção.
     """
     course_id = query.id
     logger.info(f"Deletando dados sobre course #course_title")
     # criando conexão com a base
     session = Session()
     # fazendo a remoção
     count = session.query(Course).filter(Course.id == course_id).delete()
     session.commit()

     if count:
          # retorna a representaçã da mensagem de confirmação
          logger.info(f"Deletado course #{course_id}")
          return {"mesage": "Course removido", "id": course_id}
     else:
          # se o course não foi encontrado
          error_msg = "Course não encontrado na base :/"
          logger.warning(f"Erro ao deletar course #'{course_id}', {error_msg}")
          return {"mesage": error_msg}, 404


@app.get('/find_course', tags=[course_tag],
         responses={"200": CoursesListSchema, "404": ErrorSchema})
def find_course(query: FindCourseBySchema):
      """Faz a busca por courses em que o termo passando  Course a partir do id do course

            Retorna uma representação dos courses    
      """
      termo = unquote(query.termo)
      logger.info(f"Fazendo a busca por title com o termo: {termo}")
      # criando conexão com a base
      session = Session()
      # fazendo a remoção
      courses = session.query(Course).filter(Course.title.ilike(f"%{termo}%")).all()

      if not courses:
           # se não há courses cadastrados
           return {"courses": []}, 200
      else:
           logger.info(f"%d courses encontrados" % len(courses))
           # retorna a representação de course
           return apresenta_courses(courses), 200

######################## Category ###############################

@app.post('/category', tags=[category_tag],
          responses={"200": CategorySchema, "409": ErrorSchema, "400": ErrorSchema})
def add_category(form: CategorySchema):
    """Adiciona uma nova categoria à base de dados

    Retorna uma representação das categorias associados.
    """
    
    logger.debug(f"Adicionando categoria")
    
    try:
        if 'file' not in request.files:
             flash ('no file part')
             return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
             flash ('No selected file')
             return redirect(request.url)
        if file and allowed_file(file.filename):
             image_category = file.read()    
             print ("teste image",image_category)
        category = Category(
        name=form.name,
        description=form.description,
        image_category=image_category
        )
        # criando conexão com a base
        session = Session()
        # adicionando categoria
        session.add(category)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado categoria ")
        return apresenta_categoria(category), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Category de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar categoria , {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar categoria ', {error_msg}")
        return {"mesage": error_msg}, 400
    

#@app.get('/category', tags=[category_tag],
#         responses={"200": CategoryViewSchema, "404": ErrorSchema})
#def get_category(query: FindCategoryByIdSchema):
#     """Faz a busca por uma categoria a partir do id do categoria
#        Retorna uma represetação das categorias.
#     """
#     category_id = query.id
#     logger.info(f"Coletando dados sobre categoria #{category_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     category = session.query(Category).filter(Category.id == category_id).first()
     

#     if not category:
#          # se a categoria não foi encontrado
#          error_msg = "Categoria não encontrado na base :/"
#          logger.warning(f"Erro ao buscar categoria: %s" % category)
#          # retora a representação de categoria
#          return {"mesage": error_msg}, 404
#     else:
#          logger.info("Category encontrado: %s" % category)
#          # retorna a representação de course
#          return apresenta_categoria(category), 200
     

@app.get('/categories', tags=[category_tag],
         responses={"200": CategoriesListSchema, "404": ErrorSchema})
def get_categories():
     """Faz a busca por todos as categorias cadastrados

     Retorna uma representação da listagem de categorias.
     """
     logger.info(f"Listing categorias ")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     categories = session.query(Category).all()

     if not categories:
          # se não há courses cadastrados
          return {"categories": []}, 200
     else:
        logger.info(f"%d categorias econtrados" % len(categories))
        # retorna a representação de categoria
        return apresenta_categoria(categories), 200
     

@app.delete('/category', tags=[category_tag],
            responses={"200": CategoryDelSchema, "404": ErrorSchema})
def del_category(query: FindCategoryByIdSchema):
     """Deleta uma categoria a partir do id informado
     
        Retorna uma mensagem de confirmação da remoção.
     """
     category_id = query.id
     logger.info(f"Deletando dados sobre category #cupom_title")
     # criando conexão com a base
     session = Session()
     # fazendo a remoção
     count = session.query(Category).filter(Category.id == category_id).delete()
     session.commit()

     if count:
          # retorna a representaçã da mensagem de confirmação
          logger.info(f"Deletado category #{ category_id}")
          return {"mesage": "Category removido", "id": category_id}
     else:
          # se o category não foi encontrado
          error_msg = "Category não encontrado na base :/"
          logger.warning(f"Erro ao deletar cupom #'{category_id}', {error_msg}")
          return {"mesage": error_msg}, 404



##################### Cupom ######################################

@app.get('/cupons', tags=[category_tag],
         responses={"200": CupomListSchema, "404": ErrorSchema})
def get_cupons():
     """Faz a busca por todos os cupons cadastrados

     Retorna uma representação da listagem de cupons.
     """
     logger.info(f"Listing cupons ")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     cupons = session.query(Cupom).all()

     if not cupons:
          # se não há courses cadastrados
          return {"cupons": []}, 200
     else:
        logger.info(f"%d cupons econtrados" % len(cupons))
        # retorna a representação de promotion
        return apresenta_cupons(cupons), 200


@app.post('/cupom', tags=[cupom_tag],
          responses={"200": CupomSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cupom(form: CupomSchema):
    """Adiciona um novo cupom à base de dados

    Retorna uma representação das cupons associadas.
    """
    cupom = Cupom(
        name=form.name,
        discount=form.discount,
        valid=form.valid)
    logger.debug(f"Adicionando cupom de nome: '{cupom.name}'")
    try:
        
        # criando conexão com a base
        session = Session()
        # adicionando pagamento
        session.add(cupom)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado promotion de nome: '{cupom.name}'")
        return apresenta_cupom(cupom), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Promotion de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar promotion '{cupom.name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar promotion '{cupom.name}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.put('/cupom', tags=[cupom_tag],
          responses={"200": CupomSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_cupom(query: FindCupomByIdSchema, form: CupomSchema):
    """Atualiza a cupom

    Retorna uma representação das cupons associadas.
    """    

    try:
        cupom_id = query.id
        logger.debug(f"Coletando dados sobre cupom#{cupom_id}")

        # criando conexão com a base
        session = Session()

        cupom = session.query(Cupom).filter(Cupom.id == cupom_id).first()
        cupom.name = form.name 
        cupom.discount = form.discount
        cupom.valid = form.valid

        session.commit()
        logger.debug(f"Adicionado cupom de nome: '{cupom.name}'")
        return apresenta_cupom(cupom), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cupom de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cupom '{cupom.name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cupom '{cupom.name}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/cupom', tags=[cupom_tag],
            responses={"200": CupomDelSchema, "404": ErrorSchema})
def del_cupom(query: FindCupomByIdSchema):
     """Deleta uma cupom a partir do id informado
     
        Retorna uma mensagem de confirmação da remoção.
     """
     cupom_id = query.id
     logger.info(f"Deletando dados sobre cupom #cupom_title")
     # criando conexão com a base
     session = Session()
     # fazendo a remoção
     count = session.query(Cupom).filter(Cupom.id == cupom_id).delete()
     session.commit()

     if count:
          # retorna a representaçã da mensagem de confirmação
          logger.info(f"Deletado cupom #{ cupom_id}")
          return {"mesage": "Cupom removido", "id": cupom_id}
     else:
          # se o cupom não foi encontrado
          error_msg = "Cupom não encontrado na base :/"
          logger.warning(f"Erro ao deletar cupom #'{cupom_id}', {error_msg}")
          return {"mesage": error_msg}, 404
     

@app.get('/cupom', tags=[cupom_tag],
         responses={"200": CupomSchema, "404": ErrorSchema})
def get_cupom(query: FindCupomBySchema):
    """Faz a busca por um cupom a partir do nome do cupom

    Retorna uma representação dos cupons.
    """
    cupom_name = unquote(unquote(query.code))
    print(cupom_name)
    logger.debug(f"Coletando dados sobre cupom #{cupom_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cupom = session.query(Cupom).filter(Cupom.name == cupom_name).first()

    if not cupom:
        # se a cupom não foi encontrado
        error_msg = "Cupom não encontrado na base :/"
        logger.warning(f"Erro ao buscar cupom '{cupom_name}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cupom econtrado: '{cupom.name}'")
        # retorna a representação da promoção
        return apresenta_cupom(cupom), 200
     























  
