import uos as os


def add(filename, data):
    try:
        with open(filename, "a") as f:
            f.write(data)
        err = False
    except Exception as e:
        err = str(e)
    return err


def count_entries(filename):
    try:
        with open(filename) as f:
            full_file = f.read()
        counter = 0
        for line in full_file:
            if line[:2] == "===":
                counter += 1
    except Exception:
        pass
    return counter