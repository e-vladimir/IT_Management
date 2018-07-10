from core_gui     import *
from core_objects import *


class FormEquipment(CForm):
	_groups      = CCatalogFieldGroups
	_group       = CCatalogFieldGroup

	_equipments  = CEquipments
	_equipment   = CEquipment

	model_fields = QStandardItemModel
	tree_fields  = QTreeView

	current_group = None
	current_field = None

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)
		self._equipments  = CEquipments(self.application.sql_connection)
		self._equipment   = CEquipment(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

	def __init_ui__(self):
		self.setWindowTitle("ОС и ТМЦ")
		self.setMinimumSize(460, 640)

		self.tree_fields = QTreeView()
		self.tree_fields.setModel(self.model_fields)