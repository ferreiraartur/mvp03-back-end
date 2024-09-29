from pydantic import BaseModel, Base64Bytes
from typing import Optional, List
from models.course import Course


class CourseSchema(BaseModel):
    """ Define como um novo course vai ser inserido e representado
    """
    
    title: str = "Docker Certified Associate"
    price: str = "29.99"
    content: str = "content"
    file: Base64Bytes = "Image"
    #imageURL: str = "/src/assets/courses/docker.png"
    #category: str = "DevOps"
    #image_data: str = "image"
    #category_id: int


class CourseViewSchema(BaseModel):
    """ Define como um novo course vai ser inserido e representado
    """
    title: str = "Docker Certified Associate"
    price: str = "29.99"
    content: str = "content"
    #category_id: int
    #imageURL: str = "/src/assets/courses/docker.png"
    #category: str = "DevOps"


class FindCourseBySchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do course.
    """
    termo: str = "Docker"


class FindCourseByIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apen com base no ID do course.
    """
    id: int = "1"


class CoursesListSchema(BaseModel):
    """ Define como uma listagem de courses será retornada.
    """
    courses:List[CourseViewSchema]


def apresenta_courses(courses: List[Course]):
    """ Retorna uma representação do course seguindo o schema definido em ListagemCoursesSchema.
    """
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title,
            "price": course.price,
            "content": course.content,
            #"imageURL": course.imageURL,
            #"category": course.category,
            #"filename": course.filename,
            #"filepath": course.filepath,
            #"image_data": course.image_data,
        })
    
    return {"courses": result}


#class CourseViewSchema(BaseModel):
#    """ Define como um course será retornado: course
#    """
#    id: int = 1
#    title: str = ""


class CourseDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int


def apresenta_course(course: Course):
    """ Retorna uma representação do course seguindo o schema definido em
        Course
    """
    return {
        "id": course.id,
        "title": course.title,
        "price": course.price,
        "content": course.content,
        #"imageURL": course.imageURL,
        #"category": course.category
    }





