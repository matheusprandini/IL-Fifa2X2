import numpy as np
import cv2
import time
from Agent import Agent
from Data import Data
from DAIL import DAIL
from Screen import Screen
from Keys import Keys

if __name__ == '__main__':
    
    agent = Agent('test')
    agent.load_move_model('Models/new_fifanet_normalized_dail_5_2x2_movement_actions.h5')
    agent.load_action_model('Models/new_fifanet_normalized_dail_5_2x2_control_actions.h5')
    agent.execute_agent()

    '''agent = Agent('test')
    agent.load_move_model('Models/fifanet_move_balanced_normalized_2x2_2ksamples.h5')
    agent.load_action_model('Models/fifanet_action_balanced_normalized_2x2_500samples.h5')
	
    data = Data('balanced_training_data_2x2_control_actions.npy')

    dail = DAIL(agent, 5, 1.9, data, "new_training_data_5%_dail_2x2_control_actions.npy")
    dail.execute_active_deep_imitation_learning_control_actions()'''