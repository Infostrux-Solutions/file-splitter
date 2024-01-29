import os, sys

        test_data = #TODO
        
        for model_file in test_data.split('#### split ####'):
            count = 0
            body = ''
            for line in model_file.splitlines():
                # Skip empty line if its the start
                if count == 0 and line.strip() == '':
                    continue

                # First line is path, second is filename 
                if count == 0:
                    output_path = line.strip('[').strip(']')
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                elif count == 1:
                    filename = line.strip('[').strip(']') 
                    output = os.path.join(output_path, filename)
                else:
                    body += line + '\n'    
                count += 1
            
            with open(output, 'w') as f:
                f.write(body)  