from core_gui       import *
from core_sqlite    import *

from gui_form_main  import FormMain


class AppManage(CApplication):
	sql_connection = None

	version = "180206/1321"

	def init_sql(self):
		self.sql_connection = TSQLiteConnection('{0}/{1}'.format(self.PATH_COMMON, "db.sqlite"))

	def __init_forms__(self):
		self.form_main       = FormMain(self)


app = AppManage()
app.form_main.showMaximized()
sys.exit(app.exec_())
