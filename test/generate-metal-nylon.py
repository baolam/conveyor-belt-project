import sys
sys.path.append("./")

from src.preprocess import analyze
from src.constant import *

analyze(METAL_PATH)
analyze(NYLON_PATH)