from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from config import host, user, password, db_name

Base = declarative_base()


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


student_course_relation = Table(
    'studentcourserelation', Base.metadata,
    Column('student_id', Integer, ForeignKey('studentmodel.id')),
    Column('course_id', Integer, ForeignKey('coursemodel.id'))
)

db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
engine = create_engine(db_url, echo=True)
Base.metadata.create_all(engine)
