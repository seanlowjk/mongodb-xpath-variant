def get_full_path(path, attr):
    if path == "":
        return attr 

    return path + "." + attr

def split_path(path):
    return path.split(".")