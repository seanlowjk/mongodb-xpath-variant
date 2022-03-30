from utils.constants import STEP_STARTER, STEP_SEPERATOR


class Path:
    def __init__(self, str_path):
        self.str_path = str_path

    def __str__(self):
        return self.str_path

    def get_parts(self):
        return self.str_path.split("::")
