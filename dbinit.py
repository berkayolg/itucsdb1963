import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE FACULTIES (
    FAC_ID SERIAL PRIMARY KEY,
    FAC_NAME VARCHAR(100) NOT NULL,
    BUILDING_CODE VARCHAR(5) UNIQUE NOT NULL
)""",
    """CREATE TABLE ASSISTANTS (
    AS_ID SERIAL PRIMARY KEY,
    AS_NAME VARCHAR(100) NOT NULL,
    DEPARTMENT VARCHAR(100) NOT NULL,
    LAB VARCHAR(100),
    LECTURE INTEGER,
    EMAIL VARCHAR(80) UNIQUE NOT NULL,
    FOREIGN KEY LECTURE REFERENCES LECTURES(LEC_ID),
    FOREIGN KEY LAB REFERENCES LABS(LAB_ID)
)""",
    """CREATE TABLE LABS (
    LAB_ID SERIAL PRIMARY KEY,
    LAB_NAME VARCHAR(100) UNIQUE,
    DEPARTMENT VARCHAR(100),
    CLUBS VARCHAR(100),
    FACULTY INTEGER,
    BUILDING  INTEGER,
    ROOM INTEGER,
    FOREIGN KEY BUILDING REFERENCES BUILDINGS(BUILD_ID),
    FOREIGN KEY ACADEMIC REFERENCES ACADEMICS(AC_ID),
    FOREIGN KEY FACULTY REFERENCES FACULTIES(FAC_ID)
)""",
    """CREATE TABLE DEPARTMENTS (
    DEP_ID SERIAL PRIMARY KEY,
    DEP_NAME VARCHAR(100),
    FACULTY INTEGER,
    BUILDING INTEGER,
    FOREIGN KEY BUILDING REFERENCES BUILDINGS(BUILD_ID),
    FOREIGN KEY FACULTY REFERENCES FACULTIES(FAC_ID)
)""",
    "INSERT INTO FACULTIES VALUES ('Computer and Informatics Engineering Faculty', 'EEB')",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
