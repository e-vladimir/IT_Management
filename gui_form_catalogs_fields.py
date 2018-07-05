from core_gui     import *
from core_objects import *


class FormCatalogsFields(CForm):
	model_fields = QStandardItemModel

	def __init_objects__(self):
		self.model_fields = QStandardItemModel()

	def __init_ui__(self):
		super(FormCatalogsFields, self).__init_ui__()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("Каталог - характеристики")

		tree_fields = QTreeView()
		tree_fields.setModel(self.model_fields)

		self.setCentralWidget(tree_fields)

	def __init_icons__(self):
		self.icon_field_add    = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_field_delete = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_save         = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_close        = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

	def __init_actions__(self):
		self.action_save           = QAction(self.icon_save,         "Сохранить",               None)
		self.action_save_close     = QAction(self.icon_save,         "Сохранить и закрыть",     None)
		self.action_close          = QAction(self.icon_close,        "Закрыть",                 None)

		self.action_field_add      = QAction(self.icon_field_add,    "Добавить",                None)
		self.action_field_add_new  = QAction(self.icon_field_add,    "Добавить в новый раздел", None)
		self.action_field_delete   = QAction(self.icon_field_delete, "Удалить",                 None)

	def __init_events__(self):
		self.action_field_add.triggered.connect(self.click_field_add)
		self.action_field_add_new.triggered.connect(self.click_field_add_new)
		self.action_field_delete.triggered.connect(self.click_field_delete)

	def __init_menu__(self):
		menu_main = QMenu("Действия")
		menu_main.addAction(self.action_save)
		menu_main.addAction(self.action_save_close)
		menu_main.addSeparator()
		menu_main.addAction(self.action_close)

		menu_fields = QMenu("Характеристики")
		menu_fields.addAction(self.action_field_add)
		menu_fields.addAction(self.action_field_add_new)
		menu_fields.addSeparator()
		menu_fields.addAction(self.action_field_delete)

		self.menuBar().addMenu(menu_main)
		self.menuBar().addMenu(menu_fields)

	def load(self):
		self.model_fields.clear()

	def load_and_show(self):
		self.load()
		self.showCentered()

	def click_field_add(self, in_category=None):
		if in_category is not None:
			new_field    = "Характеристика"

			new_field, result = QInputDialog.getText(self, "Новая характеристика", in_category, text=new_field)

			if result:
				self.model_fields.appendRow(QStandartItemWithID("{0}/{1}".format(in_category, new_field), None))

	def click_field_add_new(self):
		new_category = "Новая категория"

		new_category, result = QInputDialog.getText(self, "Новая категория", "Укажите названае новой категории", text=new_category)

		if result:
			self.click_field_add(new_category)

	def click_field_delete(self):
		pass