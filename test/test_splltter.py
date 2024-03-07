from lib.split import Splitter
import pytest

def split_obj():
    return Splitter(input_file = './test/input/sample.txt')

def get_config(num):

    if num == 1:
        filename = 'test/output/f1/config1.yml'
    elif num == 2:
        filename = 'test/output/f2/config2.yml'
    
    with open(filename, 'r') as f:
        data = f.read()

    return data

def test_split():
    s = split_obj()
    s.open()
    s.split()
    assert len(s.file_list) == 2

def test_metadata():
    s = split_obj()
    s.open()
    s.split()   
    assert s.file_list[0].body == get_config(1)
    assert s.file_list[1].body == get_config(2)