import gym
from gym import spaces
import numpy as np
import socket

class SBBenv(gym.Env):
    def __init__(self):
        super(SBBenv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(31)
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255, shape=
                        (40, 40, 3), dtype=np.uint8)

        SERVER = "127.0.0.1"
        PORT = 10012
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.client.sendall(bytes("RST",'UTF-8'))

    def _take_action(self,action):
        self.client.sendall(bytes("ACT " + action,'UTF-8'))
        data = self.client.recv(10000)
        data = data.decode()

        finaldata = data.split()
        obs = finaldata[1:]

        return reward, obs



    def step(self, action):
        # Execute one time step within the environment
        reward, obs = self._take_action(self,action)
        self.current_step += 1

        if reward < 0 :
            done = True
        else : 
            done = False

      
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.client.sendall(bytes("RST",'UTF-8'))
        data = self.client.recv(1024)

        data=data.decode()
        return self.start()

    def start(self):
        self.client.sendall(bytes("SRT",'UTF-8'))
        data = client.recv(10000)
        data = data.decode()

        finaldata = data.split()
        obs = finaldata[1:]

        return obs