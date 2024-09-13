from pathlib import Path
import ast

def read_smsnums():
    smsnumbers = Path('../resources/smsnumbers')
    with open(smsnumbers, 'r') as smsnums:
        contents = smsnums.read()
        if contents:
            contents = ast.literal_eval(contents)
            print(contents)
            return contents


def empty_smsnums():
    smsnumbers = Path('../resources/smsnumbers')
    with open(smsnumbers, "w") as smsnums:
        smsnums.truncate(0)


def write_smsnums(content):
    smsnumbers = Path('../resources/smsnumbers')
    with open(smsnumbers, 'w') as smsnums:
        smsnums.write("{}".format(content))
