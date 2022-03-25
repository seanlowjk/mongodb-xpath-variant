from json import load

class Executor:
    def __init__(self, json_file_data):
        self.json_data = load(json_file_data)
    
    def get_data(self):
        return self.json_data

    def has_path(self, path):
        return True 
