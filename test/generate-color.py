import sys
sys.path.append("./")

from src.preprocess import analyze
from src.constant import *

analyze(RED_PATH)
analyze(YELLOW_PATH)