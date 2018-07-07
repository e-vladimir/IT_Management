from dict import *
from core_sqlite import *


# Мета-классы
class CMeta:
	connection  = TSQLiteConnection

	def __init__(self, in_connection=None):
		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

	def _init_db_(self):
		sql = "CREATE TABLE IF NOT EXISTS {0} " \
		      "(" \
		      " ID     INTEGER PRIMARY KEY ASC, " \
		      " type   TEXT, " \
		      " note   TEXT  " \
		      ")".format(TABLE_META)

		self.connection.exec_create(sql)


class CMetaFields(CMeta):
	_fields = dict
	_id_obj = ""
	
	def __init__(self, in_connection=None):
		super(CMetaFields, self).__init__(in_connection)

		self._fields = dict()
	
	def _init_db_(self):
		sql = "CREATE TABLE IF NOT EXISTS {0} " \
		      "(" \
		      " ID     INTEGER PRIMARY KEY ASC, " \
		      " ID_OBJ INTEGER, " \
		      " type   TEXT, " \
		      " value  TEXT  " \
		      ")".format(TABLE_FIELDS)

		self.connection.exec_create(sql)

	def _load_field_(self, in_id):
		self._id_obj = in_id

		sql = "SELECT " \
		      " type, " \
		      " value " \
		      "FROM {0} " \
		      "WHERE " \
		      " (id = '{1}'".format(TABLE_FIELDS, in_id)

		field_values = self.connection.get_multiple(sql)
		_type        = field_values[0]
		_value       = field_values[1]

		self._fields[_type] = _value

	def load(self, in_id_obj):
		self._id_obj = in_id_obj

		sql = "SELECT " \
		      " ID " \
		      "FROM {0} " \
		      "WHERE " \
		      " (ID_OBJ = '{1}')".format(TABLE_FIELDS, self._id_obj)

		list_id = self.connection.get_list(sql)

		self._fields = dict()

		for field_id in list_id:
			self._load_field_(field_id)

	def save(self):
		if self._id_obj is not None:
			self.connection.transaction_start()

			sql = "DELETE FROM {0} " \
			      "WHERE " \
			      " (ID_OBJ = '{1}')".format(TABLE_FIELDS, self._id_obj)
			self.connection.exec_delete(sql)

			for field in self._fields:
				sql = "INSERT INTO {0} (" \
				      " ID_OBJ," \
				      " type,  " \
				      " value )" \
				      "VALUES (" \
				      " '{1}', " \
				      " '{2}', " \
				      " '{3}' )".format(TABLE_FIELDS, self._id_obj, field, self._fields[field])
				self.connection.exec_insert(sql)

			self.connection.transaction_commit()

	def get_field(self, in_field):
		if in_field not in self._fields:
			return None
		else:
			return self._fields[in_field]

	def set_field(self, in_field, in_value=""):
		self._fields[in_field] = in_value


class CMetaObject(CMeta):
	fields = CMetaFields
	id     = None
	type   = ""
	note   = ""

	def __init__(self, in_connection=None):
		super(CMetaObject, self).__init__(in_connection)

		self.id = None

	def load(self, in_id=None):
		if in_id is not None:
			self.id = in_id

		if self.id is not None:
			sql = "SELECT " \
			      " type, note " \
			      "FROM {0} " \
			      "WHERE" \
			      " (id = {1})".format(TABLE_META, self.id)
			_data = self.connection.get_multiple(sql)

			self.type = _data[0]
			self.note = _data[1]

			self.fields.load(self.id)

	def save(self):
		if self.id is None:
			sql = "INSERT INTO {0} (" \
			      " type,  " \
			      " note)  " \
			      "VALUES (" \
			      " '{0}', " \
			      " '{1}' )".format(TABLE_META, self.type, self.note)
			self.exec_insert(sql)

			sql = "SELECT last_insert_rowid()"
			self.id = self.connection.get_single(sql)
		else:
			sql = "UPDATE {0} " \
			      "SET" \
			      " type = '{1}', " \
			      " note = '{2}' " \
			      "WHERE " \
			      " id = '{3}'".format(TABLE_META, self.type, self.note, self.id)
			self.connection.exec_updadte(sql)

		self.fields.save()
