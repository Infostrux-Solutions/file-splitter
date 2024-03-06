from dataclasses import dataclass, field
from lib.file import File
from typing import List, Dict
import os
import sys

@dataclass
class Splitter:
    """
        Splits a file based on the supplied metadata header
    """

    # Optional inputs. Not required to load during init
    # Sets the:
    # - default spliiter syntax
    # - default output path
    # - data packet ->  if you have a custom data stream and want to customize the handling 
    delimiter:           str = '##### splitter #####'
    input_file:          str = None
    raw_data:            str = None
    default_output_path: str = None
    file_list:          List = field(default_factory=lambda: [])

    # open the file and dump the data
    def open(self):

        if not os.path.exists(self.input_file):
            sys.exit(f'File {self.input_file} does not exist.')

        with open(self.input_file,  'r') as f:
            self.raw_data = f.read()

    # write the files defined in the filelist
    def write(self):

        if len(self.file_list) == 0:
            sys.exit('Nothing to write!')

        for file in self.file_list:
            file.write()

    # Performs the following processes
    # 1. Opens the file
    # 2. Splits it into spearate files
    # 3. Writes to output
    # Function is meant to be an all in one solution
    def process(self):
        self.open()
        self.split()
        self.write()

    # Reads the data and sets the metadata based on the header
    # Header info should be encapsulated with square brackets and be the first couple of lines of the data
    # trim_whitespace auto trims all whitespace surrounding the header, auto set to True
    # Sample Header is:
    # [/home/kasm-user/workspace/auto-dbt-framework/target/tests] <= output location
    # [config.yml] <= filename
    def read_header(self, raw_data = None, trim_whitespace = True):

        filepath = ''
        filename = ''
        body     = '' 

        metadata_counter = 0   
        
        # Split the raw_data into lines
        raw_data_lines = raw_data.splitlines(keepends=False)

        for ndx, line in enumerate(raw_data_lines):
            
            if trim_whitespace:
                if metadata_counter == 0 and line.strip() == '':
                    continue

            # next two lines are headers
            if metadata_counter == 0:
                filepath = line.strip('[').strip(']') 
                metadata_counter += 1
            elif metadata_counter == 1:
                filename = line.strip('[').strip(']') 
                metadata_counter +=1
            # keep everything else
            else: 
                body = '\n'.join(raw_data_lines[ndx:])
                break
  
        file = File(filepath = filepath, filename = filename, body = body)
        return file

    # Splits by the delimiter
    def split(self):
        
        if self.raw_data is None: 
            sys.exit("No data detected. Make sure you have opened the file or check your file's contents.")

        for ndx, chunk in enumerate(self.raw_data.split(self.delimiter)):
            
            # Skip empty files
            if chunk.strip() == '':
                continue
            
            file = self.read_header(raw_data = chunk)
            self.file_list.append(file)

    
