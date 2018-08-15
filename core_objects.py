from dict import *
from core_sqlite import *


# Мета-конверторы
def _extract_part(in_field, in_part_num):
	if in_field is not None:
		_list = in_field.split("/")

		if len(_list) > in_part_num:
			return _list[in_part_num]
		else:
			return None
	else:
		return None


def extract_field_group(in_field=None):
	return _extract_part(in_field, 0)


def extract_field_name(in_field=None):
	return _extract_part(in_field, 1)


# Мета-классы
class CMeta:
	connection  = TSQLiteConnection

	def __init__(self, in_connection=None):
		self.set_connection(in_connection)

		self.__init_objects__()

	def __init_db__(self):
		sql = "CREATE TABLE IF NOT EXISTS {0} " \
		      "(" \
		      "  ID     INTEGER PRIMARY KEY ASC, " \
		      "  type   TEXT, " \
		      "  note   TEXT  " \
		      ")".format(TABLE_META)

		self.connection.exec_create(sql)

	def __init_objects__(self):
		pass

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self.__init_db__()


class CMetaFields(CMeta):
	_fields = dict
	_id_obj = ""

	hide_fields = []

	def __init__(self, in_connection=None):
		super(CMetaFields, self).__init__(in_connection)

		self._fields     = dict()
		self.hide_fields = []

	def __init_db__(self):
		sql = "CREATE TABLE IF NOT EXISTS {0} " \
		      "(" \
		      "  ID     INTEGER PRIMARY KEY ASC, " \
		      "  ID_OBJ INTEGER, " \
		      "  field  TEXT, " \
		      "  value  TEXT  " \
		      ")".format(TABLE_FIELDS)

		self.connection.exec_create(sql)

	def _load_field_(self, in_id):
		self._id_obj = in_id

		sql = "SELECT "   \
		      "  field, " \
		      "  value "  \
		      "FROM {0} " \
		      "WHERE "    \
		      "  id = '{1}'".format(TABLE_FIELDS, in_id)

		field_values = self.connection.get_multiple(sql)
		_type        = field_values[0]
		_value       = field_values[1]

		self._fields[_type] = _value

	def clear(self):
		self._fields = dict()

	def delete_field(self, in_field=None):
		if in_field is not None:
			if in_field in self._fields:
				self._fields.pop(in_field)

	def get_field(self, in_field):
		if in_field not in self._fields:
			return None
		else:
			return self._fields[in_field]

	def get_list(self):
		result = []

		for field in self._fields:
			if field not in self.hide_fields:
				result.append(field)

		return result

	def load(self, in_id_obj):
		self._id_obj = in_id_obj

		sql = "SELECT " \
		      "  ID " \
		      "FROM {0} " \
		      "WHERE " \
		      "  (ID_OBJ = '{1}')".format(TABLE_FIELDS, self._id_obj)

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
				      "  ID_OBJ," \
				      "  field,  "\
				      "  value )" \
				      "VALUES ("  \
				      "  '{1}', " \
				      "  '{2}', " \
				      "  '{3}' )".format(TABLE_FIELDS, self._id_obj, field, self._fields[field])
				self.connection.exec_insert(sql)

			self.connection.transaction_commit()

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

	def clear(self, in_clear_id=False):
		if in_clear_id:
			self.id = None

		self.fields.clear()
		self.note = ""

	def set_connection(self, in_connection=None):
		super(CMetaObject, self).set_connection(in_connection)

		self.fields = CMetaFields(in_connection)

	def delete(self):
		self.connection.transaction_start()
		sql = "DELETE FROM {0} " \
		      "WHERE " \
		      "  ID_OBJ='{1}'".format(TABLE_FIELDS, self.id)
		self.connection.exec_delete(sql)

		sql = "DELETE FROM {0} " \
		      "WHERE " \
		      "  ID='{1}'".format(TABLE_META, self.id)
		self.connection.exec_delete(sql)

		self.connection.transaction_commit()

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

	def set(self, in_field_cat, in_field_subcat, in_value=""):
		self.fields.set_field("{}/{}".format(in_field_cat, in_field_subcat), in_value)

	def get(self, in_field_cat, in_field_subcat):
		return self.fields.get_field("{}/{}".format(in_field_cat, in_field_subcat))


