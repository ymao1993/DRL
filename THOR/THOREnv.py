import skimage
import numpy as np
import random
import robosims.server
import THORConfig as config
import cv2
from THORTarget import THORTargetManager
from THOROfflineEnv import EnvSim

class THOREnvironment:
    def __init__(self, feat_mode = False):
        self._env = EnvSim(feat_mode = feat_mode)
        self._done = True
        self._total_episode_reward = 0
        self._env_idx = None
        self._target_idx = None
        self._target_img = None
        self._target_img_pose = None
        self._target_img_mgr = THORTargetManager(config.target_images_folder)
        self._step_count = 0
        self._cur_frame = None

        # uncomment it if you what lazy initialization
        self._env.pre_load()

    def step(self, action_idx):
        assert(not self._done)
        observation, action_success = self._env.step(action_idx)
        self._step_count += 1
        if self._check_found_target(observation):
            self._done = True
            reward = 1
        else:
            reward = -1
        if self._step_count == config.episode_max_steps:
            self._done = True
        self._total_episode_reward += reward
        if config.display:
            self.render(observation, 'cur_frame')
        return observation, action_success, reward, self._done

    def reset(self, env_idx, target_idx):
        assert(self._done)
        assert(0 <= env_idx < len(config.supported_envs))
        assert(target_idx is not None)
        assert(0 <= target_idx < self.get_num_targets())
        self._env_idx = env_idx
        self._target_idx = target_idx
        env_name = config.supported_envs[self._env_idx]
        self._target_img = self._target_img_mgr.get_target_image(env_name, self._target_idx)
        self._target_img_pose = self._target_img_mgr.get_target_image_pose(env_name, self._target_idx)
        observation = self._env.reset(env_name)
        for _ in range(random.randrange(0, config.random_start + 1)):
            observation, _ = self._env.step(random.randrange(0, self.get_num_actions()))
        self._total_episode_reward = 0
        self._step_count = 0
        self._done = False
        if config.display:
            self.render(self._target_img, 'target')
            self.render(observation, 'cur_frame')
        return observation

    def render(self, frame, name):
        env_name = config.supported_envs[self._env_idx]
        cv2.imshow(name, frame)

    def reset_random(self):
        target_idx = random.randrange(0, self.get_num_targets())
        env_idx = random.randrange(0, len(config.supported_envs))
        return self.reset(env_idx, target_idx)

    def get_num_actions(self):
        return len(config.supported_actions)

    def get_num_targets(self):
        return config.targets_per_scene

    def get_env_name(self):
        return config.supported_envs[self._env_idx]

    def get_env_idx(self):
        assert(self._env_idx is not None)
        return self._env_idx

    def get_target_image(self):
        assert(self._target_img is not None)
        return self._target_img

    def episode_done(self):
        return self._done

    def get_total_episode_reward(self):
        return self._total_episode_reward

    def _check_found_target(self, observation):
        assert(self._target_img_pose is not None)        
        return self._target_img_pose == self._env.get_pose()


    

