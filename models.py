import csv_processor


class CSVModel:
    def __init__(self):
        self.image_paths = []
        self.image_labels = []

    def convert_csv_to_image(self, filepath):
        return csv_processor.csv_to_image(filepath)
    # add every image to paths and labels list
    def add_image(self, filepath):
        image = self.convert_csv_to_image(filepath)
        self.image_paths.append(filepath)
        self.image_labels.append(image)

    def get_current_image(self, index):
        return self.image_labels[index]