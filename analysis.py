import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols



if len(sys.argv) < 2:
    print(""" Usage: analysis_pcbs FILE
    Argument:
       FILE     : an .xpd file generated in `data` subfolder
    """)
    sys.exit()

data = pd.read_csv(sys.argv[1], comment='#')

correct_response=data['respkey']==data['expected_resp']
data['correct_response']=[int(b) for b in correct_response]

# testing some plots. sns catplot not very adapted here 

data.groupby('motion_coherence').mean()['correct_response'].plot()
plt.show()
data.groupby('motion_coherence').mean()['RT'].plot()
plt.show()




# TODO: save the plots in graphics files
