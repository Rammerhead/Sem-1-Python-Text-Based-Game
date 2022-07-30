#######################################################################
#######################################################################

#Init
import random
from tkinter import *
import tkinter.simpledialog


player_location = [1, 1]


#Game stuff

winloc = ((22,32), (23,32), (24,32), (25,32))
puzzling = False
health = 5
confused_statements = ("\"What are you saying?\"", "\"Excuse me, I did not get that.\"", "\"Can you please repeat what you just said?\"", "\"Huh? What? Please repeat.\"", "\"I'm sorry, what? Say again?\"", "\"I don't understand what you're saying.\"")
unconscious_statements = ("The man is either either dead or unconscious. But there appears to\nbe a note on him which says 'switch to next gate is at (5,25)'")
inventory = []
npcs = {(4,32):[f"There is a robot here, it doesn't look too\nsmart, nor harmful. Appears as if it's programmers\nweren't too smart either.", ("Interact", "Leave", "Attack"), [(3, 'Spacedollars')]]}
terminals = {(4,4):(0, [f"Welcome aboard the Spaceship Seacrossers! This terminal will give you information\nabout this spaceship and our current location in space!", f"We left Earth on year 2054, our journey to the planet Kepler 438b\nwas planned to every micrometer. However...", f"The ship's AI, MasterComputer Durandal calculated that we\ncannot make it all the way through, and so\nshould return to Earth at once.", f"The ship's Alpha officer, Commander Miguel, decided to ignore the AI's advice, and decided to go on\nwith the jouney.", f"This caused the ship's AI to take control of the ship,\nespecially considering protocol violations that the captain had\ncommmitted. The captain however, decided to bring some engineers\nto reprogram the AI and stop it from taking control.", f"But as the engineers tried to reprogram the\nAI, some problems occurred, and the AI took control\nover the entire ship. It made the smart\nrobots attack all humans, many of whom\nwere killed.", f"The commander decided to escape, and went into\nthe ship's cryobay chamber, to go\ninto cyrogenic sleep (Pods where humans can sleep for\nextended lengths of time, such as years)\n", f"Durandal has now decided to keep the spaceship in\na suspended state in space. I cannot stay here too long.\nI shall lock this room to prevent any dangerous robots\nfrom entering in. The switch to open the gate to this\nroom is located at (1,5)\n\nTerminal Logging End.\n-Echo Officer AR1337"]),
			(14,42):(1, [f"Alright, anyone reading this, please read carefully. The way to defeat\nDurandal... you have to deactivate his core by cracking his puzzles.", f"The two puzzles exist right in front of him. Check the map if\nneed any help. And listen carefully... DO NOT TRUST DURANDAL.\n He will try to trick you. You must get to the ship's\ncontrol room. Which can only be opened after Durandal is deactivated.", f"The puzzle woks like this. The machine will think of a word, and you'll\nhave to guess the word by guessing it's individual letters. You'll have 6\ntrials avaialable. Guessing the right letter will not consume your trials.\n", f"However, if you keep guessing wrong, and exhaust your trials, then you'll\nlose. Then you'll have to try again. So think smartly.", f"If anyone's reading this, then you are probably the only one who can\nget this spaceship back home. Best of luck. Meanwhile, I guess I'm living my last\nminutes. I'm starving, after all...\nTERMINAL LOG END\n- AR1337"]),
			(24,44):(2, [f"Oh hey there human, I see you. My name is Durandal and\nI am here to assist you. Go ahead, and you'll find a very convenient\nmetal bar.", "It's placed at the location (25,45).\nI need you to pick it up and use it. Trust me, for I was\nthe one who ran this ship and brought it this far. Our mission shall\nbe a success. Please remain calm and follow orders.\nTerminal Log End.\n-Durandal"])
			}



win = {1:False, 2:False}
puzzle_locations = {(22,44):1, (24,42):2}

terminal0_index = -1
terminal1_index = -1
terminal2_index = -1
#Creating the walls


