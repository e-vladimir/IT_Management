from core_gui     import *
from core_objects import *


class FormMain(CForm):
	model_equipment = QStandardItemModel

	_equipments = CEquipments
	_equipment  = CEquipment

	_current_equipment_item = None

	def __init_actions__(self):
		self.action_select_equipment = QAction(self.icon_small_equipment, "Учёт ОС и ТМЦ",        None)
		self.action_catalogs_fields  = QAction(self.icon_small_equipment, "Характеристики",       None)

		self.action_equipment_add    = QAction(self.icon_small_add,       "Добавить ОС или ТМЦ",  None)
		self.action_equipment_delete = QAction(self.icon_small_delete,    "Удалить <ОС или ТМЦ>", None)

	def __init_events__(self):
		self.action_select_equipment.triggered.connect(self.select_equipment)

		self.action_equipment_add.triggered.connect(self.add_equipment)

		self.action_catalogs_fields.triggered.connect(self.open_catalog_fields)

	def __init_icons__(self):
		self.icon_small_equipment = QIcon(self.application.PATH_ICONS_SMALL + "equipments.png")
		self.icon_small_catalog   = QIcon(self.application.PATH_ICONS_SMALL + "catalog.png")
		self.icon_small_add       = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete    = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

	def __init_menu__(self):
		self.menu_sections  = QMenu("Раздел")
		self.menu_sections.addAction(self.action_select_equipment)

		self.menu_catalogs  = QMenu("Каталоги")
		self.menu_catalogs.addAction(self.action_catalogs_fields)

		self.menu_equipment = QMenu("Действия")
		self.menu_equipment.setVisible(False)
		self.menu_equipment.addAction(self.action_equipment_add)
		self.menu_equipment.addSeparator()
		self.menu_equipment.addAction(self.action_equipment_delete)

		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_catalogs)

	def __init_objects__(self):
		self.model_equipment = QStandardItemModel()

		self._equipment  = CEquipment(self.application.sql_connection)
		self._equipments = CEquipments(self.application.sql_connection)

	def __init_ui__(self):
		super(FormMain, self).__init_ui__()

		self.setMinimumSize(800, 640)
		self.setWindowTitle("IT-management")

		self._init_panel_equipment_()

	def _init_panel_equipment_(self):
		self.panel_equipment = QTreeView()
		self.panel_equipment.setModel(self.model_equipment)
		self.panel_equipment.header().hide()
		self.panel_equipment.setEditTriggers(QTreeView.NoEditTriggers)

	def select_equipment(self):
		self.load_equipments()

		self.menu_sections.setTitle(self.action_select_equipment.text())

		self.setCentralWidget(self.panel_equipment)

		self.menuBar().clear()
		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_equipment)
		self.menuBar().addMenu(self.menu_catalogs)

	def open_catalog_fields(self):
		self.application.form_catalog_fields.load_and_show()

	def add_equipment(self):
		self.application.form_equipment.load()

	def _add_equipment(self, in_id=None):
		self._equipment.load(in_id)

		item_category    = QStandartItemWithID(self._equipment.base.category,    in_id)
		item_subcategory = QStandartItemWithID(self._equipment.base.subcategory, in_id)

		item_brand       = QStandartItemWithID(self._equipment.base.brand,       in_id)
		item_model       = QStandartItemWithID(self._equipment.base.model,       in_id)

		item_state       = QStandartItemWithID(self._equipment.base.state,       in_id)

		self.model_equipment.appendRow([item_category, item_subcategory, item_brand, item_model, item_state])

	def load_equipments(self):
		self.model_equipment.clear()

		_list_id = self._equipments.get_list_id()

		for _id in _list_id:
			self._add_equipment(_id)

		self.resize_equipment()

	def resize_equipment(self):
		self.panel_equipment.hide()

		for index_col in range(self.model_equipment.columnCount()):
			self.panel_equipment.resizeColumnToContents(index_col)

		self.panel_equipment.show()

	def get_current_equipment(self):
		_current_index = self.panel_equipment.currentIndex()
		self._current_equipment_item = self.model_equipment.itemFromIndex(_current_index)