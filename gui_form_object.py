from core_gui     import *
from core_objects import *


class FormObject(CForm):
	model_fields = QStandardItemModel

	def __init_ui__(self):
		self.model_fields = QStandardItemModel()

		super(FormObject, self).__init_ui__()

		self.setMinimumSize(480, 600)
		self.setWindowTitle("[ID]: [Тип] - [Название]")
		self.setContentsMargins(0, 0, 0, 0)

		self._init_main_()

	def _init_main_(self):
		self.main_note  = QLineEdit()
		self.main_note.setPlaceholderText("Примечание")
		self.tabs       = QTabWidget()

		central_layout = QVBoxLayout()
		central_layout.setContentsMargins(3, 3, 3, 3)
		central_layout.setSpacing(3)
		central_layout.addWidget(self.tabs)
		central_layout.addWidget(self.main_note)

		central_widget = QWidget()
		central_widget.setLayout(central_layout)
		central_widget.setContentsMargins(0, 0, 0, 0)

		self.setCentralWidget(central_widget)

		self._init_tab_fields_()
		self._init_tab_transactions_()

	def _init_tab_fields_(self):
		self.tree_fields = QTreeView()
		self.tree_fields.setModel(self.model_fields)

	def _init_tab_transactions_(self):
		pass

	def load(self, in_id=None):
		pass

	def new(self):
		pass
