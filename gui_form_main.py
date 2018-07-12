from core_gui     import *
from core_objects import *


class FormMain(CForm):
	model_equipment = QStandardItemModel

	_equipments = CEquipments
	_equipment  = CEquipment

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
		self.menu_equipment.addAction(self.action_equipment_delete)

		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_catalogs)

	def __init_objects__(self):
		self.model_equipment = QStandardItemModel()

		self._equipment  = CEquipment(self.application.sql_connection)
		self._equipments = CEquipments(self.application.sql_connection)

	def __init_ui__(self):
		super(FormMain, self).__init_ui__()

		self.setWindowTitle("IT-management")

		self._init_panel_equipment_()

	def _init_panel_equipment_(self):
		self.panel_equipment = QTreeView()

	def select_equipment(self):
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
