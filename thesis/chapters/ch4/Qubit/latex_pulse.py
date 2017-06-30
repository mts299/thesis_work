##
from pulse_graph import piecewiseConstantPlot
import sys


save_stdout = sys.stdout
sys.stdout = open('trash', 'w')

piecewiseConstantPlot(24,3)
sys.stdout = save_stdout

