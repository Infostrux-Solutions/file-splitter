from lib.split import Splitter

def run():

    s = Splitter(input_file = 'tests/test_input_vernew.txt')
    s.open()
    s.split()
    s.write()

if __name__ == '__main__':
    run()