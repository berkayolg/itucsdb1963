import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS PEOPLE (
    P_ID SERIAL PRIMARY KEY,
    NAME VARCHAR(100),
    EMAIL VARCHAR(120),
    PHOTO VARCHAR(120)
)""",

    """CREATE TABLE IF NOT EXISTS BUILDINGS (
    BU_ID SERIAL PRIMARY KEY,
    BU_NAME VARCHAR(100),
    BU_CODE VARCHAR(5)
)""",

    """CREATE TABLE IF NOT EXISTS FACULTIES (
    FAC_ID SERIAL PRIMARY KEY,
    FAC_NAME VARCHAR(100) NOT NULL,
    FAC_BUILDING INTEGER,
    FOREIGN KEY (FAC_BUILDING) REFERENCES BUILDINGS(BU_ID)
)""",

    """CREATE TABLE IF NOT EXISTS DEPARTMENTS (
    DEP_ID SERIAL PRIMARY KEY,
    DEP_NAME VARCHAR(100),
    FACULTY INTEGER,
    BUILDING INTEGER,
    DEAN INTEGER,
    FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID),
    FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID),
    FOREIGN KEY (DEAN) REFERENCES PEOPLE(P_ID)
)""",

    """CREATE TABLE IF NOT EXISTS ROOMS (
    ROOM_ID SERIAL PRIMARY KEY,
    BUILDING INTEGER,
    ROOM_NAME VARCHAR(10) UNIQUE NOT NULL,
    CAP INTEGER NOT NULL,
    CLASS BOOLEAN,
    LAB BOOLEAN,
    ROOM BOOLEAN,
    FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID)
    )""",

    """CREATE TABLE IF NOT EXISTS LABS (
    LAB_ID SERIAL PRIMARY KEY,
    LAB_NAME VARCHAR(100) UNIQUE,
    DEPARTMENT INTEGER,
    FACULTY INTEGER,
    BUILDING  INTEGER,
    ROOM INTEGER,
    FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID),
    FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID),
    FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID),
    FOREIGN KEY (ROOM) REFERENCES ROOMS(ROOM_ID)
)""",

    """CREATE TABLE IF NOT EXISTS ASSISTANTS (
    AS_ID SERIAL PRIMARY KEY,
    AS_PERSON INTEGER NOT NULL,
    LAB INTEGER,
    DEGREE VARCHAR(10),
    FOREIGN KEY (AS_PERSON) REFERENCES PEOPLE(P_ID),
    FOREIGN KEY (LAB) REFERENCES LABS(LAB_ID)
)""",

    """CREATE TABLE PAPERS (
    PAPER_ID SERIAL PRIMARY KEY,
    CONFERENCE VARCHAR(100),
    CITATION_COUNT INTEGER DEFAULT 0,
    AUTHOR INTEGER,
    FOREIGN KEY (AUTHOR) REFERENCES PEOPLE(P_ID)
)""",

    """CREATE TABLE CLUBS (
    CLUB_ID SERIAL PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    FACULTY INTEGER,
    ADVISOR INTEGER,
    CHAIRMAN INTEGER,
    V_CHAIRMAN_1 INTEGER,
    V_CHAIRMAN_2 INTEGER,
    FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID),
    FOREIGN KEY (ADVISOR) REFERENCES PEOPLE(P_ID),
    FOREIGN KEY (CHAIRMAN) REFERENCES PEOPLE(P_ID),
    FOREIGN KEY (V_CHAIRMAN_1) REFERENCES PEOPLE(P_ID),
    FOREIGN KEY (V_CHAIRMAN_2) REFERENCES PEOPLE(P_ID)
)""",

    """CREATE TABLE IF NOT EXISTS INSTRUCTORS(
    INS_ID SERIAL PRIMARY KEY,
    DEPARTMENT INTEGER,
    ROOM INTEGER UNIQUE,
    LAB INTEGER,
    FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID),
    FOREIGN KEY (ROOM) REFERENCES ROOMS(ROOM_ID),
    FOREIGN KEY (LAB) REFERENCES LABS(LAB_ID)
    )""",

    """CREATE TABLE IF NOT EXISTS CLASSES(
    CL_ID SERIAL PRIMARY KEY,
    BUILDING INTEGER,
    FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID)
    )""",

    """CREATE TABLE IF NOT EXISTS LESSONS (
    LESSON_ID SERIAL PRIMARY KEY,
    CAP INTEGER,
    ENROLLED INTEGER,
    DATE INTEGER,
    CRN INTEGER UNIQUE NOT NULL,
    CODE VARCHAR(5),
    INSTRUCTOR INTEGER,
    LOCATION INTEGER, 
    ASSISTANT INTEGER,
    CREDIT INTEGER,
    FOREIGN KEY (INSTRUCTOR) REFERENCES INSTRUCTORS(INS_ID),
    FOREIGN KEY (ASSISTANT) REFERENCES ASSISTANTS(AS_ID),
    FOREIGN KEY (LOCATION) REFERENCES CLASSES(CL_ID)
    )""",
    """CREATE TABLE IF NOT EXISTS STUDENTS (
    STU_ID INTEGER PRIMARY KEY,
    NUMBER INTEGER,
    EARNED_CREDITS INTEGER,
    DEPARTMANT INTEGER NOT NULL,
    FACULTY INTEGER NOT NULL,
    CLUB INTEGER,
    LAB INTEGER,
    FOREIGN KEY (STU_ID) REFERENCES PEOPLE,
    FOREIGN KEY (DEPARTMANT) REFERENCES DEPARTMANTS,
    FOREIGN KEY (FACULTY) REFERENCES FACULTIES,
    FOREIGN KEY (CLUB) REFERENCES CLUBS,
    FOREIGN KEY (LAB) REFERENCES LABS
    )"""

]


def initialize(url):
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
            cursor.close()
    except Exception as err:
        print("Error: ", err)


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
