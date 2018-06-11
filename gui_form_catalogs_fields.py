from core_gui     import *
from core_objects import *


class FormCatalogsFields(CForm):
	CatFields = CCatFields
	CatField  = CCatField

	def __init__(self, in_application=None):
		super(FormCatalogsFields, self).__init__(in_application)

		self.CatFields = CCatFields(self.application.sql_connection)
		self.CatField  = CCatField(self.application.sql_connection)

	def __init_ui__(self):
		super(FormCatalogsFields, self).__init_ui__()

		self.setMinimumSize(420, 600)
		self.setWindowTitle("IT-management: Каталог характеристик")

	def load_and_show(self):
		self.show()