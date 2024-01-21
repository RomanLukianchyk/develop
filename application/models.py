from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from config import host, user, password, db_name

Base = declarative_base()
db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
engine = create_engine(db_url, echo=True)

class GroupModel(Base):
    __tablename__ = 'groupmodel'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('StudentModel', back_populates='group')


class CourseModel(Base):
    __tablename__ = 'coursemodel'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('StudentModel', secondary='studentcourserelation', back_populates='courses')


class StudentModel(Base):
    __tablename__ = 'studentmodel'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groupmodel.id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    group = relationship('GroupModel', back_populates='students')
    courses = relationship('CourseModel', secondary='studentcourserelation', back_populates='students')


class StudentCourseRelation(Base):
    __tablename__ = 'studentcourserelation'

    student_id = Column(Integer, ForeignKey('studentmodel.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('coursemodel.id'), primary_key=True)
