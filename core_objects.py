from dict import *


# Характеристики
class CFields:
	connection  = None

	def __init__(self, in_connection):
		super(CFields, self).__init__(in_connection=None)

		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
				  " ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "\
			      " ID_OBJ     INTEGER, " \
			      " field_cat  TEXT, " \
			      " field_scat TEXT, " \
			      " value      TEXT" \
			      ")".format(TABLE_OBJ_FIELDS)
			self.connection.exec_create(sql)


class CMetaField:
	connection  = None

	id_obj = ""
	cat    = ""
	scat   = ""
	value  = ""

	struct = ""

	def __init__(self, in_connection):
		super(CMetaField, self).__init__(in_connection=None)

		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection


# Объекты
class CObjects:
	connection  = None

	def __init__(self, in_connection=None):
		super(CObjects, self).__init__()

		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
			      " ID         INTEGER PRIMARY KEY NOT NULL, " \
			      " type       TEXT, " \
			      " note       TEXT, " \
			      " state      TEXT" \
			      ")".format(TABLE_OBJ_LIST)
			self.connection.exec_create(sql)


class CMetaObject:
	connection  = None

	id          = None
	note        = ""
	type        = ""
	state       = ""

	fields      = dict()

	def __init__(self, in_connection=None):
		super(CMetaObject, self).__init__()

		self.set_connection(in_connection)

	def _generate_id_(self):
		sql = "SELECT ID " \
		      "FROM {} " \
		      "ORDER BY id DESC " \
		      "LIMIT 1".format(TABLE_OBJ_LIST)
		last_id = self.connection.get_single(sql)

		if last_id is None: last_id = 0
		else:               last_id = int(last_id) + 1

		self.id = last_id

	def set_connection(self, in_connection=None):
		self.connection   = in_connection

	def set_field(self, in_field="", in_value=""):
		self.fields[in_field] = in_value

	def get_field(self, in_field=""):
		if in_field in self.fields:	return self.fields[in_field]
		else:           			return None

	def clear(self, in_clearID=False):
		self.fields = dict()
		self.note   = ""

		if in_clearID: self.id = None

	def load(self, in_id=None):
		if in_id is not None: self.id = in_id

		self.clear()

		if self.id is not None:
			sql = "SELECT type, note, state " \
			      "FROM {} " \
			      "WHERE (id='{}')".format(TABLE_OBJ_LIST, self.id)
			self.type  = self.connection.get_single(sql, 0)
			self.note  = self.connection.get_single(sql, 1)
			self.state = self.connection.get_single(sql, 2)

			sql = "SELECT field, value " \
			      "FROM {} " \
			      "WHERE (id='{}') " \
			      "ORDER BY field".format(TABLE_OBJ_FIELDS, self.id)
			fields = self.connection.get_list(sql, 0)
			values = self.connection.get_list(sql, 1)

			index = 0

			for field in fields:
				self.fields[field] = values[index]

				index += 1

	def save(self):
		self.connection.transaction_start()

		try:

			if self.id is None:
				self._generate_id_()

				sql = "INSERT INTO {} " \
				      " (ID,     note,  type, state) " \
				      "VALUES " \
				      " ('{}', '{}', '{}', '{}')".format(TABLE_OBJ_LIST, self.id, self.note, self.type, self.state)
				self.connection.exec_insert(sql)
			else:
				sql = "UPDATE {} " \
				      "SET note ='{}', " \
				      "    type ='{}'," \
				      "    state='{}' " \
				      "WHERE id ='{}'".format(TABLE_OBJ_LIST, self.note, self.type, self.state, self.id)
				self.connection.exec_update(sql)

			sql = "DELETE FROM {0} WHERE (id='{1}')".format(TABLE_OBJ_FIELDS, self.id)
			self.connection.exec_delete(sql)

			for field, value in self.fields.items():
				sql = "INSERT INTO {} (ID, field, value) VALUES ('{}', '{}', '{}')".format(TABLE_OBJ_FIELDS, self.id, field, value)
				self.connection.exec_insert(sql)

			self.connection.transaction_commit()

			return True
		except Exception as error:
			self.connection.transaction_rollback()

			return False

	def delete(self):
		self.connection.transaction_start()

		try:
			sql = "DELETE FROM fields WHERE (id='{}')".format(self.id)
			self.connection.exec_delete(sql)

			sql = "DELETE FROM meta WHERE (id='{}')".format(self.id)
			self.connection.exec_delete(sql)

			self.connection.transaction_commit()
		except:
			self.connection.transaction_rollback()


# Справочник характеристик
class CCategories:
	connection  = None

	def __init__(self, in_connection=None):
		super(CCategories, self).__init__()

		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
			      " ID         INTEGER PRIMARY KEY NOT NULL, " \
			      " type       TEXT, " \
			      " struct     TEXT, " \
			      " cat        TEXT" \
			      " scat       TEXT" \
			      ")".format(TABLE_CAT_FIELDS)
			self.connection.exec_create(sql)
