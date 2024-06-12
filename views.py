import PyQt6.QtWidgets as QtWidgets
from PIL import ImageQt
from PyQt6.QtGui import QPixmap
import PyQt6.QtCore as QtCore


class CSVView(QtWidgets.QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.current_index = 0
        self.current_image = None
        self.initUI()

    def initUI(self):
        # View created in Qt designer and converted from .ui to Python code using PyQt6.uic
        # set window title and size
        self.setWindowTitle('CSV to Image Converter')
        self.setGeometry(100, 100, 800, 600)

        # Create widgets: buttons and labels and linking them with actions
        # Create central widget
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        # Create and set layout widget for Open and Save buttons
        self.layoutWidgetOS = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidgetOS.setGeometry(QtCore.QRect(0, 0, 158, 26))
        self.layoutWidgetOS.setObjectName("layoutWidgetOS")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.layoutWidgetOS)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontal_layout")
        # Create and set Open CSV button
        self.open_csv_button = QtWidgets.QPushButton("Open CSV", parent=self.layoutWidgetOS)
        self.open_csv_button.clicked.connect(self.open_csv)
        self.horizontal_layout.addWidget(self.open_csv_button)
        # Create and set Save Image button
        self.save_button = QtWidgets.QPushButton("Save Image", parent=self.layoutWidgetOS)
        self.save_button.clicked.connect(self.save_image)
        self.horizontal_layout.addWidget(self.save_button)
        # Create and set layout widget for Prev and Next buttons
        self.layoutWidgetNP = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidgetNP.setGeometry(QtCore.QRect(630, 565, 158, 26))
        self.layoutWidgetNP.setObjectName("layoutWidgetNP")
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self.layoutWidgetNP)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")
        # Create and set Prev button
        self.prev_button = QtWidgets.QPushButton("Prev", parent=self.layoutWidgetNP)
        self.prev_button.clicked.connect(self.prev_image)
        self.horizontal_layout_2.addWidget(self.prev_button)
        # Create and set Next button
        self.next_button = QtWidgets.QPushButton("Next", parent=self.layoutWidgetNP)
        self.next_button.clicked.connect(self.next_image)
        self.horizontal_layout_2.addWidget(self.next_button)
        # Create and set label for image display
        self.image_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(20, 40, 761, 521))
        self.image_label.setObjectName("label")
        # Set central widget
        self.setCentralWidget(self.centralwidget)

    def open_csv(self):
        select_files = QtWidgets.QFileDialog()
        select_files.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        select_files.setNameFilter("CSV files (*.csv)")

        if select_files.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            file_paths = select_files.selectedFiles()
            for filepath in file_paths:
                self.model.add_image(filepath)
            self.show_image()

    def show_image(self):
        if len(self.model.image_labels) > 0:
            self.current_image = self.model.get_current_image(self.current_index)
            if type(self.current_image) == str:
                self.image_label.setText("You have chosen an incorrect CSV file")
            else:
                qimage = ImageQt.ImageQt(self.current_image)
                pixmap = QPixmap.fromImage(qimage)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            if type(self.model.image_labels[-1]) == str:
                del self.model.image_labels[-1]
                del self.model.image_paths[-1]

    def prev_image(self):
        if len(self.model.image_labels) > 0:
            self.current_index = (self.current_index - 1) % len(self.model.image_labels)
            self.show_image()

    def next_image(self):
        if len(self.model.image_labels) > 0:
            self.current_index = (self.current_index + 1) % len(self.model.image_labels)
            self.show_image()

    def save_image(self):
        if len(self.model.image_labels) > 0:
            self.current_image = self.model.get_current_image(self.current_index)
            qimage = ImageQt.ImageQt(self.current_image)
            pixmap = QPixmap.fromImage(qimage)
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;BMP Files (*.bmp);;JPEG Files (*.jpg)")
            if filename:
                pixmap.save(filename)
