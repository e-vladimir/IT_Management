from core_gui     import *
from core_objects import *


class FormEquipment(CForm):
	_groups            = CCatalogFieldGroups
	_group             = CCatalogFieldGroup

	_equipments        = CEquipments
	_equipment         = CEquipment

	_transactions      = CTransactions
	_transaction       = CTransaction

	model_fields       = QStandardItemModel
	model_transactions = QStandardItemModel
	tree_fields        = QTreeView

	current_main_group = None
	current_main_field = None
	current_main_value = None

	current_transaction = None

	def __init_actions__(self):
		self.action_save           = QAction(self.icon_small_save,   "Сохранить",               None)
		self.action_save_and_close = QAction(self.icon_small_save,   "Сохранить и закрыть",     None)
		self.action_save_as_copy   = QAction(self.icon_small_save,   "Сохранить как копию",     None)
		self.action_delete         = QAction(self.icon_small_delete, "Удалить",                 None)
		self.action_load           = QAction(self.icon_small_open,   "Загрузить",               None)
		self.action_close          = QAction(self.icon_small_close,  "Закрыть",                 None)

		self.action_field_add      = QAction(self.icon_small_insert, "Добавить характеристику", None)
		self.action_field_delete   = QAction(self.icon_small_delete, "Удалить характеристику",  None)

		self.action_field_up       = QAction(self.icon_small_up,     "Переместить выше",        None)
		self.action_field_down     = QAction(self.icon_small_down,   "Переместить ниже",        None)

		self.action_transaction_note   = QAction(self.icon_small_note,   "Записать примечание",        None)
		self.action_transaction_delete = QAction(self.icon_small_delete, "Удалить транзакцию",        None)

	def __init_events__(self):
		self.tree_fields.expanded.connect(self._gui_resize_fields)
		self.tree_fields.collapsed.connect(self._gui_resize_fields)

		self.tree_fields.clicked.connect(self._get_current_main)

		self.table_transactions.clicked.connect(self._get_current_transaction)
		self.table_transactions.doubleClicked.connect(self.transaction_set_note)
		self.table_transactions.expanded.connect(self._gui_resize_fields)
		self.table_transactions.collapsed.connect(self._gui_resize_fields)

		self.list_values.doubleClicked.connect(self._select_value)

		self.action_save.triggered.connect(self.save)
		self.action_save_as_copy.triggered.connect(self.save_copy)
		self.action_save_and_close.triggered.connect(self.save_and_close)

		self.action_delete.triggered.connect(self.delete)

		self.action_load.triggered.connect(self.load)
		self.action_close.triggered.connect(self.close)

		self.action_field_delete.triggered.connect(self._field_delete)
		self.action_field_add.triggered.connect(self._field_add)

		self.action_field_up.triggered.connect(self._field_up)
		self.action_field_down.triggered.connect(self._field_down)

		self.action_transaction_note.triggered.connect(self.transaction_set_note)
		self.action_transaction_delete.triggered.connect(self.transaction_delete)

	def __init_icons__(self):
		self.icon_small_insert       = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete       = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_open         = QIcon(self.application.PATH_ICONS_SMALL + "table_open.png")
		self.icon_small_save         = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_close        = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_fields       = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

		self.icon_small_up           = QIcon(self.application.PATH_ICONS_SMALL + "arrow_up.png")
		self.icon_small_down         = QIcon(self.application.PATH_ICONS_SMALL + "arrow_down.png")

		self.icon_small_transactions = QIcon(self.application.PATH_ICONS_SMALL + "transactions.png")

		self.icon_small_note         = QIcon(self.application.PATH_ICONS_SMALL + "note.png")

	def __init_objects__(self):
		self._groups            = CCatalogFieldGroups(self.application.sql_connection)
		self._group             = CCatalogFieldGroup(self.application.sql_connection)

		self._equipments        = CEquipments(self.application.sql_connection)
		self._equipment         = CEquipment(self.application.sql_connection)

		self._transactions      = CTransactions(self.application.sql_connection)
		self._transaction       = CTransaction(self.application.sql_connection)

		self.model_fields       = QStandardItemModel()
		self.model_transactions = QStandardItemModel()

	def __init_menu__(self):
		menu_actions = QMenu("Действия")
		menu_actions.addAction(self.action_save)
		menu_actions.addAction(self.action_save_and_close)
		menu_actions.addAction(self.action_save_as_copy)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_load)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_delete)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_close)

		menu_fields = QMenu("Характеристики")
		menu_fields.addAction(self.action_field_add)
		menu_fields.addAction(self.action_field_delete)
		menu_fields.addSeparator()
		menu_fields.addAction(self.action_field_up)
		menu_fields.addAction(self.action_field_down)

		menu_transactions = QMenu("Транзакции")
		menu_transactions.addAction(self.action_transaction_note)
		menu_transactions.addSeparator()
		menu_transactions.addAction(self.action_transaction_delete)

		self.menuBar().addMenu(menu_actions)
		self.menuBar().addMenu(menu_fields)
		self.menuBar().addMenu(menu_transactions)

	def __ui__(self):
		self.setWindowTitle("ОС и ТМЦ")
		self.setMinimumSize(640, 480)

		self._init_tabs()

	def _init_tab_main(self):
		self.tree_fields = QTreeView()
		self.tree_fields.setMinimumWidth(450)
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()
		self.tree_fields.setAlternatingRowColors(True)

		self.list_values = QListWidget()

		splitter_main = QSplitter()
		splitter_main.setContentsMargins(3, 3, 3, 3)
		splitter_main.addWidget(self.tree_fields)
		splitter_main.addWidget(self.list_values)

		self.tabs.addTab(splitter_main, self.icon_small_fields, "Характеристики")

	def _init_tab_transactions(self):
		self.table_transactions = QTreeView()
		self.table_transactions.setModel(self.model_transactions)
		self.table_transactions.setEditTriggers(QTableView.NoEditTriggers)
		self.table_transactions.setSelectionBehavior(QTableView.SelectRows)

		self.tabs.addTab(self.table_transactions, self.icon_small_transactions, "Транзакции")

	def _init_tabs(self):
		self.tabs = QTabWidget()
		self.field_note = QLineEdit()
		self.field_note.setPlaceholderText("Примечание")

		central_layout = QVBoxLayout()
		central_layout.setContentsMargins(3, 3, 3, 3)
		central_layout.setSpacing(3)
		central_layout.addWidget(self.tabs)
		central_layout.addWidget(self.field_note)

		central_widget = QWidget()
		central_widget.setLayout(central_layout)

		self.setCentralWidget(central_widget)

		self._init_tab_main()
		self._init_tab_transactions()

	def _field_add(self):
		_dialog = QInputDialog()

		_text, _result = _dialog.getText(self, "Новая характеристика", "Категория: {}".format(self.current_main_group.text()))

		if _result:
			self.current_main_group.appendRow([QStandardItemWithID(_text), QNoneModelItem()])

	def _field_delete(self):
		_row = self.current_main_field.row()

		self.current_main_group.removeRow(_row)

		self._get_current_main()

	def _field_down(self):
		current_row = self.current_main_field.row()
		_row        = self.current_main_group.takeRow(current_row)

		self.current_main_group.insertRow(current_row + 1, _row)
		self.tree_fields.setCurrentIndex(self.model_fields.indexFromItem(self.current_main_field))

		self._get_current_main()

	def _field_up(self):
		current_row = self.current_main_field.row()
		_row        = self.current_main_group.takeRow(current_row)

		self.current_main_group.insertRow(current_row - 1, _row)
		self.tree_fields.setCurrentIndex(self.model_fields.indexFromItem(self.current_main_field))

		self._get_current_main()

	def _get_current_main(self):
		self.current_main_group = None
		self.current_main_field = None
		self.current_main_value = None

		_current_index = self.tree_fields.currentIndex()
		_current_row   = _current_index.row()
		_current_item  = self.model_fields.itemFromIndex(_current_index)

		if _current_item is not None:
			_current_parent = _current_item.parent()

			if _current_parent is None:
				self.current_main_group = _current_item
			else:
				self.current_main_group = _current_parent
				self.current_main_field = _current_parent.child(_current_row, 0)
				self.current_main_value = _current_parent.child(_current_row, 1)

		self._load_list_values()
		self._gui_enable_disable()

	def _get_current_transaction(self):
		_current_index = self.table_transactions.currentIndex()
		_current_item  = self.model_transactions.itemFromIndex(_current_index)

		self.current_transaction = _current_item

	def _gui_enable_disable(self):
		self.action_field_add.setEnabled(self.current_main_group is not None)

		self.action_field_delete.setEnabled(self.current_main_field is not None)

		if self.current_main_field is not None:
			self.action_field_delete.setText("Удалить: " + self.current_main_field.text())

			self.action_field_up.setEnabled(self.current_main_field.row() > 0)
			self.action_field_down.setEnabled(self.current_main_field.row() < (self.current_main_group.rowCount() - 1))
		else:
			self.action_field_delete.setText("Удалить характеристику")

			self.action_field_up.setEnabled(False)
			self.action_field_down.setEnabled(False)

	def _gui_resize_fields(self):
		self.tree_fields.resizeColumnToContents(0)

		for _id_column in range(self.model_transactions.columnCount()):
			self.table_transactions.resizeColumnToContents(_id_column)

	def _load_fields(self):
		list_groups = self._groups.get_list()

		for group in list_groups:
			self._group.load(group)

			item_group = QStandardItemWithID(self._group.name)
			item_group.setCheckable(True)

			list_fields = self._group.get_fields()
			for field in list_fields:
				item_group.appendRow([QStandardItemWithID(field), QStandardItemWithID("")])

			self.model_fields.appendRow([item_group, QNoneModelItem()])

	def _load_list_values(self):
		self.list_values.clear()

		if self.current_main_field is not None:
			_group = self.current_main_group.text()
			_field = self.current_main_field.text()

			_values = self._equipment.get_values_by_field(_group, _field)

			if _values is not None:
				self.list_values.addItems(_values)

	def _load_transactions(self):
		self.model_transactions.clear()

		_list_id    = self._transactions.get_list_id_by_object(self._equipment.id)
		_list_dates = self._transactions.get_list_date_by_object(self._equipment.id)

		for _date in _list_dates:
			_item_data = QStandardItemWithID(_date)

			for _id in _list_id:
				self._transaction.load(_id)

				if self._transaction.date == _date:
					_item_field = QStandardItemWithID(self._transaction.field, _id)
					_item_value = QStandardItemWithID(self._transaction.value, _id)
					_item_note  = QStandardItemWithID(self._transaction.note,  _id)

					_item_data.appendRow([_item_field, _item_value, _item_note])

			self.model_transactions.appendRow([_item_data, QNoneModelItem(), QNoneModelItem()])

		self.table_transactions.sortByColumn(0, Qt.AscendingOrder)
		self.model_transactions.setHorizontalHeaderLabels(["Данные", "Значение", "Примечание"])

		self._gui_resize_fields()

	def _load_title(self):
		self.setWindowTitle("{} - {} {}".format(self._equipment.base.subcategory,
		                                        self._equipment.base.brand,
		                                        self._equipment.base.model))

	def _select_value(self):
		_item  = self.list_values.currentItem()
		_value = _item.text()

		self.current_main_value.setText(_value)

	def _set_field(self, in_field="", in_value=""):
		_group = extract_field_group(in_field)
		_field = extract_field_name(in_field)

		_item_group = None
		_item_field = None
		_item_value = QStandardItemWithID(in_value)

		for _index_row in range(self.model_fields.rowCount()):
			_item_group = self.model_fields.item(_index_row)

			if _item_group.text() == _group:
				for _index_subrow in range(_item_group.rowCount()):
					_item_field = _item_group.child(_index_subrow)

					if _item_field.text() == _field:
						_item_group.setChild(_index_subrow, 1, _item_value)
						_item_group.setCheckState(Qt.Checked)

						break
				else:
					_item_group.setCheckState(Qt.Checked)
					_item_group.appendRow([QStandardItemWithID(_field), _item_value])

				if _item_group.checkState() == Qt.Checked:
					self.tree_fields.setExpanded(self.model_fields.indexFromItem(_item_group), True)

				break
		else:
			_item_group = QStandardItemWithID(_group)
			_item_group.setCheckable(True)
			_item_group.appendRow([QStandardItemWithID(_field), _item_value])
			self.model_fields.appendRow([_item_group, QNoneModelItem()])

	def delete(self):
		_dialog = QMessageBox()

		_result = _dialog.question(self,
		                           "Удаление ОС и ТМЦ",
		                           "Подтвердите удаление: {} {}".format(self._equipment.base.brand,
		                                                                self._equipment.base.model),
		                           QMessageBox.Yes | QMessageBox.No)

		if _result == QMessageBox.Yes:
			self._equipment.delete()

			self.close()

			self.application.form_main.equipments_load()

	def load(self, in_id=None):
		self.model_fields.clear()

		self._load_fields()

		if in_id is not None:
			self._equipment.load(in_id)
		else:
			self._equipment.load()

		self.field_note.setText(self._equipment.note)

		self._load_title()

		_list_fields = self._equipment.fields.get_list()

		for _field in _list_fields:
			_value = self._equipment.fields.get_field(_field)

			self._set_field(_field, _value)

		self._load_transactions()

		self._gui_resize_fields()

		if not self.isVisible():
			self.tabs.setCurrentIndex(0)

		self.showCentered()
		self._get_current_main()

	def new(self):
		self._equipment.clear(True)
		self.load()

	def new_and_show(self):
		self.new()
		self.show()

	def save(self):
		if self._equipment.id is not None:
			self._equipment.stasis_fields()

		self._equipment.clear()

		_id_obj = self._equipment.id

		for index_group in range(self.model_fields.rowCount()):
			item_group = self.model_fields.item(index_group)
			group      = item_group.text()

			if item_group.checkState() == Qt.Checked:
				for index_field in range(item_group.rowCount()):
					item_field = item_group.child(index_field, 0)
					item_value = item_group.child(index_field, 1)

					field      = item_field.text()
					value      = item_value.text()

					self._equipment.set(group, field, value)

		self._equipment.note = self.field_note.text()

		self._equipment.save()

		self.load()

		self.application.form_main.equipments_load()
		self.application.form_main.equipments_jump_to_id(self._equipment.id)

	def save_and_close(self):
		self.save()
		self.close()

	def save_copy(self):
		self._equipment.id = None
		self.save()

	def show(self, *args, **kwargs):
		super(FormEquipment, self).show(*args, **kwargs)

		self.action_load.setEnabled(self._equipment.id is not None)
		self.action_delete.setEnabled(self._equipment.id is not None)

	def transaction_set_note(self):
		_row = None

		if self.current_transaction is not None:
			_row = self.current_transaction.row()
			_item_note = self.model_transactions.item(_row, 3)

			_dialog = QInputDialog()
			_note, result = _dialog.getText(self, "Примечание к транзакции", "Введите примечание", text=_item_note.text())

			if result:
				self._transaction.load(_item_note.id)
				self._transaction.note = _note
				self._transaction.save()

				_item_note.setText(_note)

				self._gui_resize_fields()

	def transaction_delete(self):
		_row = None

		if self.current_transaction is not None:
			_row = self.current_transaction.row()
			_item_date  = self.model_transactions.item(_row, 0)
			_item_field = self.model_transactions.item(_row, 1)
			_item_value = self.model_transactions.item(_row, 2)
			_item_note  = self.model_transactions.item(_row, 3)

			_date  = _item_date.text()
			_field = _item_field.text()
			_value = _item_value.text()
			_note  = _item_note.text()

			_dialog = QMessageBox()

			_result = _dialog.question(self,
			                           "Удаление транзакции",
			                           "Подтвердите удаление транзакции: \n{} - {} = {} \nПримечание: {}".format(_date, _field, _value, _note),
			                           QMessageBox.Yes | QMessageBox.No)

			if _result == QMessageBox.Yes:
				self._transaction.id = _item_date.id
				self._transaction.delete()

				self._load_transactions()
