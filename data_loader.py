import json
from typing import List

import config
from model import Issue
from config import prompt_for_data_file

# Store issues as singleton to avoid reloads
_ISSUES:List[Issue] = None

class DataLoader:
    """
    Loads the issue data into a runtime object.
    """
    _data_path: str = None  # Class-level variable to store the selected file path

    def __init__(self):
        """
        Constructor
        """
        if DataLoader._data_path is None:
            DataLoader._data_path = prompt_for_data_file()
        self.data_path: str = DataLoader._data_path

    def get_issues(self):
        """
        This should be invoked by other parts of the application to get access
        to the issues in the data file.
        """
        global _ISSUES  # to access it within the function
        if _ISSUES is None:
            _ISSUES = self._load()
            print(f'Loaded {len(_ISSUES)} issues from {self.data_path}.')
        return _ISSUES
    
    def _load(self):
        """
        Loads the issues into memory.
        """
        with open(self.data_path,'r') as fin:
            return [Issue(i) for i in json.load(fin)]
    

if __name__ == '__main__':
    # Run the loader for testing
    DataLoader().get_issues()