# Базовые классы
class CCatalogFieldGroups(CMeta):
	def get_list(self):
		result   = []
		_list_id = self.get_list_id()

		for _id in _list_id:
			sql = "SELECT " \
			      "  value " \
			      "FROM {0} " \
			      "WHERE " \
			      "  ID_OBJ='{1}' and " \
			      "  field='{2}'".format(TABLE_FIELDS, _id, CATALOG_FIELDS_GROUP_NAME)
			result.append(self.connection.get_single(sql))

		return result

	def get_list_id(self):
		sql = "SELECT DISTINCT " \
		      "  ID " \
		      "FROM {0} " \
		      "WHERE " \
		      "  type='{1}'".format(TABLE_META, CATALOG_FIELDS_GROUP)
		return self.connection.get_list(sql)


class CCatalogFieldGroup(CMetaObject):
	type = CATALOG_FIELDS_GROUP
	name = ""

	def __init_objects__(self):
		self.fields.hide_fields = [CATALOG_FIELDS_GROUP_NAME]

	def _get_id(self, in_name=None):
		sql = "SELECT " \
		      "  ID_OBJ " \
		      "FROM {0} " \
		      "WHERE " \
		      "  field  ='{1}' and " \
		      "  value ='{2}'".format(TABLE_FIELDS, CATALOG_FIELDS_GROUP_NAME, in_name)
		return self.connection.get_single(sql)

	def clear(self, in_clear_id=False):
		if in_clear_id:
			self.id = None

		self.name = ""
		self.note = ""
		self.fields.clear()

	def get_fields(self):
		result = []
		list_fields = self.fields.get_list()

		for field in list_fields:
			if "Характеристика" in field:
				result.append(self.fields.get_field(field))

		return result

	def load(self, in_id_or_name=None):
		self.fields.clear()

		if type(in_id_or_name) == int:
			self.id = in_id_or_name
		elif type(in_id_or_name) == str:
			self.id = self._get_id(in_id_or_name)

		if self.id is not None:
			self.clear()
			super(CCatalogFieldGroup, self).load()
			self.name = self.fields.get_field("Название")

	def save(self):
		self.fields.set_field("Название", self.name)
		self.id = self._get_id(self.name)

		super(CCatalogFieldGroup, self).save()


# Транзитные классы
class GroupMeta:
	_meta = None

	def __init__(self, in_metaObject=None):
		self._meta = in_metaObject

		self.load()

	def clear(self):
		pass

	def load(self):
		self.clear()


class GroupBase(GroupMeta):
	category             = ""
	subcategory          = ""

	brand                = ""
	model                = ""
	serial_num           = ""
	description          = ""

	state                = ""

	def clear(self):
		self.brand       = ""
		self.category    = ""
		self.description = ""
		self.model       = ""
		self.serial_num  = ""
		self.state       = ""
		self.subcategory = ""

	def load(self):
		super(GroupBase, self).load()

		self.brand       = self._meta.get(FIELDS_GROUP_BASE, "Производитель")
		self.category    = self._meta.get(FIELDS_GROUP_BASE, "Категория")
		self.description = self._meta.get(FIELDS_GROUP_BASE, "Описание")
		self.model       = self._meta.get(FIELDS_GROUP_BASE, "Модель")
		self.serial_num  = self._meta.get(FIELDS_GROUP_BASE, "Серийный номер")
		self.state       = self._meta.get(FIELDS_GROUP_BASE, "Состояние")
		self.subcategory = self._meta.get(FIELDS_GROUP_BASE, "Подкатегория")


class GroupPlacement(GroupMeta):
	people             = ""
	placement          = ""
	struct             = ""

	def clear(self):
		self.people    = ""
		self.placement = ""
		self.struct    = ""

	def load(self):
		super(GroupPlacement, self).load()

		self.people    = self._meta.get(FIELDS_GROUP_PLACEMENT, "Сотрудник")
		self.placement = self._meta.get(FIELDS_GROUP_PLACEMENT, "Помещение")
		self.struct    = self._meta.get(FIELDS_GROUP_PLACEMENT, "Структура")


class GroupAccounting(GroupMeta):
	include = ""
	number  = ""
	people  = ""

	def clear(self):
		self.include = ""
		self.number  = ""
		self.people  = ""

	def load(self):
		super(GroupAccounting, self).load()

		self.include = self._meta.get(FIELDS_GROUP_ACCOUNTING, "Числится")
		self.number  = self._meta.get(FIELDS_GROUP_ACCOUNTING, "Инвентарный номер")
		self.people  = self._meta.get(FIELDS_GROUP_ACCOUNTING, "Сотрудник")


