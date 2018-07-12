from core_gui     import *
from core_objects import *


class NoneModelItem(QStandartItemWithID):
	def __init__(self):
		super(NoneModelItem, self).__init__("", None)


class FormEquipment(CForm):
	_groups      = CCatalogFieldGroups
	_group       = CCatalogFieldGroup

	_equipments  = CEquipments
	_equipment   = CEquipment

	model_fields = QStandardItemModel
	tree_fields  = QTreeView

	current_group = None
	current_field = None

	def __init_events__(self):
		self.tree_fields.expanded.connect(self._gui_resize_fields)
		self.tree_fields.collapsed.connect(self._gui_resize_fields)

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)
		self._equipments  = CEquipments(self.application.sql_connection)
		self._equipment   = CEquipment(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

	def __init_ui__(self):
		self.setWindowTitle("ОС и ТМЦ")
		self.setMinimumSize(460, 640)

		self._init_tabs_()

	def _init_tabs_(self):
		self.tabs = QTabWidget()
		self.field_note = QLineEdit()
		self.field_note.setPlaceholderText("Примечение")

		central_layout = QVBoxLayout()
		central_layout.setContentsMargins(3, 3, 3, 3)
		central_layout.setSpacing(3)
		central_layout.addWidget(self.tabs)
		central_layout.addWidget(self.field_note)

		central_widget = QWidget()
		central_widget.setLayout(central_layout)

		self.setCentralWidget(central_widget)

		self._init_tab_main_()

	def _init_tab_main_(self):
		self.tree_fields = QTreeView()
		self.tree_fields.setMinimumWidth(300)
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()
		self.tree_fields.setAlternatingRowColors(True)

		self.field_values = QListWidget()

		splitter_main = QSplitter()
		splitter_main.setContentsMargins(3, 3, 3, 3)
		splitter_main.addWidget(self.tree_fields)
		splitter_main.addWidget(self.field_values)

		self.tabs.addTab(splitter_main, "Характеристики")

	def load_fields(self):
		self.model_fields.clear()

		list_groups = self._groups.get_list()

		for group in list_groups:
			self._group.load(group)

			item_group = QStandartItemWithID(self._group.name, None)
			item_group.setCheckable(True)

			list_fields = self._group.get_fields()
			for field in list_fields:
				item_group.appendRow([QStandartItemWithID(field, None), NoneModelItem()])

			self.model_fields.appendRow([item_group, NoneModelItem()])

	def load(self, in_id=None):
		self.load_fields()

		self._gui_resize_fields()

		self.showCentered()

	def _gui_resize_fields(self):
		self.tree_fields.resizeColumnToContents(0)
