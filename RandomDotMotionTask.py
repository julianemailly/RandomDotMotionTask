from expyriment import design, control, stimuli, misc
import random as r 
import numpy as np 
import math as m 

LEFT_RESPONSE=misc.constants.K_LEFT
RIGHT_RESPONSE=misc.constants.K_RIGHT
MOTION_COHERENCE=np.tile(np.linspace(0,100,5),5)
NUMBER_TRIALS=len(MOTION_COHERENCE)
MAX_RESPONSE_DELAY=5000
COLOR_OF_ARENA=misc.constants.C_GREY
COLOR_OF_DOTS=misc.constants.C_WHITE
RADIUS_OF_ARENA=100
RADIUS_OF_DOTS=5
WIDTH_INNER_SQUARE=2*RADIUS_OF_ARENA/m.sqrt(2)

exp = design.Experiment(name="Random Dot Motion Task")
control.initialize(exp)

cue = stimuli.FixCross(size=(50, 50), line_width=4)
blankscreen = stimuli.BlankScreen()
instructions = stimuli.TextScreen("Instructions",
    f"""blablabla.""")


trials=np.random.shuffle(MOTION_COHERENCE)

def distance_to_center(point):
    x,y=point[0],point[1]
    return(m.sqrt(x**2+y**2))

def generate_random_position_in_arena() : 
	x=np.random.random()*WIDTH_INNER_SQUARE-(WIDTH_INNER_SQUARE/2)
	y=np.random.random()*WIDTH_INNER_SQUARE-(WIDTH_INNER_SQUARE/2)
	return(x,y)

def generate_n_dots(n_dots):
	positions=[generate_random_position_in_arena() for k in range (n_dots)]
    dot_list=[]
    for i in range (n_dots) :
        dot_list.append(stimuli.Circle(radius=RADIUS_OF_DOTS, colour=COLOR_OF_DOTS),position=positions[i])
    return(dot_list)

def split_dot_list(motion_coherence,dot_list): #wanted to use np.random.choice but cannot have 2 lists in the end
    dots_belong_to_coherent_list=np.random.binomial(1,motion_coherence/100,len(dot_list))
    coherent_dots=[]
    random_dots=[]
    for k in range (len(dot_list)) :
    	if dots_belong_to_coherent_list[k]==1 : 
    		coherent_dots.append(dot_list[k])
    	else : 
    		random_dots.append(dot_list[k])
    return(coherent_dots,random_dots)

def coherent_movement(dot_list,direction) : 
    if direction=='left' :
        movement=[-1,0]
    elif direction=='right':
        movement=[1,0]
    for dot in dot_list :
        dot.move(movement)


def random_movement(dot_list) : 
	for dot in dot_list : 
		movement=[np.random.random*2-1,np.random.random*2-1]
		dot.move(movement)

def dots_out_of_arena(dot_list) : 
	for dot in dot_list : 
		if distance_to_center(dot.position)>RADIUS_OF_ARENA : 
			dots_out_of_arena.append(dot)
	return(dots_out_of_arena)

#general structure of algorithm (White Noise algo) 
#disply fixation cross
#for each trial : 
#display arena in grey
#create n random dots
# show dots
#during a certain time, make dots move : for each 'frame' displayed 
#split list in two according to desire motion coherence : one part with coherent motion dots CMD, other part with random mption dots RMD
#erase previous position of the dots
#make both part move either coherently according to the chosen direction of this trial (left vs right) for the CMD or randomly for RMD
#retrieve the dots that are now outside of the area and erase them
#make some dots spawn in the area to compensate
#repeat for each frame displayed

def display_random_dot_motion(motion_coherence,number_dots,time_duration=MAX_RESPONSE_DELAY): #test to display a single dot moving in a circular area
	movement = [0, 2]
	dot = stimuli.Circle(radius=RADIUS_OF_DOTS, colour=COLOR_OF_DOTS)
	stimuli.BlankScreen().present()
	arena=stimuli.Circle(radius=RADIUS_OF_ARENA+2*RADIUS_OF_DOTS,colour=COLOR_OF_ARENA)
	cue.present()
	exp.clock.wait(1000)
	exp.clock.reset_stopwatch()
	while exp.clock.stopwatch_time < time_duration:
		erase = stimuli.Circle(radius=RADIUS_OF_DOTS, position=dot.position, colour = COLOR_OF_ARENA)
		dot.move(movement)
		if distance_to_center(dot.position)>RADIUS_OF_ARENA : 
			movement[0],movement[1]=-movement[0],-movement[1]
		erase.present(clear=False, update=False) # present but do not refesh screen
		arena.present(clear=False,update=False)
		dot.present(clear=False, update=True)    # present but do not refesh screen
		exp.screen.update_stimuli([dot,erase])  # refesh screen
		exp.keyboard.check()    # ensure that keyboard input is proccesed # to quit experiment with ESC
		exp.clock.wait(1)



control.start()

display_random_dot_motion(50,1,time_duration=5000)

control.end()