wall = tuple(set(
	[(0,j) for j in range(10)] + [(j, 0) for j in range(10)]
	+ [(9,i) for i in range(10)] + [(i, 9) for i in range(10) if i !=3]
	+ [(1,i) for i in range(10,21)] + [(5,i) for i in range(10,21)]
	+ [(i,21) for i in range(1,9) if i!=3] 
	+ [(1,i) for i in range(21, 47)] + [(9,i) for i in range(21,47) if i!=41] #Room 1,2,3
	+ [(i,29) for i in range(1,9) if i!=4] #Gate3

	+ [(i,37) for i in range(1,9) if i!=4]		#Gate4
	+ [(i,47) for i in range(0,27)]
	
	+ [(9,i) for i in range(37,47) if i!=41]	#Gate5
	+ [(i,37) for i in range(9,44) if i!=23]
	+ [(18,i) for i in range(37,47) if i!=43]	#Gate6
	+ [(26,i) for i in range(37,47)]

	+ [(i,37) for i in range(18,27) if i!=23]	#Gate7

	+ [(21,i) for i in range(31,38)]
	+ [(25,i) for i in range(31,38)]
	+ [(i,31) for i in range(21,26)]
	))

treasure_grid = tuple(set(tuple((i,j) for i in range(1,9) for j in range(28,37))))
dollared = random.sample(treasure_grid, k=5)

#Switches and their respective gates
switch_gates = {(1,5):(3,9), (3,20):(3,21), (5,25):(4,29), (6,34):(4,37), (3,43):(9,41), (16,43):(18,43), 'AI':(23,27)}

#loot[(location)] [0:Display on entering location, 1:Stuff] [Stuff1]
loot_locations = {(3,22):[f"You have found the body of a man. This man\nis either dead or unconscious. He has\na note saying that the next switch\nis at (5,25). He also seems to have some health packs\nwhich can be used by typing 'health' in the input bar.", ("Scavenge", "Leave"), [(5, 'Health packs')]],

				(3,24):[f"You have found some space dollars\nYour current location is {player_location}\nand your health is {health}", ("Take", "Leave"), [(1,'Spacedollars')]],
				(3,25):[f"You have found some space dollars\nYour current location is {player_location}\nand your health is {health}", ("Take", "Leave"), [(1,'Spacedollars')]],
				(25,45):[f"You have found a strange iron bar with some buttons on it\nYour current location is {player_location}\nand your health is {health}", ("Pick up", "Leave"), [(1,'Iron Bar')]]
				
				}
maploc = (3,23)
for i in dollared:
	loot_locations[i] = [f"You have found some space dollars\nYour current location is {player_location}\nand your health is {health}", ("Take", "Leave"), [(1,'Spacedollars')]]


ground_items = {(3,10):'note'}
note_dict = {(3,10):"I do not know if anyone will ever read this,\nbut if you are reading this, then don't go ahead! Go from the left or right!\nThis place is filled with traps! I almost fell into one now...It seems\nlike the traps begin from [3,11] and end on [3,19] - AR1337 (Echo Officer)"
			}



traps = tuple((3,i) for i in range(11, 20))

root = Tk()
bg = PhotoImage(file = 'space1.png')
mapimage = PhotoImage(file = 'map.png')

label1 = Label(root, image=bg)
label1.place(x=0, y=0)
root.title("Seacrossers")

#Functions

def map_click():
	mapwindow = Toplevel()
	maplabel = Label(mapwindow, image=mapimage).pack()



