from expyriment import design, control, stimuli, misc
import random as r 
import numpy as np 
import math as m 

N_DOTS=10
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
MOVEMENT_TO_THE_LEFT=[-1,0]
MOVEMENT_TO_THE_RIGHT=[1,0]


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

def generate_random_dot_position_in_inner_square_of_arena() : 
	x=np.random.random()*WIDTH_INNER_SQUARE-(WIDTH_INNER_SQUARE/2)
	y=np.random.random()*WIDTH_INNER_SQUARE-(WIDTH_INNER_SQUARE/2)
	return(x,y)

def generate_list_of_n_positions_in_inner_square_of_arena(n_dots) : 
	return([generate_random_dot_position_in_inner_square_of_arena()  for k in range (n_dots)])

def generate_n_dots(n_dots):
	positions=generate_list_of_n_positions_in_inner_square_of_arena(n_dots)
	dot_list=[]
	for i in range (n_dots) :
		dot_list.append(stimuli.Circle(radius=RADIUS_OF_DOTS, colour=COLOR_OF_DOTS,position=positions[i]))
	return(dot_list)

def display_dots_in_dot_list(dot_list):
	for dot in dot_list : 
		dot.present(clear=False, update=False)

def create_erase_list_for_dot_list(dot_list) : 
	erase_list=[]
	for dot in dot_list : 
		erase_list.append(stimuli.Circle(radius=RADIUS_OF_DOTS, position=dot.position, colour = COLOR_OF_ARENA))
	return(erase_list)

def erase_previous_position_of_dots_with_erase_list(erase_list) : 
	for erase in erase_list : 
		erase.present(clear=False,update=False)

def generate_lists_coherent_motion_dots_and_random_motion_dots(motion_coherence,dot_list): 
	dot_belongs_to_coherent_list=np.random.binomial(1,motion_coherence/100,len(dot_list))
	coherent_dot_list=[]
	random_dot_list=[]
	for k in range (len(dot_list)) :
		if dot_belongs_to_coherent_list[k] :
			coherent_dot_list.append(dot_list[k])
		else : 
			random_dot_list.append(dot_list[k])
	return(coherent_dots,random_dots)

def coherent_movement(coherent_dot_list,direction) : 
	if direction=='left' :
		movement=MOVEMENT_TO_THE_LEFT
	elif direction=='right':
		movement=MOVEMENT_TO_THE_RIGHT
	for dot in coherent_dot_list :
		dot.move(movement)


def random_movement(random_dot_list) : 
	for dot in random_dot_list : 
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
	movement = [0, 0]
	dot_list = generate_n_dots(N_DOTS)	
	stimuli.BlankScreen().present()
	arena=stimuli.Circle(radius=RADIUS_OF_ARENA+2*RADIUS_OF_DOTS,colour=COLOR_OF_ARENA)
	cue.present()
	exp.clock.wait(1000)
	exp.clock.reset_stopwatch()
	while exp.clock.stopwatch_time < time_duration:
		erase_list=create_erase_list_for_dot_list(dot_list)
		for dot in dot_list :
			dot.move(movement)
			if distance_to_center(dot.position)>RADIUS_OF_ARENA : 
				movement[0],movement[1]=-movement[0],-movement[1]
		arena.present(clear=False,update=False)
		erase_previous_position_of_dots_with_erase_list(erase_list)
		display_dots_in_dot_list(dot_list)
		exp.screen.update()  # refesh screen
		exp.keyboard.check()    # ensure that keyboard input is proccesed # to quit experiment with ESC
		exp.clock.wait(1)


control.start()

display_random_dot_motion(50,1,time_duration=5000)

control.end()