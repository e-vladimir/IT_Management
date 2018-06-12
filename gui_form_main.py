from core_gui     import *
from core_objects import *


class FormMain(CForm):
	equipments = CEquipments
	equipment  = CEquipment

	def __init_objects__(self):
		self.equipments = CEquipments(self.application.sql_connection)
		self.equipment  = CEquipment(self.application.sql_connection)

	def __init_icons__(self):
		self.icon_small_equipments   = QIcon(self.application.PATH_ICONS_SMALL + "equipments.png")
		self.icon_small_materials    = QIcon(self.application.PATH_ICONS_SMALL + "materials.png")
		self.icon_small_requests     = QIcon(self.application.PATH_ICONS_SMALL + "requests.png")
		self.icon_small_transactions = QIcon(self.application.PATH_ICONS_SMALL + "transactions.png")

		self.icon_small_catalog      = QIcon(self.application.PATH_ICONS_SMALL + "cats.png")
		self.icon_small_fields       = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

	def __init_actions__(self):
		self.action_menu_tab_equipments   = QAction(self.icon_small_equipments,   "Оборудование",   None)
		self.action_menu_tab_materials    = QAction(self.icon_small_materials,    "Материалы",      None)
		self.action_menu_tab_requests     = QAction(self.icon_small_requests,     "Заявки",         None)
		self.action_menu_tab_transactions = QAction(self.icon_small_transactions, "Транзакции",     None)

		self.action_menu_catalog_fields   = QAction(self.icon_small_fields,       "Характеристики", None)

	def __init_events__(self):
		self.action_menu_tab_equipments.triggered.connect(self.select_tab_equipments)

		self.action_menu_catalog_fields.triggered.connect(self.application.form_catalogs_fields.load_and_show)

	def __init_ui__(self):
		super(FormMain, self).__init_ui__()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("IT-management - {0}".format(self.application.version))

	def __init_menu__(self):
		self.menu_tabs = QMenu("Раздел")
		self.menu_tabs.addAction(self.action_menu_tab_equipments)
		self.menu_tabs.addAction(self.action_menu_tab_materials)
		self.menu_tabs.addAction(self.action_menu_tab_requests)
		self.menu_tabs.addAction(self.action_menu_tab_transactions)

		self.menu_catalogs = QMenu("Каталоги")
		self.menu_catalogs.setIcon(self.icon_small_catalog)
		self.menu_catalogs.addAction(self.action_menu_catalog_fields)

		self.menu_service = QMenu("Сервис")
		self.menu_service.addMenu(self.menu_catalogs)

		self.menuBar().addMenu(self.menu_tabs)
		self.menuBar().addMenu(self.menu_service)

	def select_tab_equipments(self):
		self.menu_tabs.setTitle("Оборудование")
