def get_full_path(path, attr):
    if path == "":
        return attr 

    return path + "." + attr