def terminal_next(terminal_number):
	global terminal0_index
	global terminal1_index
	global terminal2_index
	if terminal_number == 0:
		if terminal0_index < len(terminals[tuple(player_location)][1]) -1:
			terminal0_index += 1
		else:
			terminal0_index = 0
		mainLabel['text'] = f"{terminals[tuple(player_location)][1][terminal0_index]}\n\nYour options are:\nnext\nleave"
	elif terminal_number == 1:
		if terminal1_index < len(terminals[tuple(player_location)][1]) -1:
			terminal1_index += 1
		else:
			terminal1_index = 0
		mainLabel['text'] = f"{terminals[tuple(player_location)][1][terminal1_index]}\n\nYour options are:\nnext\nleave"
	elif terminal_number == 2:
		if terminal2_index < len(terminals[tuple(player_location)][1]) -1:
			terminal2_index += 1
		else:
			terminal2_index = 0
		mainLabel['text'] = f"{terminals[tuple(player_location)][1][terminal2_index]}\n\nYour options are:\nnext\nleave"


def puzzle_AI(number):
	global health
	global puzzling
	global win1
	puzzling = True

	words = ['accepted', 'nebula', 'galaxy', 'milkyway',
	         'ruleset', 'programming', 'astronomy', 'satellite',
	         'directive', 'spaceship', 'violation', 'protocol',
	         ]

	# Function will choose one random
	# word from this list of words
	word = random.choice(words)

	cumulative_stuff = ''
	guesses = ''
	for char in word:
		if char in guesses:
			cumulative_stuff = cumulative_stuff + (char) + ' '

		else:
			cumulative_stuff = cumulative_stuff + ("_") + ' '

	mainLabel['text'] = f"Guess the characters\n{cumulative_stuff}"
	# any number of turns can be used here
	turns =6

	while turns > 0:

		guess = tkinter.simpledialog.askstring("Guess", "Guess a character:")
		guesses += guess

	    # counts the number of times a user fails
		failed = 0
		cumulative_stuff = ''
	    # all characters from the input
	    # word taking one at a time\
		for char in word:
			if char in guesses:
				cumulative_stuff = cumulative_stuff + (char) + ' '

			else:
				cumulative_stuff = cumulative_stuff + ("_") + ' '

				failed += 1
	         


		if failed == 0:
	        
			mainLabel['text'] = f"You win.\nThe word is: {word}"
			puzzling = False
			win[number] = True
			if win[1] == True and win[2] == True:
				del switch_gates['AI']
			del puzzle_locations[tuple(player_location)]
			terminals[((24,44),)] = (2, [f"SYSTEM MALFUNCTION! DURANDAL HAS CRASHED!"])
			break



		if guess not in word:

			turns -= 1
			cumulative_stuff += f"\nWrong.\nYou have {turns} more guesses\n" 
			if turns == 0:
				mainLabel['text'] = f"You lose. You feel a surge of electricity go through\nyour body as the machine gives you the electric shock.\nYou'll have to try again."
				health -= 1
				if health == 0:
					death('AI')
				puzzling = False


				break

		elif guess in word:
			cumulative_stuff += f"\nCorrect.\nYou have {turns} more guesses\n"

		mainLabel['text'] = f"{cumulative_stuff}"







