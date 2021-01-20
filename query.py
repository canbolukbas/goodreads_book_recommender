import sys
import os

def single_url_recommendation(path):
    os.system("python single_url_recommendation.py {}".format(path))

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
