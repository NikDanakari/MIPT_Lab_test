import sys
from PyQt6.QtWidgets import QApplication
import views, models


# custom application class to assemble app from model and view
class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = models.CSVModel() # initializing a model
        self.main_view = views.CSVView(self.model) # initializing a view using model
        self.main_view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    app.exec()