def player_event():
	global health
	if tuple(player_location) in switch_gates.keys():
		mainLabel['text'] = (f"You have found a switch!\nType 'activate' to run the switch!\nYour location is {player_location}")
		button_enter['state'] = NORMAL
	elif tuple(player_location) in traps:
		health -= 1
		mainLabel['text'] = (f"You stumbled upon a trap, which took 1 hp.\nYour current health is {health}\nand your current location is {player_location}")
	elif tuple(player_location) in note_dict.keys():
		mainLabel['text'] = (f"You have found a torn note paper, that says \"{note_dict[tuple(player_location)]}\"\nYour current location is {player_location}")
	elif tuple(player_location) in loot_locations.keys():
		mainLabel['text'] = (f"{loot_locations[tuple(player_location)][0]}\nYour options are:\n{loot_locations[tuple(player_location)][1]}")
		button_enter['state'] = NORMAL
	elif tuple(player_location) in npcs.keys():
		mainLabel['text'] = (f"{npcs[tuple(player_location)][0]}\nYour options are:\n{npcs[tuple(player_location)][1]}")
	elif tuple(player_location) in terminals.keys():
		mainLabel['text'] = f"You have found a ship terminal. Would you like\nto access the information inside?\nYour current location is {player_location}, and health is {health}. Your options are:\n\nNext\nLeave"
	elif tuple(player_location) in puzzle_locations.keys():
		puzzle_AI(puzzle_locations[tuple(player_location)])
	elif tuple(player_location) in winloc:
		mainLabel['text'] = f"CONGRATULATIONS!\nYOU REACHED THE CONTROL SYSTEMS AND REVERTED\nCOURSE BACK TO EARTH!\nYour points:{inventory.count('Spacedollars')*10}"
		button_enter['state'] = DISABLED
		button_Up['state'] = DISABLED
		button_Left['state'] = DISABLED
		button_Right['state'] = DISABLED
		button_Down['state'] = DISABLED
	elif tuple(player_location) == maploc:
		mainLabel['text'] = f"You found a map!"
		button_map['state'] = NORMAL
		button_map['fg'] = 'red'
	if health == 0 :
		death('health')












def click_Up():
	global player_location
	if ((player_location[0], player_location[1] + 1) not in wall) and ((player_location[0], player_location[1] + 1) not in tuple(switch_gates.values())): 
		player_location[1] = player_location[1] + 1
		mainLabel['text'] = f""+str(player_location) + f" is your location and\nyour health is {health}"

	elif ((player_location[0], player_location[1] + 1) in wall):
		mainLabel['text'] = (f"You have hit a wall above.\nYour current location is  {player_location}\nand your health is {health}" )

	elif ((player_location[0], player_location[1] + 1) in tuple(switch_gates.values())):
		mainLabel['text'] = (f"You have hit a gate above.\nYour current location is  {player_location}\nand your health is {health}" )
	player_event()

def click_Left():
	global player_location
	if ((player_location[0] - 1, player_location[1]) not in wall) and ((player_location[0] - 1, player_location[1]) not in tuple(switch_gates.values())): 
		player_location[0] = player_location[0] - 1
		mainLabel['text'] = f""+str(player_location)+ f" is your location and\nyour health is {health}"

	elif ((player_location[0] - 1, player_location[1]) in wall):
		mainLabel['text'] = (f"You have hit a wall on the left.\nYour current location is  {player_location}\nand your health is {health}")

	elif ((player_location[0] - 1, player_location[1]) in tuple(switch_gates.values())):
		mainLabel['text'] = (f"You have hit a gate on the left.\nYour current location is  {player_location}\nand your health is {health}")
	player_event()

def click_Right():
	global player_location
	if ((player_location[0] + 1, player_location[1]) not in wall) and ((player_location[0] + 1, player_location[1]) not in tuple(switch_gates.values())): 
		player_location[0] = player_location[0] + 1
		mainLabel['text'] = f""+str(player_location) + f" is your location and\nyour health is {health}"

	elif ((player_location[0] + 1, player_location[1]) in wall):
		mainLabel['text'] = (f"You have hit a wall on the right.\nYour current location is  {player_location}\nand your health is {health}")

	elif ((player_location[0] + 1, player_location[1]) in tuple(switch_gates.values())):
		mainLabel['text'] = (f"You have hit a gate on the right.\nYour current location is  {player_location}\nand your health is {health}")
	player_event()

def click_Down():
	global player_location
	if ((player_location[0], player_location[1] - 1) not in wall) and ((player_location[0], player_location[1] - 1) not in tuple(switch_gates.values())): 
		player_location[1] = player_location[1] - 1
		mainLabel['text'] = f""+str(player_location) + f" is your location and\nyour health is {health}"

	elif ((player_location[0], player_location[1] - 1) in wall):
		mainLabel['text'] = (f"You have hit a wall below.\nYour current location is  {player_location}\nand your health is {health}")

	elif ((player_location[0], player_location[1] - 1) in tuple(switch_gates.values())):
		mainLabel['text'] = (f"You have hit a gate below.\nYour current location is  {player_location}\nand your health is {health}")
	player_event()










