"""
This script provdies an example of an agent that can be controled by human player by typing command
"""

import THORConfig as config
from THOREnv import THOREnvironment
import random
import skimage.io
import cv2

commands = {'w':'MoveAhead', 's':'MoveBack', 'a':'MoveLeft', 'd':'MoveRight',
			'j':'RotateLeft','l':'RotateRight', 'i':'LookUp', 'k':'LookDown'}

thor_env = THOREnvironment()

num_actions = thor_env.get_num_actions()
num_targets = thor_env.get_num_targets()

print('number of actions: ' + str(num_actions))
print('number of targets: ' + str(num_targets))

thor_env.reset_random()

print('cur_env_idx: ' + str(thor_env.get_env_idx()))
print('cur_env_name: ' + thor_env.get_env_name())

current_target = thor_env.get_target_image()
skimage.io.imsave('target.png', current_target)
while True:
	command_chr = chr(cv2.waitKey())
	if command_chr not in commands:
		continue
	action_name = commands[command_chr]
	if action_name not in config.supported_actions:
		print('{0} is not supported.'.format(action_name))
	action_idx = config.supported_actions_idx[action_name]
	observation, action_success, reward, done = thor_env.step(action_idx)
	if reward > 0:
		print('found !')
		assert(done)
	if done:
		break
print('total_episode_reward: ' + str(thor_env.get_total_episode_reward()))

