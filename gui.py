from core_gui import *
from gui_form_main      import FormMain
from core_sqlite import *


class AppManage(CApplication):
	sql_connection = None

	version = "180206/1321"

	def init_sql(self):
		self.sql_connection = TSQLiteConnection('{0}/{1}'.format(self.PATH_COMMON, "db.sqlite"))

	def __init_forms__(self):
		# Костыль
		self.init_sql()

		self.form_main       = FormMain(self)


app = AppManage()
app.form_main.show()
sys.exit(app.exec_())