def click_Enter():
	global health
	global inventory
	player_entry_input = player_entry.get()
	if (player_entry_input.lower() == 'activate') and (tuple(player_location) in switch_gates.keys()):
		mainLabel['text'] = (f"The gate at {switch_gates[tuple(player_location)]} is now open")
		del switch_gates[tuple(player_location)]
	elif tuple(player_location) == (25, 45) and player_entry_input.lower() == 'pick up':
		death('bar')

	elif tuple(player_location) in loot_locations.keys():
		if player_entry_input.lower() == 'scavenge' or player_entry_input.lower() == 'take':
			if loot_locations[tuple(player_location)][2]:
				inventory.extend((loot_locations[tuple(player_location)][2][0][1]) for i in range (loot_locations[tuple(player_location)][2][0][0]))
				inventory.sort()
				inventory_display_variable = ''
				inventory_cumulative = ''

				for i in inventory:
					if i not in inventory_display_variable:	
						inventory_display_variable = str(inventory.count(i)) + ' - ' + i + '\n'
						inventory_cumulative = inventory_cumulative + inventory_display_variable

				inventory_widget['text'] = (f"{inventory_cumulative}")
				mainLabel['text'] = f"You found some items and stored them\nin your inventory."
				del loot_locations[tuple(player_location)]



		elif player_entry_input.lower() == 'leave':
				mainLabel['text'] = f"You decide to leave the place. Your location\nis {player_location} and health is {health}"





	elif player_entry_input.lower() == 'health':
		if 'Health packs' in inventory and health < 5:
			health += 1
			inventory.remove('Health packs')
			mainLabel['text'] = f"You used a health pack and recovered 1 hp.\nYour current location is {player_location}\nand your health is {health}"
			inventory_display_variable = ''
			inventory_cumulative = ''

			for i in inventory:
				if i not in inventory_display_variable:	
					inventory_display_variable = str(inventory.count(i)) + ' - ' + i + '\n'
					inventory_cumulative = inventory_cumulative + inventory_display_variable

			inventory_widget['text'] = (f"{inventory_cumulative}")
		elif health == 5:
			mainLabel['text'] = f"Your health is already max (5). Your\ncurrent location is {player_location}"




	elif tuple(player_location) in npcs.keys():
		if player_entry_input.lower() == 'attack':
			if health == 1:
				death('robot')
			else:
				health -= 1
				mainLabel['text'] = f"You managed to destroy the robot\nbut you lost some health. You gained\n{npcs[tuple(player_location)][2][0][0]} {npcs[tuple(player_location)][2][0][1]}"
				inventory.extend((npcs[tuple(player_location)][2][0][1]) for i in range (npcs[tuple(player_location)][2][0][0]))
				inventory.sort()
				inventory_display_variable = ''
				inventory_cumulative = ''

				for i in inventory:
					if i not in inventory_display_variable:	
						inventory_display_variable = str(inventory.count(i)) + ' - ' + i + '\n'
						inventory_cumulative = inventory_cumulative + inventory_display_variable
				inventory_widget['text'] = (f"{inventory_cumulative}")


		elif player_entry_input.lower() == 'interact':
			mainLabel['text'] = random.choice(confused_statements)


		elif player_entry_input.lower() == 'leave':
			mainLabel['text'] = f"You decide to leave the place. Your location\nis {player_location} and health is {health}"




	elif tuple(player_location) in terminals.keys():
		if player_entry_input.lower() == 'next':
			terminal_next(terminals[tuple(player_location)][0])

		elif player_entry_input.lower() == 'leave':
			mainLabel['text'] = f"You decide to leave the place. Your location\nis {player_location} and health is {health}"

	elif puzzling:
		return player_entry_input

	
	del player_entry_input
	player_entry.delete(0, END)









