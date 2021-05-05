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