from dataclasses import dataclass, field
from typing import List, Dict
import os
import sys

@dataclass
class File:
    """
        Represents a single file
    """

    # File metadata
    # Body is a List of strings to be outputted
    body:       List = field(default_factory=lambda: [])
    filepath:   str  = None
    filename:   str  = None 

    # Write the contents of the body to the file
    def write(self):

        if not os.path.exists(self.filepath):
             os.makedirs(self.filepath)
        
        output = os.path.join(self.filepath, self.filename)

        with open(output, 'w') as o:
            o.write(self.body)