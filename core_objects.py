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
	fields_list = dict()

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

	def clear(self):
		self.fields_list = dict()

	def get(self, in_field_name):
		if in_field_name in self.fields_list:
			return self.fields_list[in_field_name]
		else:
			return None

	def set(self, in_field_name, in_field_value=""):
		""" in_field_name = <Категория>/<Подкатегория> """
		if in_field_name in self.fields_list:
			self.fields_list[in_field_name] = in_field_value


class CField(CMeta):
	id       = ""
	id_obj   = ""
	cat      = ""
	scat     = ""
	value    = ""


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

	def clear(self, in_clearID=False):
		self.fields.clear()
		self.note   = ""

		if in_clearID: self.id = None


class CEquipments(CMetaObjects):
	type = EQUIPMENT


class CEquipment(CMetaObject):
	type = EQUIPMENT

	def clear(self, in_clearID=False):
		super(CEquipment, self).clear(in_clearID)


# Справочник характеристик
class CCatFields(CMeta):
	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
			      " ID         INTEGER PRIMARY KEY NOT NULL, " \
			      " cat        TEXT, " \
			      " scat       TEXT" \
			      ")".format(TABLE_CAT_FIELDS)
			self.connection.exec_create(sql)

	def get_list(self, filter_object=None, filter_struct=None, filter_cat=None, filter_scat=None):
		sql = "SELECT id " \
		      "FROM {} " \
		      "ORDER BY id ".format(TABLE_CAT_FIELDS)

		if not ((filter_object is None) and (filter_struct is None) and (filter_cat is None) and (filter_scat is None)):
			sql += "WHERE ("

			if filter_object is not None: sql += "(type_obj = {})".format(filter_object)
			if filter_cat    is not None: sql += "(cat      = {})".format(filter_cat)
			if filter_scat   is not None: sql += "(scat     = {})".format(filter_scat)

			sql += ")"

		return self.connection.get_list(sql)


class CCatField(CMeta):
	id       = None

	type_obj = ""

	cat      = ""
	scat     = ""

	def clear(self, in_clear_id=False):
		if in_clear_id: self.id = None

		self.type_obj = ""
		self.cat      = ""
		self.scat     = ""
