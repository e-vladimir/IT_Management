from core_gui     import *
from core_objects import *


class FormMain(CForm):
	def __init_icons__(self):
		self.icon_small_equipment = QIcon(self.application.PATH_ICONS_SMALL + "equipments.png")
		self.icon_small_catalog   = QIcon(self.application.PATH_ICONS_SMALL + "catalog.png")

	def __init_actions__(self):
		self.action_select_equipment = QAction(self.icon_small_equipment, "Учёт ОС и ТМЦ", None)
		self.action_catalogs_fields  = QAction(self.icon_small_equipment, "Характеристики", None)

	def __init_menu__(self):
		self.menu_sections = QMenu("Раздел")
		self.menu_sections.addAction(self.action_select_equipment)

		self.menu_equipment_catalogs = QMenu("Каталоги")
		self.menu_equipment_catalogs.addAction(self.action_catalogs_fields)

		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_equipment_catalogs)

	def __init_events__(self):
		self.action_select_equipment.triggered.connect(self.select_equipment)

	def select_equipment(self):
		self.menu_sections.setTitle(self.action_select_equipment.text())
