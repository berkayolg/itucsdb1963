Parts Implemented by Uğur Ali Kaplan
================================

*****************
Assistants
*****************

.. note:: All table creations exist in db_init.py file.

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~~~~~

This is how Assistants table is defined in the database. As we are holding foreign keys, it is impossible to
create an assistant entry before having the right values for foreign key attributes. Related information 
about how to create entries for those tables can be found in the other parts of this documentation.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS ASSISTANTS (
        AS_ID SERIAL PRIMARY KEY,
        AS_PERSON INTEGER NOT NULL,
        LAB INTEGER,
        DEGREE VARCHAR(10),
        DEPARTMENT INTEGER,
        FACULTY INTEGER,
        FOREIGN KEY (AS_PERSON) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (LAB) REFERENCES LABS(LAB_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Assistant Class
~~~~~~~~~~~~~~~~~~~~~~~~

Since it makes it easier to create, we have defined an assistant class for creating an entry into our database.
Therefore, before adding a new assistant an object of class Assistant must be initialized. Here is the definition of
the Assistant class:

.. code-block:: python

    class Assistant:
        def __init__(self, person, lab, degree, department, faculty):
            self.person = person
            self.lab = lab
            self.degree = degree
            self.department = department
            self.faculty = faculty


Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

Adding an assistant into the database is pretty straigthforward. You have to pass the object you have initialized
into add_assistant() function.

.. code-block:: python

   def add_assistant(self, assistant):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [assistant.person, assistant.lab, assistant.degree, assistant.department, assistant.faculty]
                statement = "INSERT INTO ASSISTANTS (AS_PERSON, LAB, DEGREE, DEPARTMENT, FACULTY) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add assistant Error: ", err)


Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

It turns out, reading assistants is not as straigthforward as creating an entry. There are multiple options.

**Option 1: get_assistant**

get_assistant takes assistant id as input and returns a dictionary. It also returns assistant's name, email and photo from people
table.

.. code-block:: python

   def get_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (a.as_id, p.name, p.email, p.photo, a.degree, a.as_person, a.lab, a.department, a.faculty) FROM assistants a JOIN people p ON a.as_person = p.p_id WHERE a.as_id = %s"
                data = [as_id]
                cursor.execute(statement, data)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Email": datum[2].strip('"'),
                        "Photo": datum[3].strip('"'),
                        "Degree": datum[4].strip('"'),
                        "Person": int(datum[5]),
                        "Lab": int(datum[6]),
                        "Dep": int(datum[7]),
                        "Fac": int(datum[8])
                    }
                    retval.append(val)
                return retval[0]
        except Exception as err:
            print("Get assistant DB Error: ", err)

        return None

**Option 2: get_assistants**

Notice the "s" at the end of the function name. This is used to get all the assistants in the database.
It returns the query result as a list.

.. code-block:: python

   def get_assistants(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM ASSISTANTS JOIN PEOPLE ON (ASSISTANTS.as_person = PEOPLE.p_id)"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Delete assistant Error: ", err)

**Option 3: get_assistant_info**

This is a combination of get_assistant and get_assistants. It returns a list of dictionaries where each dictionary is for an
entry in the assistants table.

