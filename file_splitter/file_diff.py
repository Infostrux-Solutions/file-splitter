from typing import List, Dict
import os, sys
import difflib

    
def write_output( 
        output: str = None,
        output_name: str = None,
        output_path: str = None,
        overwrite: bool = True
    ):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    output_file_path = os.path.join(output_path, output_name)

        
    # Normal operation if not SQL or SQL does not exist
    if not os.path.exists(output_file_path) or output_name.split('.')[1].lower() != 'sql' or overwrite:
        with open(output_file_path, 'w') as f:
            f.write(output)

    # if exists - compare
    else:

        # compare
        old_data = ''
        with open(output_file_path, 'r') as f:
            old_data = f.readlines()
        
        new_data_flag = False
        index = 0
        while index in range(len(old_data)):
            line = old_data[index]
            if  line == f'=======\n':
                old_data.pop(index)
                new_data_flag = True
            elif line == f'>>>>>>> NEW\n' :
                old_data.pop(index)
                new_data_flag = False
            elif new_data_flag or line == f'<<<<<<< OLD\n':
                old_data.pop(index)
            else : index = index +1
        
        new_data = [line + '\n' for line in output.split('\n')]

        # if the new data has an empty line it will add an extra newline - remove this
        if new_data[-1] == '\n':
            new_data = new_data[:-1]

        # if old data last line lacks a newline add one
        if not old_data[-1].endswith('\n'):
            old_data[-1] = old_data[-1] + '\n'
        
        diff_data = list(difflib.unified_diff(old_data, new_data, fromfile = output_name, tofile = output_name))

        if len(diff_data) > 0:
            print('Differences detected! See below')

            for line in diff_data:
                startcode = '\033[0m'
                endcode = startcode
                if line.startswith('+'):
                    startcode = '\033[92m'
                elif line.startswith('-'):
                    startcode = '\033[91m'

                print(f'{startcode}{line}{endcode}', end='')

            # write out merge file
            full_diff_data = list(difflib.unified_diff(old_data, new_data, fromfile = output_name, tofile = output_name, n=100000))
            with open(output_file_path, 'w') as f:
                old = False
                new = False
                for line in full_diff_data:
                    if line.startswith(('---','+++','@@')):
                        continue

                    if line.startswith('-') and not old:
                        f.write(f'<<<<<<< OLD\n')
                        old = True

                    elif line.startswith((' ', '+')) and old:
                        f.write('=======\n')
                        old = False
                        new = True

                    elif line.startswith('+') and not new:
                        f.write(f'<<<<<<< OLD\n')
                        f.write('=======\n')
                        new =  True
                    
                    elif line.startswith((' ', '-')) and new:
                        f.write(f'>>>>>>> NEW\n')
                        new = False
                        if line.startswith('-'):
                            f.write(f'<<<<<<< OLD\n')
                            old = True

                    f.write(line[1:])
                
                if old:
                    f.write('=======\n')
                    f.write(f'>>>>>>> NEW\n')
                    
                if new:
                    f.write(f'>>>>>>> NEW\n')

        # otherwise no new changes
        else:
            with open(output_path, 'w') as f:
                f.write(output)   