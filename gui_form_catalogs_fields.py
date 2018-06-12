from core_gui     import *
from core_objects import *


class FormCatalogsFields(CForm):
	CatFields = CCatFields
	CatField  = CCatField

	model_fields = QStandardItemModel

	def __init_icons__(self):
		self.icon_small_row_insert  = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_row_delete  = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_table_save  = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_table_close = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

	def __init_actions__(self):
		self.action_field_add      = QAction(self.icon_small_row_insert,  "Добавить характеристику", None)
		self.action_field_delete   = QAction(self.icon_small_row_delete,  "Удалить характеристику",  None)

		self.action_save           = QAction(self.icon_small_table_save,  "Сохранить",               None)
		self.action_save_and_close = QAction(self.icon_small_table_save,  "Сохранить и закрыть",     None)
		self.action_close          = QAction(self.icon_small_table_close, "Закрыть",                 None)

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

		self.table_fields = QTableView()
		self.table_fields.setModel(self.model_fields)

		self.setCentralWidget(self.table_fields)

		self.setContentsMargins(3, 3, 3, 3)

	def load_and_show(self):
		self.model_fields.clear()

		id_list_all = self.CatFields.get_list()

		self.show()