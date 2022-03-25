from utils.constants import STEP_STARTER


class Path:
    def __init__(self, str_path):
        self.str_path =str_path
        self.levels = str_path.split(STEP_STARTER)

    def __str__(self):
        return self.str_path

    def get_levels(self):
        return self.levels 
