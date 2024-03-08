from lib.split import Splitter
import argparse

def run():

    parser = argparse.ArgumentParser(description = 'Split a file by a delimiter')
    parser.add_argument('-f', '--file', help = 'The file to be split', required = True)
    parser.add_argument('-d','--delimiter', help = 'The delimiter to split on', required = False)

    args = parser.parse_args()

    s = Splitter(input_file = args.file, delimiter = args.delimiter)
    s.process()

if __name__ == '__main__':
    run()
