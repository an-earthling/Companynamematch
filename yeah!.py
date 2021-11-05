from os import linesep
import sas7bdat as sas

import itertools

path = './data/irm_all/irm_all.sas7bdat'

with sas.SAS7BDAT(path, skip_header=False) as reader:
    n = 5 # line number you want to read
    lines = itertools.islice(reader.readlines(), n)
    for i in lines:
        print(i)
    