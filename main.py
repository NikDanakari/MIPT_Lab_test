import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,  QImage
from PyQt6.QtCore import Qt
from PIL import ImageQt
import csv_processor

# custom class for window
class Solution(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        # set window title and size
        self.setWindowTitle('CSV to Image Converter')
        self.setGeometry(100, 100, 800, 600)
        # create lists for labels and paths - neccessary for navigation
        self.image_labels = []
        self.image_paths = []
        self.current_image_index = 0
        # create central widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # create layout for central widget
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        # create and set open button
        self.openButton = QPushButton('Open CSV', self)
        self.openButton.clicked.connect(self.open_csv)
        self.layout.addWidget(self.openButton)
        # create and set previous image button
        self.prev_button = QPushButton("Previous Image", self)
        self.prev_button.clicked.connect(self.show_prev_image)
        self.layout.addWidget(self.prev_button)
        # create and set next image button
        self.next_button = QPushButton("Next Image", self)
        self.next_button.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next_button)
        # create and set save button
        self.saveButton = QPushButton('Save Image', self)
        self.saveButton.clicked.connect(self.saveImage)
        self.layout.addWidget(self.saveButton)
        #create image label
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        self.image = None
    #call custom csv2image converter
    def converter(self, filepath):
        return csv_processor.csv_to_image(filepath)
    # method to open and operate with files
    def open_csv(self):
        select_files = QFileDialog()
        select_files.setFileMode(QFileDialog.FileMode.ExistingFiles)
        select_files.setNameFilter("CSV files (*.csv)") # Set filter to view only .csv files
        
        # If user pushes "open" in file dialog
        if select_files.exec() == QFileDialog.DialogCode.Accepted:
            file_paths = select_files.selectedFiles() # get list of selected files
            # create image and set pixmap for every selected file
            for filepath in file_paths:
                self.image = self.converter(filepath)
                if type(self.image) == str:
                    raise ValueError(self.image)
                qimage = ImageQt.ImageQt(self.image)
                pixmap = QPixmap.fromImage(qimage)

                # set image label and scale it
                image_label = QLabel(self)
                image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

                # add image label and path to lists
                self.image_labels.append(image_label)
                self.image_paths.append(filepath)

            self.show_image()
    # method to show current image
    def show_image(self):

        # non-empty checker
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index] # get current image label
            self.image_label.setPixmap(current_image.pixmap()) # set current image label to pixmap 
    
    # method to switch to the next image
    def show_prev_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_labels) # count prev image index with looping
            self.show_image()

    # method to switch to the previous image
    def show_next_image(self):
        if len(self.image_labels) > 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_labels) # count next image index with looping
            self.show_image()
    # save image 
    def saveImage(self):
        if len(self.image_labels) > 0:
            current_image = self.image_labels[self.current_image_index]
            pixmap = current_image.pixmap() # get current image
        # open save dialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;BMP Files (*.bmp);;JPEG Files (*.jpg)") # list of formats to choose from
        if filename:
            pixmap.save(filename)


def main():
    app = QApplication(sys.argv)

    window = Solution()
    window.show()
    app.exec()
#execute main function
if __name__ == "__main__":
    main()