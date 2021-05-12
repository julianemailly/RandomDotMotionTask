'''
Running this code will display a Random Dot Motion task with expyriment. The stimuli are created thanks to the White Noise algorithm. 
Each trial is charaterised by the motion coherence of the dots and the direction of the movement is chosen randomly before each trial.
The default parameters of this experiments (motion coherence: 0%, 1%, 2%, 3%, 5%, 8%, 10%, 20%, 30%, 50%, 100%, each repeated 15 times) give a good psychometric function when analysed with analysis.py.
'''


from expyriment import design, control, stimuli, misc 
import numpy as np 

N_DOTS=30
MOTION_COHERENCE=np.tile([0,1,2,3,5,8,10,20,30,50,100],15)
N_TRIALS=len(MOTION_COHERENCE)

LEFT_RESPONSE=misc.constants.K_LEFT
RIGHT_RESPONSE=misc.constants.K_RIGHT
MAX_RESPONSE_DELAY=5000

COLOR_OF_ARENA=misc.constants.C_GREY
COLOR_OF_DOTS=misc.constants.C_WHITE

RADIUS_OF_ARENA=100
RADIUS_OF_DOTS=5
WIDTH_INNER_SQUARE=2*RADIUS_OF_ARENA/np.sqrt(2)

MOVEMENT_TO_THE_LEFT=[-2,0]
MOVEMENT_TO_THE_RIGHT=[2,0]

AMPLITUDE_RANDOM_MOVEMENT=10
MEAN_RANDOM_MOVEMENT=5

SIZE_FIXATION_CROSS=50
LINE_WIDTH_FIXATION_CROSS=4

def expected_key_response(direction):
	if direction=='left':
		return(LEFT_RESPONSE)
	elif direction=='right':
		return(RIGHT_RESPONSE)

def distance_to_center(point):
	x,y=point[0],point[1]
	return(np.sqrt(x**2+y**2))

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
	movement=[np.random.random()*AMPLITUDE_RANDOM_MOVEMENT-MEAN_RANDOM_MOVEMENT,np.random.random()*AMPLITUDE_RANDOM_MOVEMENT-MEAN_RANDOM_MOVEMENT]
	random_dot.move(movement)

def update_all_dots_positions(dot_list,indexes_of_coherent_dots,direction) : 
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

def update_stimulus(dot_list,arena):
	erase_list=create_erase_list_for_dot_list(dot_list)

	indexes_of_coherent_dots=list_of_indexes_of_dots_with_coherent_movement(motion_coherence,dot_list)
	update_all_dots_positions(dot_list,indexes_of_coherent_dots,direction)
	arena.present(clear=False,update=False)
	erase_previous_position_of_dots_with_erase_list(erase_list)
	display_dots_in_dot_list(dot_list)

	dots_out=dots_out_of_arena(dot_list)
	relocate_dots_out_of_arena(dots_out)
	exp.screen.update()

def check_keyboard_response_and_time():
	key=exp.keyboard.check()
	time=exp.clock.stopwatch_time 
	return(key,time) 

def execute_trial(motion_coherence,direction,number_dots,time_duration=MAX_RESPONSE_DELAY): 
	dot_list = generate_n_dots(N_DOTS)	
	stimuli.BlankScreen().present()
	arena=stimuli.Circle(radius=RADIUS_OF_ARENA+2*RADIUS_OF_DOTS,colour=COLOR_OF_ARENA)
	cue=stimuli.FixCross(size=(SIZE_FIXATION_CROSS, SIZE_FIXATION_CROSS), line_width=LINE_WIDTH_FIXATION_CROSS)

	cue.present()
	exp.clock.wait(1000)

	key=exp.keyboard.check()
	exp.clock.reset_stopwatch()

	while (exp.clock.stopwatch_time < time_duration) and (key is None):

		update_stimulus(dot_list,arena)
		key,time=check_keyboard_response_and_time() 
		exp.clock.wait(1)

	return(key,time)

def randomize_trials():
	np.random.shuffle(MOTION_COHERENCE)

def choose_random_direction():
	return(np.random.choice(['left','right'],1)[0])


exp = design.Experiment(name="Random Dot Motion Task")
control.initialize(exp)

INSTRUCTIONS = stimuli.TextScreen("Instructions",
    f"""You are going to see small white dots moving in a grey circle on the screen.

    Your task is to decide, as quickly as possible, if the dots are moving to the left or to the right.

    If you think that they are moving to the left, press the left arrow key. If you think that they are moving to  the right, press the right arrow key.

    There will be {N_TRIALS} trials in total.

    Press the space bar to start.""")


randomize_trials()
exp.add_data_variable_names(['trial', 'motion_coherence','expected_resp', 'respkey', 'RT'])


control.start()
INSTRUCTIONS.present()
exp.keyboard.wait()

for i_trial in range (N_TRIALS):
	motion_coherence=MOTION_COHERENCE[i_trial]
	direction=choose_random_direction()
	key,rt=execute_trial(motion_coherence,direction,N_DOTS)
	exp.data.add([i_trial, motion_coherence, expected_key_response(direction), key, rt])


control.end()