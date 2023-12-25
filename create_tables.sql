-- Создание таблицы GroupModel
CREATE TABLE GroupModel (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

-- Создание таблицы StudentModel
CREATE TABLE StudentModel (
    id serial PRIMARY KEY,
    group_id integer REFERENCES GroupModel(id),
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL
);

-- Создание таблицы CourseModel
CREATE TABLE CourseModel (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

CREATE TABLE StudentCourseRelation (
    student_id INTEGER REFERENCES StudentModel(id),
    course_id INTEGER REFERENCES CourseModel(id),
    PRIMARY KEY (student_id, course_id)
);
