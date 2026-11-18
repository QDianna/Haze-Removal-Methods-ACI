import os
import shutil

if os.path.exists("test_outputs"):
    shutil.rmtree("test_outputs")
    print("cleared test_outputs/")
else:
    print("test_outputs doesnt exist")