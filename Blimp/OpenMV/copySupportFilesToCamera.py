import os
from distutils.dir_util import copy_tree
currDir = os.path.dirname(__file__);
# copy subdirectory example
from_directory = currDir + "\support"
to_directory = "E:/"

copy_tree(from_directory, to_directory)

