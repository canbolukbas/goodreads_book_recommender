import sys
import os
from single_url_recommendation import *

def single_url_recommendation(path):
    main(path)

def build_model(path):
    os.system("python build_model.py {}".format(path))

def is_url(path):
    if path[:5]=="https":
        return True

path = sys.argv[1]
if is_url(path):
    single_url_recommendation(path)
else:
    build_model(path)
