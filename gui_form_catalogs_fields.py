from core_gui     import *
from core_objects import *
from functools import partial


class QItemModelIcon(QStandartItemWithID):
	def __init__(self,  in_caption, in_id="", in_editable=True, in_icon=None):
		super(QItemModelIcon, self).__init__(in_caption, in_id, in_editable)

		if in_icon is not None:
			self.setIcon(in_icon)


class FormCatalogsFields(CForm):
	CatFields = CCatFields
	CatField  = CCatField

	model_fields = QStandardItemModel

	current_type  = None
	current_group = None
	current_field = None

	def __init_icons__(self):
		self.icon_small_row_insert  = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_row_delete  = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_table_save  = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_table_close = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_readonly    = QIcon(self.application.PATH_ICONS_SMALL + "bullet_black.png")

	def __init_actions__(self):
		self.action_field_add       = QAction(self.icon_small_row_insert,  "Добавить характеристику", None)
		self.action_field_delete    = QAction(self.icon_small_row_delete,  "Удалить характеристику",  None)

		self.action_save            = QAction(self.icon_small_table_save,  "Сохранить",               None)
		self.action_save_and_close  = QAction(self.icon_small_table_save,  "Сохранить и закрыть",     None)
		self.action_close           = QAction(self.icon_small_table_close, "Закрыть",                 None)

	def __init_events__(self):
		self.action_save.triggered.connect(self.save)

	def __init_menu__(self):
		self.menu_actions = QMenu("Действия")
		self.menu_actions.addAction(self.action_save)
		self.menu_actions.addAction(self.action_save_and_close)
		self.menu_actions.addSeparator()
		self.menu_actions.addAction(self.action_close)

		self.menu_fields = QMenu("Характеристики")
		self.menu_fields.addAction(self.action_field_add)
		self.menu_fields.addAction(self.action_field_delete)

		self.menuBar().addMenu(self.menu_actions)
		self.menuBar().addMenu(self.menu_fields)

	def __init_objects__(self):
		self.model_fields = QStandardItemModel()

		self.CatFields = CCatFields(self.application.sql_connection)
		self.CatField  = CCatField(self.application.sql_connection)

	def __init_ui__(self):
		super(FormCatalogsFields, self).__init_ui__()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("Каталог - характеристики")

		self.tree_fields = QTreeView()
		self.tree_fields.setModel(self.model_fields)

		self.setCentralWidget(self.tree_fields)

		self.setContentsMargins(3, 3, 3, 3)

	def load_and_show(self):
		self.model_fields.clear()

		# Базовый набор Оборудование
		item_group_equipment    = QItemModelIcon("Оборудование",         None, False, self.icon_small_readonly)
		item_category_equipment = QItemModelIcon("Основные параметры",           None, False, self.icon_small_readonly)
		item_category_equipment.appendRow(QItemModelIcon("Категория",            None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Подкатегория",         None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Статус",               None, False, self.icon_small_readonly))
		item_group_equipment.appendRow(item_category_equipment)

		item_category_equipment = QItemModelIcon("Техническое описание", None, False, self.icon_small_readonly)
		item_category_equipment.appendRow(QItemModelIcon("Производитель",        None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Модель",               None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Серийный номер",       None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Техническое описание", None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Состояние",            None, False, self.icon_small_readonly))
		item_group_equipment.appendRow(item_category_equipment)

		item_category_equipment = QItemModelIcon("Местоположение",       None, False, self.icon_small_readonly)
		item_category_equipment.appendRow(QItemModelIcon("Подразделение",        None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Местоположение",       None, False, self.icon_small_readonly))
		item_category_equipment.appendRow(QItemModelIcon("Ответственное лицо",   None, False, self.icon_small_readonly))
		item_group_equipment.appendRow(item_category_equipment)

		self.model_fields.appendRow(item_group_equipment)

		self.tree_fields.header().hide()

		id_list_all = self.CatFields.get_list()

		self.showCentered()

	def save(self, in_close=False):
		if in_close:
			self.close()
