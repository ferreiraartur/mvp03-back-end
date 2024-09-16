from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask,flash, request, redirect, url_for, render_template, send_file
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from models import Session, Course
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.put('/category')


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
                    category=form.category,
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
      

     































  
