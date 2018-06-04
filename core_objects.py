from dict import *


class CMetaObject:
	connection  = None

	id          = None
	note        = ""
	type        = ""
	state       = ""

	fields = dict()

	def __init__(self, in_connection=None):
		super(CMetaObject, self).__init__()

		self.set_connection(in_connection)

	def _init_db_(self):
		if self.connection is not None:
			sql = "CREATE TABLE IF NOT EXISTS meta" \
			      "(" \
			      " ID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " \
			      " note  TEXT, " \
			      " type  TEXT, " \
			      " state TEXT" \
			      ")"
			self.connection.exec_create(sql)

			sql = "CREATE TABLE IF NOT EXISTS fields" \
			      "(" \
			      " ID    INTEGER, " \
			      " field TEXT, " \
			      " value TEXT" \
			      ")"
			self.connection.exec_create(sql)

	def _generate_id_(self):
		sql = "SELECT id " \
		      "FROM meta " \
		      "ORDER BY id DESC " \
		      "LIMIT 1"
		last_id = self.connection.get_single(sql)

		if last_id is None: last_id = 0
		else: last_id = int(last_id) + 1

		self.id = last_id

	def set_connection(self, in_connection=None):
		self.connection   = in_connection
		self._init_db_()

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
		if in_id is not None:
			self.id = in_id

		self.clear()

		if self.id is not None:
			sql = "SELECT type, note, state " \
			      "FROM meta " \
			      "WHERE (id='{0}')".format(self.id)
			self.type  = self.connection.get_single(sql, 0)
			self.note  = self.connection.get_single(sql, 1)
			self.state = self.connection.get_single(sql, 2)

			sql = "SELECT field, value " \
			      "FROM fields " \
			      "WHERE (id='{0}') " \
			      "ORDER BY field".format(self.id)
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

				sql = "INSERT INTO meta " \
				      " (ID,     note,  type, state) " \
				      "VALUES " \
				      " ('{0}', '{1}', '{2}', '{3}')".format(self.id, self.note, self.type, self.state)
				self.connection.exec_insert(sql)
			else:
				sql = "UPDATE meta " \
				      "SET note='{0}', " \
				      "    type='{1}'," \
				      "    state='{2}' " \
				      "WHERE id='{3}'".format(self.note, self.type, self.state, self.id)
				self.connection.exec_update(sql)

			sql = "DELETE FROM fields WHERE (id='{0}')".format(self.id)
			self.connection.exec_delete(sql)

			for field, value in self.fields.items():
				sql = "INSERT INTO fields (ID, field, value) VALUES ('{0}', '{1}', '{2}')".format(self.id, field, value)
				self.connection.exec_insert(sql)

			self.connection.transaction_commit()

			return True
		except Exception as error:
			self.connection.transaction_rollback()

			return False

	def delete(self):
		self.connection.transaction_start()

		try:
			sql = "DELETE FROM fields WHERE (id='{0}')".format(self.id)
			self.connection.exec_delete(sql)

			sql = "DELETE FROM meta WHERE (id='{0}')".format(self.id)
			self.connection.exec_delete(sql)

			self.connection.transaction_commit()
		except:
			self.connection.transaction_rollback()
