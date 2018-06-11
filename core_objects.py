from dict import *


# Мета-класс
class CMeta:
	connection  = None

	def __init__(self, in_connection):
		super(CMeta, self).__init__()

		self.set_connection(in_connection)

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

	def _init_db_(self):
		pass


# Характеристики
class CFields(CMeta):
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


class CField(CMeta):
	id     = ""
	id_obj = ""
	cat    = ""
	scat   = ""
	value  = ""

	struct = ""


# Объекты
class CMetaObjects(CMeta):
	type = "Объект"

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


class CMetaObject(CMeta):
	id          = None
	note        = ""
	type        = ""
	state       = ""

	fields      = CFields

	def set_connection(self, in_connection=None):
		super(CMetaObject, self).set_connection(in_connection)

		self.fields = CFields(self.connection)

	def set_field(self, in_field="", in_value=""):
		self.fields[in_field] = in_value

	def get_field(self, in_field=""):
		if in_field in self.fields:	return self.fields[in_field]
		else:           			return None

	def clear(self, in_clearID=False):
		self.fields = dict()
		self.note   = ""

		if in_clearID: self.id = None


class CEquipments(CMetaObjects):
	type = EQUIPMENT


class CEquipment(CMetaObject):
	type = EQUIPMENT


# Справочник характеристик
class CCatFields(CMeta):
	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
			      " ID         INTEGER PRIMARY KEY NOT NULL, " \
			      " type_obj   TEXT, " \
			      " struct     TEXT, " \
			      " cat        TEXT, " \
			      " scat       TEXT" \
			      ")".format(TABLE_CAT_FIELDS)
			self.connection.exec_create(sql)


class CCatField(CMeta):
	id       = None

	type_obj = ""
	struct   = ""
	cat      = ""
	scat     = ""

	def clear(self, in_clear_id=False):
		if in_clear_id: self.id = None

		self.type_obj = ""
		self.struct   = ""
		self.cat      = ""
		self.scat     = ""
