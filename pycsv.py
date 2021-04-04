class Csv:
    def __init__(self, data, delimiter=",", filename=""):
        self.data = data
        self.delimiter = delimiter
        self.filename = filename

    def read(self):
        csv_data = []
        with open(self.filename) as f:
            i = f.readlines()
            for line in i:
                csv_data.append(line.split(self.delimiter))
        return csv_data

C = Csv()