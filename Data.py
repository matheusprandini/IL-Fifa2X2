import numpy as np
import pandas as pd
import cv2
import time
import os
from Screen import Screen
from Keys import Keys
from collections import Counter
from random import shuffle

class Data():

    def __init__(self, file_name='training_data.npy'):
        self.file_name = file_name
        self.path_file = 'Data/' + file_name
        self.training_data = self.InitializeTrainingData()        

	# Load training data if exists, else return an empty list
    def InitializeTrainingData(self):
        if os.path.isfile(self.path_file):
            print('File exists, loading previous data!')
            return list(np.load(self.path_file))
        print('File does not exist, creating file!')
        return []
	
	# Show all data in training data (image, output_move, output_action)
    def validate_data(self):
        for data in self.training_data:
            img = data[0]
            output_move = data[1]
            cv2.imshow('test', img)
            print(output_move)
            if cv2.waitKey(25) & 0xFF == ord('q'): # Destroy all images when close the script
                cv2.destroyAllWindows()
                break

    # Merge data of two numpy files
    def merge_data(self, file1, file2):
        data_file1 = list(np.load('Data/' + file1))
        data_file2 = list(np.load('Data/' + file2))

        total_data = data_file1 + data_file2

        np.save(self.path_file,total_data)

        print("Number of examples: ", len(total_data))

    def save_data(self):
        np.save(self.path_file,self.training_data)
        print('File saved!')

	# Create training data
    def CreateTrainingData(self):
        keys = Keys()
        screen = Screen()
        print('Starting Training in...')

		# Countdown to start the training
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False
        last_time = time.time()
		
        while True:
	
            if not paused:
                grabbed_screen = screen.GrabScreenBGR() # Get actual frame
                new_screen = cv2.resize(cv2.cvtColor(grabbed_screen, cv2.COLOR_BGR2GRAY), (120,90)) # Converted and Resized frame
                #normalized_screen = new_screen.astype('float32') / 255 # Normalizing
                keys_pressed = keys.KeyCheck() # Check for pressed keys
                output_move = keys.KeysMovementOutput(keys_pressed) # Verifies if one move key was pressed
                output_action = keys.KeysActionOutput(keys_pressed) # Verifies if one action key was pressed
                self.training_data.append([new_screen, output_move, output_action]) # Create an instance of training data
            
            if len(self.training_data) % 1000 == 0:
                print(len(self.training_data))
                
            keys_pressed = keys.KeyCheck()
			
			# Pausing or Unpausing training
            if 'Q' in keys_pressed:
                if paused:
                    paused = False
                    print('Unpausing training...')
                    time.sleep(2)
                else:
                    print('Pausing training!')
                    paused = True
                    time.sleep(1)
			
			# Saving Data
            if 'P' in keys_pressed:
                np.save(self.path_file,self.training_data)

    def BalanceMovementData(self):
        train_data = np.load(self.path_file)
		
		# Convert numpy 'train_data' array to a pandas Dataframe
        df = pd.DataFrame(train_data)

		# Initialize examples
        lefts = []
        rights = []
        forwards = []
        backwards = []
        no_moves = []

		# Randomize instances positions
        shuffle(train_data)

        for data in train_data:
            img = data[0]
            choice_move = data[1]

            ## Complete Movement examples
            if choice_move == [1,0,0,0]:
                lefts.append([img,choice_move])
            elif choice_move == [0,1,0,0]:
                forwards.append([img,choice_move])
            elif choice_move == [0,0,1,0]:
                backwards.append([img,choice_move])
            elif choice_move == [0,0,0,1]:
                rights.append([img,choice_move])
            elif choice_move == [0,0,0,0]:
                no_moves.append([img,choice_move])
            else:
                print('No matches corresponding to a movement')

        print('Dataset before balancing: ')
        print(len(forwards))
        print(len(lefts))
        print(len(rights))
        print(len(backwards))

		# Balancing movement data examples
        forwards = forwards[:len(lefts)][:len(rights)][:len(backwards)]
        lefts = lefts[:len(forwards)]
        rights = rights[:len(forwards)]
        backwards = backwards[:len(forwards)]

        final_data = forwards + backwards + lefts + rights
        shuffle(final_data)

        print('\nDataset after balancing: ')
        print(len(forwards))
        print(len(lefts))
        print(len(rights))
        print(len(backwards))

        print(len(final_data))
		
		# Saving balancing data
        np.save('Data/balanced_training_data_drible_4games.npy', final_data)

    def BalanceActionData(self):
        train_data = np.load(self.path_file)
		
		# Convert numpy 'train_data' array to a pandas Dataframe
        df = pd.DataFrame(train_data)

		# Initialize examples
        no_actions = []
        defends = []
        passes = []
        shoots = []

		# Randomize instances positions
        shuffle(train_data)

        for data in train_data:
            img = data[0]
            choice_action = data[2]

            ## Complete Action examples
            if choice_action == [1,0,0,0]:
                no_actions.append([img,choice_action])
            elif choice_action == [0,1,0,0]:
                defends.append([img,choice_action])
            elif choice_action == [0,0,1,0]:
                passes.append([img,choice_action])
            elif choice_action == [0,0,0,1]:
                shoots.append([img,choice_action])
            else:
                print('No matches corresponding to a movement')

        print('Dataset before balancing: ')
        print(len(no_actions))
        print(len(defends))
        print(len(passes))
        print(len(shoots))

		# Balancing movement data examples
        no_actions = no_actions[:len(defends)][:len(passes)][:len(shoots)]
        defends = defends[:len(no_actions)]
        passes = passes[:len(no_actions)]
        shoots = shoots[:len(no_actions)]

        final_data = no_actions + defends + passes + shoots
        shuffle(final_data)

        print('\nDataset after balancing: ')
        print(len(no_actions))
        print(len(defends))
        print(len(passes))
        print(len(shoots))

        print(len(final_data))
		
		# Saving balancing data
        np.save('Data/balanced_action_training_data_2x2_4.npy', final_data)

if __name__ == '__main__':
    data = Data('new_training_data_5%_dail_2x2_control_actions.npy')
    #data.CreateTrainingData()
    #data.BalanceMovementData()
    #data.BalanceActionData()
    data.merge_data('balanced_training_data_2x2_control_actions.npy', 'new_training_data_5%_dail_2x2_control_actions.npy')