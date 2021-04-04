import os


def read(filename, delimiter=","):
    try:
        with open(filename) as f:
            csv_data = f.read()
    except Exception:
        return []
    csv_lines = csv_data.split("\n")
    lines = []
    for line in csv_lines:
        line = line.strip()
        lines.append(line.split(delimiter))
    return lines


def _parse_list_to_csv(data, delimiter):
    csv = ""
    if type(data) != list:
        data = [data]
    for line in data:
        csv += delimiter.join([str(i) for i in line]) + "\n"
    return csv


def overwritewrite(data, filename, delimiter=","):
    _write(data, filename, delimiter, "w+")


def add(data, filename, delimiter=","):
    _write(data, filename, delimiter, "a")


def _write(data, filename, delimiter, mode):
    csv = _parse_list_to_csv(data, delimiter)
    with open(filename, mode) as f:
        f.write(csv)


# class CSV:

#     def read(self, filename, delimiter=","):
#         self.filename = filename
#         self.delimiter = delimiter

#         with open(filename) as f:
#             file_data = f.read()

#         data_list = []
#         lines = file_data.split("\n")
#         for line in lines:
#             data_list.append(line.split(delimiter))
