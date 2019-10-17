import cv2
import numpy as np
import scipy.stats
import time
from Data import Data
from math import log, e
from Keys import Keys
from Screen import Screen
import winsound

# Deep Active Imitation Learning Class
class DAIL():

    ## Behavioral Agent: agent trained with behavioral cloning on the specified Dataset
    ## Active Sample Size: size (in percentage) of active samples of training data
    ## Dataset Behavioral Cloning: data used to train the behavioral agent
    def __init__(self, behavioral_agent, active_sample_size, threshold, dataset_behavioral_cloning, new_data_name):
        self.behavioral_agent = behavioral_agent
        self.active_sample_size = active_sample_size
        self.threshold = threshold
        self.dataset_behavioral_cloning = dataset_behavioral_cloning
        self.active_samples = Data(new_data_name)

    def query_sound(self):
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)

    def calculate_entropy(self, labels):
        """ Computes entropy of label distribution. """

        entropy = scipy.stats.entropy(labels,base=2)  # input probabilities to get the entropy 
        return entropy

    def execute_active_deep_imitation_learning_movement_actions(self):
        
        keys = Keys()
        screen = Screen()

        print('Starting running Active Deep Imitation Learning in...')

        # Countdown to start running the agent  
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False

        number_active_samples_to_reach = self.active_sample_size * len(self.dataset_behavioral_cloning.training_data) / 100.0

        print(len(self.active_samples.training_data))
        print(number_active_samples_to_reach)

        while len(self.active_samples.training_data) < number_active_samples_to_reach:
        
            if not paused:
                img = screen.GrabScreenBGR()

                # Preprocessing input image
                converted_img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                resized_img = cv2.resize(converted_img, (120,90))
                reshaped_img = resized_img.reshape(-1,90,120,1)
                normalized_img = reshaped_img.astype('float32') / 255
                final_img = normalized_img
                
                # Prediction and Entropy of the Labels
                move_prediction = self.behavioral_agent.predict_move(final_img)
                action_prediction = self.behavioral_agent.predict_action(final_img)
                move = np.argmax(move_prediction[0])
                action = np.argmax(action_prediction[0])
                entropy = self.calculate_entropy(action_prediction[0])
                print(move_prediction[0], ' -> ', entropy)

                if entropy < self.threshold:
                    ## Execute the behavioral agent's action
                
                    # Move action
                    self.behavioral_agent.execute_movement_action(move)
                    
                    # Control action
                    self.behavioral_agent.execute_control_action(action)

                else:
                    ## Queries a non-expert action
                    self.query_sound()

                    print('Query non-expert action: ')
                    self.behavioral_agent.release_moves()

                    # Waiting for a non-expert action
                    while True:
                        keys_pressed = keys.KeyCheck() # Check for pressed keys
                        non_expert_move = keys.KeysMovementOutput(keys_pressed) # Verifies if one move key was pressed
                        if non_expert_move != [0, 0, 0, 0]:
                            print(non_expert_move)
                            self.active_samples.training_data.append([resized_img, non_expert_move])
                            break
            
            keys_pressed = keys.KeyCheck()
            
            if 'Q' in keys_pressed:
                if paused:
                    paused = False
                    print('unpaused!')
                    time.sleep(1)
                else:
                    print('Pausing!')
                    self.behavioral_agent.release_moves()
                    paused = True
                    time.sleep(1)
        
        self.active_samples.save_data()

    def execute_active_deep_imitation_learning_control_actions(self):
        
        keys = Keys()
        screen = Screen()

        print('Starting running Active Deep Imitation Learning in...')

        # Countdown to start running the agent  
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False

        number_active_samples_to_reach = self.active_sample_size * len(self.dataset_behavioral_cloning.training_data) / 100.0

        while len(self.active_samples.training_data) < number_active_samples_to_reach:
        
            if not paused:
                img = screen.GrabScreenBGR()

                # Preprocessing input image
                converted_img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                resized_img = cv2.resize(converted_img, (120,90))
                reshaped_img = resized_img.reshape(-1,90,120,1)
                normalized_img = reshaped_img.astype('float32') / 255
                final_img = normalized_img
                
                # Prediction and Entropy of the Labels
                move_prediction = self.behavioral_agent.predict_move(final_img)
                action_prediction = self.behavioral_agent.predict_action(final_img)
                move = np.argmax(move_prediction[0])
                action = np.argmax(action_prediction[0])
                entropy = self.calculate_entropy(action_prediction[0])
                print(action_prediction[0], ' -> ', entropy)

                if entropy < self.threshold:
                    ## Execute the behavioral agent's action
                
                    # Move action
                    self.behavioral_agent.execute_movement_action(move)
                    
                    # Control action
                    self.behavioral_agent.execute_control_action(action)

                else:
                    ## Queries a non-expert action
                    self.query_sound()

                    print('Query non-expert action: ')
                    self.behavioral_agent.release_actions()

                    # Waiting for a non-expert action
                    while True:
                        keys_pressed = keys.KeyCheck() # Check for pressed keys
                        non_expert_move = keys.KeysActionOutputDAIL(keys_pressed) # Verifies if one move key was pressed
                        if non_expert_move != [0, 0, 0, 0]:
                            print(non_expert_move)
                            self.active_samples.training_data.append([resized_img, non_expert_move])
                            break
            
            keys_pressed = keys.KeyCheck()
            
            if 'Q' in keys_pressed:
                if paused:
                    paused = False
                    print('unpaused!')
                    time.sleep(1)
                else:
                    print('Pausing!')
                    self.behavioral_agent.release_moves()
                    paused = True
                    time.sleep(1)
        
        self.active_samples.save_data()