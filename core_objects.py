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


# Объекты
class CMetaEquipment(CMeta):
	type = "Объект"

	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS {} " \
			      "(" \
			      " ID         INTEGER PRIMARY KEY NOT NULL, " \
			      " type       TEXT, " \
			      " note       TEXT, " \
			      ")".format(TABLE_EQUIPMENT)
			self.connection.exec_create(sql)