# ОС и ТМЦ
class CEquipments(CMeta):
	def get_list_id(self):
		sql = "SELECT id " \
		      "FROM {} " \
		      "WHERE " \
		      "  type='{}'".format(TABLE_META, EQUIPMENT)
		return self.connection.get_list(sql)

	def get_list_groups(self):
		result = []

		sql = "SELECT DISTINCT" \
		      "  field " \
		      "FROM {0} " \
		      "LEFT JOIN" \
		      "  {1} " \
		      "ON" \
		      "  {0}.ID_OBJ = {1}.id " \
		      "WHERE " \
		      "  {1}.type = '{2}' " \
		      "ORDER BY " \
		      "  field ASC".format(TABLE_FIELDS, TABLE_META, EQUIPMENT)
		_list_fields = self.connection.get_list(sql)

		for _field in _list_fields:
			_group = extract_field_group(_field)

			if (_group not in result) and (_group is not None):
				result.append(_group)

		return result

	def get_list_fields(self, in_group):
		result = []

		sql = "SELECT DISTINCT" \
		      "  field " \
		      "FROM {0} " \
		      "LEFT JOIN" \
		      "  {1} " \
		      "ON" \
		      "  {0}.ID_OBJ = {1}.id " \
		      "WHERE " \
		      "  {1}.type = '{2}' " \
		      "ORDER BY " \
		      "  field ASC".format(TABLE_FIELDS, TABLE_META, EQUIPMENT)
		_list_fields = self.connection.get_list(sql)

		for _field in _list_fields:
			_group = extract_field_group(_field)
			_name  = extract_field_name(_field)

			if _group == in_group:
				if (_name not in result) and (_name is not None):
					result.append(_name)

		return result

	def get_list_values(self, in_field):
		sql = "SELECT value " \
		      "FROM {} " \
		      "WHERE " \
		      "  field='{}'".format(TABLE_FIELDS, in_field)

		_fields = self.connection.get_list(sql)
		_fields = list(set(_fields))

		_fields.sort()

		return _fields

	def replace_field(self, old_field, new_field):
		_commit = True

		self.connection.transaction_start()

		sql = "UPDATE {0} " \
		      "SET" \
		      "  field = '{1}_' " \
		      "WHERE " \
		      "  field = '{1}'".format(TABLE_FIELDS, new_field)
		_commit = _commit and self.connection.exec_update(sql)

		if _commit:
			sql = "UPDATE {0} " \
			      "SET" \
			      "  field = '{2}' " \
			      "WHERE " \
			      "  field = '{1}'".format(TABLE_FIELDS, old_field, new_field)
			_commit = _commit and self.connection.exec_update(sql)

		if _commit:
			sql = "DELETE " \
			      "FROM {0} " \
			      "WHERE " \
			      "  field = '{1}_'".format(TABLE_FIELDS, new_field)
			_commit = _commit and self.connection.exec_update(sql)

		if _commit:
			self.connection.transaction_commit()
		else:
			self.connection.transaction_rollback()

		return _commit

	def set_value(self, in_field, in_value):
		sql = "UPDATE {} " \
		      "SET " \
		      "  value='{}' " \
		      "WHERE " \
		      "  field='{}'".format(TABLE_FIELDS, in_value, in_field)
		return self.connection.exec_update(sql)

	def replace_value(self, in_field, in_value_from, in_value_to):
		sql = "UPDATE {} " \
		      "SET " \
		      "  value='{}' " \
		      "WHERE " \
		      "  field='{}' " \
		      "AND " \
		      "  value='{}'".format(TABLE_FIELDS, in_value_to, in_field, in_value_from)
		return self.connection.exec_update(sql)


class CEquipment(CMetaObject):
	type                   = EQUIPMENT

	base                   = GroupBase
	placement              = GroupPlacement
	accounting             = GroupAccounting

	_field_groups          = CCatalogFieldGroups
	_field_group           = CCatalogFieldGroup

	def __init_objects__(self):
		self._field_groups = CCatalogFieldGroups(self.connection)
		self._field_group  = CCatalogFieldGroup(self.connection)

		self.base          = GroupBase(self)
		self.placement     = GroupPlacement(self)
		self.accounting    = GroupAccounting(self)

	def load(self, in_id=None):
		super(CEquipment, self).load(in_id)

		self.base.load()
		self.placement.load()
		self.accounting.load()

	def get_values_by_field(self, in_group="", in_field=""):
		sql = "SELECT DISTINCT " \
		      "  value " \
		      "FROM {} " \
		      "WHERE" \
		      "  field='{}/{}' " \
		      "ORDER BY " \
		      "  value ASC ".format(TABLE_FIELDS, in_group, in_field)
		return self.connection.get_list(sql)
