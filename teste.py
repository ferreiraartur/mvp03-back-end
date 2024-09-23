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
    


    category model:
    #courses = relationship('Course', backref='category', lazy=True)


    course model:
    #category = Column(String(200))
    #category_id = Column(Integer, ForeignKey('category_catalog.pk_category'), nullable=False)
