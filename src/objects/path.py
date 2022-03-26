from utils.constants import STEP_STARTER


class Path:
    def __init__(self, str_path):
        self.str_path =str_path
        self.levels = str_path.split(STEP_STARTER)
        self.levels.pop(0)

    def __str__(self):
        return self.str_path

    def get_levels(self):
        """
        Returns the levels of the path 

        For example /child::a/child::b will return 
        [child::a, child::b]
        """
        return self.levels 
