from expyriment import design, control, stimuli, misc
import random as r 
import numpy as np 
import math as m 

N_DOTS=25
LEFT_RESPONSE=misc.constants.K_LEFT
RIGHT_RESPONSE=misc.constants.K_RIGHT
MOTION_COHERENCE=np.tile(np.linspace(0,100,5),5)
N_TRIALS=len(MOTION_COHERENCE)
DIRECTION=['left' for k in range (int(N_TRIALS/2))]+['right' for k in range (int(N_TRIALS/2)+1)]
MAX_RESPONSE_DELAY=5000
COLOR_OF_ARENA=misc.constants.C_GREY
COLOR_OF_DOTS=misc.constants.C_WHITE
RADIUS_OF_ARENA=100
RADIUS_OF_DOTS=5
WIDTH_INNER_SQUARE=2*RADIUS_OF_ARENA/m.sqrt(2)
MOVEMENT_TO_THE_LEFT=[-2,0]
MOVEMENT_TO_THE_RIGHT=[2,0]

def expected_key_response(direction):
	if direction=='left':
		return(LEFT_RESPONSE)
	elif direction=='right':
		return(RIGHT_RESPONSE)

def generate_and_present_blankscreen():
	stimuli.BlankScreen().present()

def generate_cue():
	return (stimuli.FixCross(size=(50, 50), line_width=4))

def display_cue(cue):
	cue.present()

def generate_arena() : 
	return(stimuli.Circle(radius=RADIUS_OF_ARENA+2*RADIUS_OF_DOTS,colour=COLOR_OF_ARENA))

def display_arena(arena) : 
	arena.present(clear=False,update=False)

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

def list_of_indexes_of_dots_with_coherent_movement(motion_coherence,dot_list):
	total_number_dots=len(dot_list)
	number_dots_to_select= int(total_number_dots*motion_coherence/100)
	indexes_all_dots=[k for k in range (total_number_dots)]
	indexes_of_coherent_dots=np.random.choice(indexes_all_dots,number_dots_to_select)
	return(indexes_of_coherent_dots)

def move_one_coherent_dot(coherent_dot,direction) : 
	if direction=='left' :
		coherent_dot.move(MOVEMENT_TO_THE_LEFT)
	elif direction == 'right' :
		coherent_dot.move(MOVEMENT_TO_THE_RIGHT)

def move_one_random_dot(random_dot) : 
	movement=[np.random.random()*10-5,np.random.random()*10-5]
	random_dot.move(movement)

def update_all_dots_position(dot_list,indexes_of_coherent_dots,direction) : 
	n_dots=len(dot_list)
	for i in range (n_dots) :
		if i in indexes_of_coherent_dots : 
			move_one_coherent_dot(dot_list[i],direction)
		else : 
			move_one_random_dot(dot_list[i])

def dots_out_of_arena(dot_list) : 
	dots_out=[]
	for dot in dot_list : 
		if distance_to_center(dot.position)>RADIUS_OF_ARENA : 
			dots_out.append(dot)
	return(dots_out)

def relocate_dots_out_of_arena(dots_out):
	for dot in dots_out:
		new_position=generate_random_dot_position_in_inner_square_of_arena() 
		dot.reposition(new_position)

def execute_trial(motion_coherence,direction,number_dots,time_duration=MAX_RESPONSE_DELAY): 
	dot_list = generate_n_dots(N_DOTS)	
	generate_and_present_blankscreen()
	arena=generate_arena()
	cue=generate_cue()

	display_cue(cue)
	exp.clock.wait(1000)

	key=exp.keyboard.check()
	exp.clock.reset_stopwatch()
	while (exp.clock.stopwatch_time < time_duration) and (key is None):

		erase_list=create_erase_list_for_dot_list(dot_list)

		indexes_of_coherent_dots=list_of_indexes_of_dots_with_coherent_movement(motion_coherence,dot_list)
		update_all_dots_position(dot_list,indexes_of_coherent_dots,direction)

		display_arena(arena)
		erase_previous_position_of_dots_with_erase_list(erase_list)
		display_dots_in_dot_list(dot_list)

		dots_out=dots_out_of_arena(dot_list)
		relocate_dots_out_of_arena(dots_out)

		exp.screen.update()  # refresh screen
		key=exp.keyboard.check()
		time=exp.clock.stopwatch_time    # ensure that keyboard input is proccesed # to quit experiment with ESC
		exp.clock.wait(1)
	return(key,time)

def randomize_trials():
	np.random.shuffle(MOTION_COHERENCE)
	np.random.shuffle(DIRECTION)




exp = design.Experiment(name="Random Dot Motion Task")
control.initialize(exp)

instructions = stimuli.TextScreen("Instructions",
    f"""You are going to see small white dots moving in a grey circle on the screen.

    Your task is to decide, as quickly as possible, if the dots are moving to the left or to the right.

    If you think that they are moving to the left, press the left arrow key. If you think that they are moving to  the right, press the right arrow key.

    There will be {N_TRIALS} trials in total.

    Press the space bar to start.""")


randomize_trials()
exp.add_data_variable_names(['trial', 'motion_coherence','expected_resp', 'respkey', 'RT'])


control.start()
instructions.present()
exp.keyboard.wait()

for i_trial in range (N_TRIALS):
	motion_coherence=MOTION_COHERENCE[i_trial]
	direction=DIRECTION[i_trial]
	key,rt=execute_trial(motion_coherence,direction,N_DOTS)
	exp.data.add([i_trial, motion_coherence, expected_key_response(direction), key, rt])


control.end()