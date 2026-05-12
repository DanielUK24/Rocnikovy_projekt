from src.ui.main_window import MainWindow
from src.ui.connection_window import ConnectionWindow

class AppController:
    
    def _successful_connect(self, connection_data):
        self._connection_data = connection_data
        self._main_window = MainWindow(self._set_connection)
        self._connection_window.close()
        self._main_window.show()

    def _set_connection(self):
        self._connection_window.set_inputs(self._connection_data)
        self._main_window.close()
        self._connection_window.show()

    def run_app(self):

        self._connection_window = ConnectionWindow(self._successful_connect)
        self._connection_window.show()