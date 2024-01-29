import sys
sys.path.append('./')
from file_splitter import file_diff

def main():
    with open('./tests/test_input.sql', 'r') as file:
        data = file.read()

    file_diff.write_output(
        output=data, 
        output_name='test_output.sql',
        output_path='./tests/output_dir/',
        overwrite=False
    )


main()