.. code-block:: python

    def get_assistant_info(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT (a.as_id, p.name, p.email, p.photo, a.degree) FROM assistants a JOIN people p ON a.as_person = p.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    datum = datum[0].lstrip("(").rstrip(")").split(",")
                    val = {
                        "ID": datum[0],
                        "Name": datum[1].strip('"'),
                        "Email": datum[2],
                        "Photo": datum[3],
                        "Degree": datum[4]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Assistant Info(The one with the string parsing) DB Error: ", err)

Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

To update an assistant, you have to supply assistant id, an attributes list and corresponding values. Then, using
this look-up table, corresponding entry in the database gets updated.

.. code-block:: python
	
    def update_assistant(self, as_id, attrs, values):
        attrs_lookup_table = {
            "person": "AS_PERSON",
            "lab": "LAB",
            "degree": "DEGREE",
            "department": "DEPARTMENT",
            "faculty": "FACULTY",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ASSISTANTS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE AS_ID = %s"
                values.append(as_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update assistant Error: ", err)
		
Deleting
~~~~~~~~~~~~~~~~~~~~

To delete an assistant, you have to supply assistant id.

.. code-block:: python

    def delete_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ASSISTANTS WHERE AS_ID = %s"
                values = [as_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete assistant Error: ", err)
	

*****************
Buildings
*****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS BUILDINGS (
        BU_ID SERIAL PRIMARY KEY,
        BU_NAME VARCHAR(100),
        BU_CODE VARCHAR(5),
        CAMPUS VARCHAR(20)
    )

Adding 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def add_room(self, room):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO ROOMS (BUILDING, ROOM_NAME, AVAILABLE, CLASS, LAB, ROOM) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [room.building, room.name, room.availability, room.classroom, room.lab, room.room]
                cursor.execute(statement, data)
                statement = "SELECT ROOM_ID FROM ROOMS WHERE ROOM_NAME = %s"
                data = [room.name]
                cursor.execute(statement, data)
                value = cursor.fetchall()
                room.id = value[0]
                cursor.close()
        except Exception as err:
            print("Add Room Error: ", err)
        return room

Reading 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def get_rooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT ROOM_ID, BU_NAME, ROOM_NAME FROM ROOMS JOIN BUILDINGS ON(ROOMS.BUILDING = BUILDINGS.BU_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID": data[0],
                        "Name": data[2],
                        "Building": data[1]  
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Rooms Error: ", err)
	
			
Updating 
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
	
	def update_room(self, room_id, attrs, values):
        attrs_lookup_table = {
            "building": "BUILDING",
            "room_name": "ROOM_NAME",
            "class": "CLASS",
            "lab": "LAB",
            "room": "ROOM",
            "available": "AVAILABLE"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ROOMS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE ROOM_ID = %s"
                values.append(room_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Rooms Error: ", err)
		
		
Deleting
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def delete_room(self, room_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ROOMS WHERE room_id = %s"
                values = [room_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Room Error: ", err)
	
****************
Clubs
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS CLUBS (
        CLUB_ID SERIAL PRIMARY KEY,
        NAME VARCHAR(100) NOT NULL,
        FACULTY INTEGER,
        ADVISOR INTEGER,
        CHAIRMAN INTEGER,
        V_CHAIRMAN_1 INTEGER,
        V_CHAIRMAN_2 INTEGER,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (ADVISOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (CHAIRMAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (V_CHAIRMAN_1) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (V_CHAIRMAN_2) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Adding
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

Reading
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
Updating
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

Deleting
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)

****************
Departments
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DEPARTMENTS (
        DEP_ID SERIAL PRIMARY KEY,
        DEP_NAME VARCHAR(100),
        FACULTY INTEGER,
        BUILDING INTEGER,
        DEAN INTEGER,
        FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Adding
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

Reading
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
Updating
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

Deleting
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)

****************
Faculties
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS FACULTIES (
        FAC_ID SERIAL PRIMARY KEY,
        FAC_NAME VARCHAR(100) NOT NULL,
        FAC_BUILDING INTEGER,
        DEAN INTEGER NOT NULL,
        DEAN_ASST_1 INTEGER NOT NULL,
        DEAN_ASST_2 INTEGER,
        FOREIGN KEY (FAC_BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN_ASST_1) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEAN_ASST_2) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Adding
~~~~~~~~~~~~~~~~~~~~
Before adding a classroom a room is added if not exists, with the proper values.

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

Reading
~~~~~~~~~~~~~~~~~~~~

Selecting all the values by the name in order to avoid ordering problems when giving them to attributes dictioanary.

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
Updating
~~~~~~~~~~~~~~~~~~~~

Same update process is applied to classrooms. Attribute names and their values are given parameters from the form.

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

Deleting
~~~~~~~~~~~~~~~~~~~~

.. note:: By the cascade nature if referred room is deleted the classroom is deleted. 

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)

****************
Labs
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS LABS (
        LAB_ID SERIAL PRIMARY KEY,
        LAB_NAME VARCHAR(100) UNIQUE,
        DEPARTMENT INTEGER,
        FACULTY INTEGER,
        BUILDING  INTEGER,
        ROOM INTEGER,
        INVESTIGATOR INTEGER NOT NULL,
        FOREIGN KEY (BUILDING) REFERENCES BUILDINGS(BU_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (FACULTY) REFERENCES FACULTIES(FAC_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (DEPARTMENT) REFERENCES DEPARTMENTS(DEP_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (ROOM) REFERENCES ROOMS(ROOM_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (INVESTIGATOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Adding
~~~~~~~~~~~~~~~~~~~~
Before adding a classroom a room is added if not exists, with the proper values.

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

Reading
~~~~~~~~~~~~~~~~~~~~

Selecting all the values by the name in order to avoid ordering problems when giving them to attributes dictioanary.

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
Updating
~~~~~~~~~~~~~~~~~~~~

Same update process is applied to classrooms. Attribute names and their values are given parameters from the form.

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

Deleting
~~~~~~~~~~~~~~~~~~~~

.. note:: By the cascade nature if referred room is deleted the classroom is deleted. 

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)

****************
Papers
****************

SQL Table Creation
~~~~~~~~~~~~~~~~~~~~

Private and foreign key class id refers to the room id that the class in.
.. note:: In our structure every classroom is a (inside a) room.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS PAPERS (
        PAPER_ID SERIAL PRIMARY KEY,
        TITLE VARCHAR (100),
        PLAT VARCHAR(100),
        CITATION_COUNT INTEGER DEFAULT 0,
        AUTHOR INTEGER,
        CONFERENCE BOOLEAN NOT NULL,
        FOREIGN KEY (AUTHOR) REFERENCES PEOPLE(P_ID) ON UPDATE CASCADE ON DELETE RESTRICT
    )

Adding
~~~~~~~~~~~~~~~~~~~~
Before adding a classroom a room is added if not exists, with the proper values.

.. code-block:: python

    def add_classroom(self, classroom):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                    data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                    cursor.execute(statement, data)
                    cursor.close()
            except Exception as err:
                print("Add Classroom Error: ", err)
            return classroom

Reading
~~~~~~~~~~~~~~~~~~~~

Selecting all the values by the name in order to avoid ordering problems when giving them to attributes dictioanary.

.. code-block:: python

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None
	
Updating
~~~~~~~~~~~~~~~~~~~~

Same update process is applied to classrooms. Attribute names and their values are given parameters from the form.

.. code-block:: python

	def update_classroom(self, class_id, attrs, values):
        attrs_lookup_table = {
            "type": "TYPE",
            "air_conditioner": "AIR_CONDITIONER",
            "last_restoration": "LAST_RESTORATION",
            "board_type": "BOARD_TYPE",
            "cap": "CAP"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLASSES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CL_ID = %s"
                print(statement, values)
                values.append(class_id)
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Update Classroom Error: ", err)

Deleting
~~~~~~~~~~~~~~~~~~~~

.. note:: By the cascade nature if referred room is deleted the classroom is deleted. 

.. code-block:: python

	def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)