def death(cause):
	if cause == 'health' and tuple(player_location) in traps:
		happen = "You died by stumbling upon traps."
	elif cause == 'health':
		happen = "Your health drained out."
	elif cause == 'robot':
		happen = "Your health was too low to fight the robot."
	elif cause == 'AI':
		happen = "You feel a surge of electricity go through your body as the machine\ngives you the electric shock. However, your health was too low, this time."
	elif cause == 'bar':
		happen = "The bar starts glowing, as you feel paralyzed. You fall to the ground.\nThe bar then explodes."

	button_enter['state'] = DISABLED
	button_Up['state'] = DISABLED
	button_Left['state'] = DISABLED
	button_Right['state'] = DISABLED
	button_Down['state'] = DISABLED
	mainLabel['text'] = (f"{happen}\nYou died. Better luck next time!")





def exit():
	root.quit()

def credits_click():
	
	credits_screen = Toplevel()
	credits = Label(credits_screen, bg='gray', fg= 'cyan', font='Verdana', text=f"This game was created by Group 16, CSE Section A.\n\nAditya Rao\nAditya N\nAaryan Sharma").pack(pady=30)



#Frames, labels, and buttons (all widgets)
displayFrame = LabelFrame(root, bg='gray23', fg='white', text="Player Window", padx=300, pady=20)
mainLabel = Label(displayFrame, bg='gray30', fg='white', font="Verdana 13", text=(f"You wake up from the concussion. You don't know where you are, and the area is too dark.\nYou have a navigational instrument that tells you about your locataion.\nYou also have a written note saying 'Go to [4,4]'.\nYour current location is {player_location}"))


buttonFrame = Frame(root, bg='gray23', padx = 100)
button_Up = Button(buttonFrame, bg='slate gray', fg='white', text="Up", command=click_Up)
button_Left = Button(buttonFrame, bg='slate gray', fg='white', text="Left", command=click_Left)
button_Right = Button(buttonFrame, bg='slate gray', fg='white', text="Right", command=click_Right)
button_Down = Button(buttonFrame, bg='slate gray', fg='white', text="Down", command=click_Down)
button_enter = Button(buttonFrame, bg='slate gray', fg='cyan', text="Enter", command=click_Enter)



gameFrame = LabelFrame(root, bg='slate gray', fg='white', text = "Other options", padx=200)
button_exit = Button(gameFrame, text="Exit Game", command=exit)
button_credits = Button(gameFrame, text= "Credits", command=credits_click) 
button_map = Button(gameFrame, text='Map', state=DISABLED, command=map_click)
inventoryFrame = LabelFrame(root, bg ='PaleTurquoise4', fg='white', text='Inventory', padx=10, pady=10)
inventory_widget = Label(inventoryFrame, bg = 'PaleTurquoise4', fg='white', text=f"You currently have nothing")
frame2 = Frame(root, bg = 'LightCyan4')


player_entry = Entry(frame2, width=120)
entry_label = Label(frame2, text="Enter text:")

displayFrame.pack(pady=20, padx=30)
buttonFrame.pack(pady=10)
inventoryFrame.pack(pady=10)
frame2.pack(pady=10, padx=30)
gameFrame.pack(pady=20)


#Gridding the widgets

inventory_widget.pack()
mainLabel.grid(row=0, column=0)
button_exit.grid(row=0, column=0, pady=20, padx=30)
button_credits.grid(row=0, column=1, pady=20, padx=30)
button_map.grid(row=0, column=2, pady=20, padx=30)
button_Up.grid(row=1, column=1, pady=20)
button_Left.grid(row=2, column=0)
button_Right.grid(row=2, column=2)
button_Down.grid(row=3, column=1, pady=20)

button_enter.grid(row=2, column=1, padx=100)
entry_label.grid(row=0, column=0, padx=20)
player_entry.grid(row=0, column=1, padx=10, pady=30, columnspan=2)

root.mainloop()

