'''
This script can be used to analyse the data from the Random Dot Motion Task experiment of the RandomDotMotionTask.py file. 
This code creates two plots: 
1. the proportion of correct responses as a function of the motion coherence (saved as 'psychometric_function_subject_id_subject.png')
2. the reaction time as a function of the motion coherence (saved as 'RT_function_subject_id_subject.png')
This script is meant to be used with the .xpd file generated in the data folder after you have run RandomDotMotionTask.py
The correct syntax is : python analysis.py path_to_you_xpd_file
'''

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if len(sys.argv) < 2:
    print(""" Usage: analysis_pcbs FILE
    Argument:
       FILE     : an .xpd file generated in `data` subfolder
    """)
    sys.exit()

data = pd.read_csv(sys.argv[1], comment='#')

correct_response=data['respkey']==data['expected_resp']
data['correct_response']=[int(b) for b in correct_response]

id_subject=str(data['subject_id'][0])


fig1=plt.figure()
sns.lineplot(data=data, x="motion_coherence", y="correct_response", err_style="band",ci='sd')
plt.xlabel('% of motion coherence')
plt.ylabel('proportion of correct responses')
plt.title('Psychometric function')

plt.savefig('psychometric_function_subject_'+id_subject+'.png')


fig2=plt.figure()
sns.lineplot(data=data, x="motion_coherence", y="RT", err_style="band",ci='sd')
plt.xlabel('% of motion coherence')
plt.ylabel('reaction time (ms)')
plt.title('Reaction time according to the motion coherence of the dots')

plt.savefig('RT_function_subject_'+id_subject+'.png')