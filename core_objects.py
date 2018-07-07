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
		      "  ID     INTEGER PRIMARY KEY ASC, " \
		      "  type   TEXT, " \
		      "  note   TEXT  " \
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
		      "  ID     INTEGER PRIMARY KEY ASC, " \
		      "  ID_OBJ INTEGER, " \
		      "  type   TEXT, " \
		      "  value  TEXT  " \
		      ")".format(TABLE_FIELDS)

		self.connection.exec_create(sql)

	def _load_field_(self, in_id):
		self._id_obj = in_id

		sql = "SELECT " \
		      "  type, " \
		      "  value " \
		      "FROM {0} " \
		      "WHERE " \
		      "  id = '{1}'".format(TABLE_FIELDS, in_id)

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

	def clear(self):
		self._fields = dict()


class CMetaObject(CMeta):
	fields = CMetaFields
	id     = None
	type   = ""
	note   = ""

	def __init__(self, in_connection=None):
		super(CMetaObject, self).__init__(in_connection)

		self.id = None

	def set_connection(self, in_connection=None):
		super(CMetaObject, self).set_connection(in_connection)

		self.fields = CMetaFields(in_connection)

	def load(self, in_id=None):
		if in_id is not None:
			self.id = in_id

		if self.id is not None:
			sql = "SELECT " \
			      "  type, note " \
			      "FROM {0} " \
			      "WHERE" \
			      "  id = {1}".format(TABLE_META, self.id)
			_data = self.connection.get_multiple(sql)

			self.type = _data[0]
			self.note = _data[1]

			self.fields.load(self.id)

	def save(self):
		if self.id is None:
			sql = "INSERT INTO {0} (" \
			      "  type,  " \
			      "  note" \
			      ") " \
			      "VALUES (" \
			      "  '{1}', " \
			      "  '{2}'" \
			      ")".format(TABLE_META, self.type, self.note)
			self.connection.exec_insert(sql)

			sql = "SELECT last_insert_rowid()"
			self.id = self.connection.get_single(sql)

		else:
			sql = "UPDATE {0} " \
			      "SET" \
			      "  type = '{1}', " \
			      "  note = '{2}' " \
			      "WHERE " \
			      "  id = '{3}'".format(TABLE_META, self.type, self.note, self.id)
			self.connection.exec_update(sql)

		self.fields._id_obj = self.id
		self.fields.save()


# Базовые классы
class CCatalogFieldGroups(CMeta):
	def get_groups(self):
		sql = "SELECT DISTINCT " \
		      "  id " \
		      "FROM {0} " \
		      "WHERE " \
		      "  type='{1}'".format(TABLE_FIELDS, CATALOG_FIELDS_GROUP)
		return self.connection.get_list(sql)


class CCatalogFieldGroup(CMetaObject):
	type = CATALOG_FIELDS_GROUP
	name = ""

	def save(self):
		self.fields.set_field("Название", self.name)
		self.id = self._get_id(self.name)

		super(CCatalogFieldGroup, self).save()

	def load(self, in_id_or_name=None):
		if   type(in_id_or_name) == int:
			self.id = in_id_or_name
		elif type(in_id_or_name) == str:
			self.id   = self._get_id(in_id_or_name)
			
		if self.id is not None:
			self.clear()
			super(CCatalogFieldGroup, self).load()
			self.name = self.fields.get_field("Название")

	def _get_id(self, in_name=None):
		sql = "SELECT " \
		      "  ID_OBJ " \
		      "FROM {0} " \
		      "WHERE " \
		      "  type  ='{1}' and " \
		      "  value ='{2}'".format(TABLE_FIELDS, CATALOG_FIELDS_GROUP_NAME, in_name)
		return self.connection.get_single(sql)

	def clear(self, in_clear_id=False):
		if in_clear_id:
			self.id = None

		self.name = ""
		self.note = ""
		self.fields.clear()
