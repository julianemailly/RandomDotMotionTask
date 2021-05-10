Hello everyone and welcome to this PCBS project !

## Description of the project

The goal of this project is to program a random dot motion (RDM) task which is typically used in perceptual decision making.
This task is quite simple : there is a certain amount of dots on the screen that are moving randomly, and some of them (for example 25%) are all moving towards the left or the right. The aim of the participant is to decide, as quickly as possible, in which direction the dots are moving. 
The percentage of motion coherence (i.e. what proportion of dots are moving in the same direction) can vary and the goal is to compute, for each participant, a psychometric function showing the percentage of correct answers according to the motion coherence of the stimulus.
The reaction time (RT) of the participant will also be recorded in ordre to compute it as a function of the motion coherence. 

Since this task is very famous, there is no specific article which is dedicated to present it. However, here is a [really interesting paper](https://www.sciencedirect.com/science/article/pii/S004269890900100X) comparing different RDM algorithms. The purpose of this project will be to code the "White Noise" algorithm which is the oldest one.

## How to install the experiment on your computer

To run this experiment on your computer, you will need Python and the following modules:
* expyriment
* numpy
* sys
* pandas
* matplotlib.pyplot
* seaborn

Now that you have installed Python and the required packages, you can download the folder containing the code [here](http://github.com/julianemailly/RandomDotMotionTask/archive/refs/heads/master.zip) and unzip it. The best is to place the unzipped folder in your home directory.

To run the experiment, use these commands in a terminal:

```
cd RandomDotMotionTask
python RandomDotMotionTask.py
```

Be careful! The folder is sometimes downloaded as `RandomDotMotionTask-master`. in this case, use `cd RandomDotMotionTask-master` instead of `cd RandomDotMotionTask`. 

## Analysis of the results

After the experiment is done, you will find a subfolder called `data` in the `RandomDotMotionTask` folder. In this subfolder, a `.xpd` file has been generated.

If you want to analyse the perforance of the participant, you can use the following command (in the `RandomDotMotionTask` folder as before):

```
python analysis.py data/your_xpd_file_in_data_folder.xpd
```

where `your_xpd_file_in_data_folder.xpd` needs to be replaced with the name of the `.xpd` file mentionned earlier.

Once the command is run, you should see two `.png` files in the `RandomDotMotionTask` folder:
1. A file named `psychometric_function_subject_ID.png` 
2. A file named `RT_function_subject_ID.png`
where `ID` should be the subject ID number you entered at the beginning of the experiment.

The first figure is the psychometric curve, i.e. the fraction of correct answers as a function of the motion coherence. The second one shows the reaction time as a function of the motion coherence. In both plots, the standard deviation is represented as a transparent band.

## Personal background

# My previous coding experience

I have a background in mathematics, physics and computer science (and also in psychology). I learned the basics of coding during my preparatory classes for the Grandes Ecoles, where I chose the computer science optional curriculum. We were using Python and Caml. During these two years, I had to do two projects (Travaux d'initiative Personnelle Encadrée) and I did them both in programming. I continued to use Python at the university in some classes and also in my intership this year (as well as ROS, which is not a language but is used to develop robot softwares). During this first year of Cogmaster, I have learned R for the Datacamp class but mostly for an external course about statistics and classification. I also had an algorithmics project during the first semester  (about the A-star algorithm). In a word, I have a good coding experience in several languages and I am quite used to this kind of projects.

### What I have learned since

I have learned a lot about coding experiments (and the expyriment and pygame modules in general), which is a skill that will be definitely useful for me. I also (re)discovered regular expressions that seem very helpful. But the most important in my opinion was the principles of clean code that I will try to use in my scripts from now on.


### What I missed in this course

I feel like there could have been a course dedicated to expyriment, which is not that easy to understand. Also, it might be relevant to divide this course into levels like Datacamp, so that everybody can learn at their own pace.