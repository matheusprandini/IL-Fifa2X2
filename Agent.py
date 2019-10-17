import numpy as np
import cv2
import time
from Screen import Screen
from Keys import Keys, W, A, S, D, L, K, P, SPACE
from keras.models import load_model

class Agent():

    def __init__(self, name):
        self.name = name
        self.keyboard = Keys()
        self.move_model = None
        self.action_model = None

    def right(self):
        self.keyboard.PressKey(D)
        self.keyboard.ReleaseKey(W)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(S)

    def left(self):
        self.keyboard.PressKey(A)
        self.keyboard.ReleaseKey(W)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(S)

    def up(self):
        self.keyboard.PressKey(W)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(S)

    def down(self):
        self.keyboard.PressKey(S)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(W)

    def shoot(self):
        self.keyboard.PressKey(SPACE)
        time.sleep(0.2)
        self.keyboard.ReleaseKey(SPACE)
        self.keyboard.ReleaseKey(L)
        self.keyboard.ReleaseKey(K)
        time.sleep(0.6)

    def defend(self):
        self.keyboard.PressKey(L)
        self.keyboard.ReleaseKey(SPACE)
        self.keyboard.ReleaseKey(K)

    def pass_ball(self):
        self.keyboard.PressKey(K)
        time.sleep(0.1)
        self.keyboard.ReleaseKey(K)
        self.keyboard.ReleaseKey(L)
        self.keyboard.ReleaseKey(SPACE)

    def release_moves(self):
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(S)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(W)

    def release_actions(self):
        self.keyboard.ReleaseKey(SPACE)
        self.keyboard.ReleaseKey(L)
        self.keyboard.ReleaseKey(K)
	
    def load_move_model(self, path_file):
        self.move_model = load_model(path_file)

    def load_action_model(self, path_file):
        self.action_model = load_model(path_file)
	
    def predict_move(self, image):
        return self.move_model.predict(image)

    def predict_action(self, image):
        return self.action_model.predict(image)

    def execute_movement_action(self, action):
        if action == 3:
            self.right()
        elif action == 2:
            self.down()
        elif action == 1:
            self.up()
        elif action == 0:
            self.left()

    def execute_control_action(self, action):
        if action == 3:
            self.shoot()
        elif action == 2:
            self.pass_ball()
        elif action == 1:
            self.defend()

    def execute_movement_action_with_threshold(self, actions_probabilities):
        movement_actions_rounded = np.round(actions_probabilities)
        action = np.argmax(movement_actions_rounded)

        self.execute_movement_action(action)

    def execute_control_action_with_threshold(self, actions_probabilities):
        control_actions_rounded = np.round(actions_probabilities)
        action = np.argmax(control_actions_rounded)

        self.execute_control_action(action)

    def execute_agent(self):
        
        keys = Keys()
        screen = Screen()

        print('Starting running Direct Imitation Learning in...')

        # Countdown to start running the agent  
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False

        while True:
        
            if not paused:
                img = screen.GrabScreenBGR()

                # Preprocessing input image
                converted_img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                resized_img = cv2.resize(converted_img, (120,90))
                reshaped_img = resized_img.reshape(-1,90,120,1)
                normalized_img = reshaped_img.astype('float32') / 255.0
                final_img = normalized_img
                
                # Prediction and Entropy of the Labels
                move_prediction = self.predict_move(final_img)
                action_prediction = self.predict_action(final_img)
                move_action = np.argmax(move_prediction[0])
                control_action = np.argmax(action_prediction[0])
                print(move_prediction[0], ' - ', action_prediction[0])
                
                # Move action
                self.execute_movement_action(move_action)
                #self.execute_movement_action_with_threshold(move_prediction[0])

                # Action action
                self.execute_control_action(control_action)
                #self.execute_control_action_with_threshold(action_prediction[0])
            
            keys_pressed = keys.KeyCheck()
            
            if 'Q' in keys_pressed:
                if paused:
                    paused = False
                    print('unpaused!')
                    time.sleep(1)
                else:
                    print('Pausing!')
                    self.release_moves()
                    paused = True
                    time.sleep(1)
		
if __name__ == '__main__':
    agent = Agent('test')
    agent.left()
    agent.right()
    agent.up()
    agent.down()