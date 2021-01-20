import sys
import os
from single_url_recommendation import *
from build_model import *

def single_url_recommendation(path):
    main(path)

def build_model(path):
    build_model_main(path)

def is_url(path):
    if path[:5]=="https":
        return True

# Read path from command line arguments
path = sys.argv[1]
if is_url(path):
    single_url_recommendation(path)
else:
    build_model(path)
