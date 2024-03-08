# File-Splitter

## Background
This is a Python Utility that can split a large file into smaller files with given metadata
A Python utility that can split a large file into smaller files with given metadata

## Usage
You can use the splitter either as a module or as a command line utility:

## Installation
Install the requirements file via (it is recommeneded to run this in a Python Virtual Environment):

```
pip install -r requirements.txt
```
### Command line Usage
To run the splitter in the command line, pass in the name of the file (and optionally the delimiter to split by):
```
python main.py -f [FILE] -d [DELIMITER]
```
This will split the file and output the newly created files at their destination that was specified by the metadata. If the path to the output does not exist the program will automatically create the needed folders.

### As a module
To use it as a module you can simply copy the `file.py` and `split.py` files in the `lib/` folder and import as such in your project:

```
from lib.split import Splitter
```

You can then run the `Splitter` class by instantiating a new instance and calling the `process()` module:
```
s = Splitter('file.txt')
s.process()
```

## Formatting
The splitter takes in a file that is separated by a delimiter that indicates the start of a new page. The first two non empty lines of a file is considered to be the metadata of the file: they represent the output location and name of the file. An example is shown below (note the metadata is encapsulated with square brackets):

```
[/output/f1]
[file1.txt]

This is file 1!

##### splitter #####
[/output/f2]
[file2.txt]

This is file 2!

```

## Delimiter Notes:
The delimiter you pass in specifies the string that will indicate where a file split should occur. By default this is set to `##### splitter #####`. Alternatively you can override this by passing in your down custom delimiter, either as a commandline argument (`-d DELIMITER`) or by passing it during class creation (`Splitter(input_file='file1.txt, delimieter='my_new_delimiter')`)