import gym
from gym import spaces
import numpy as np
import socket
import time
import torch

def recv_until(sock: socket.socket, n: int):
    buffer = ""
    read = 0
    while read < n:
        income = sock.recv(n - read).decode()
        read += len(income)
        buffer += income
    return buffer

def send_until(sock: socket.socket, data: str):
    buffer = bytearray(data, 'utf-8')
    n = 0
    while n < len(buffer):
        sent = sock.send(buffer)
        buffer = buffer[sent:]
        n += sent

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
        send_until(self.client, 'RESET\n')
        if recv_until(self.client, 5) != "DONE\n":
            raise Exception('unity server error')

    def _take_action(self,action):
        actiontosend = action.item()
        send_until(self.client, 'ACTION ' + str(actiontosend) + '\n')
        #self.client.sendall(bytes("ACTION " + str(actiontosend),'UTF-8'))
        data = recv_until(self.client, 10)
        #data = data.decode()

        finaldata = data.split()
        reward = finaldata[0]

        return reward

    def _next_observation(self):
        send_until(self.client, 'SCREEN\n')

        data = recv_until(self.client, 19201)
        finaldata = data.split()
        obs = finaldata

        return obs

    def step(self, action):
        # Execute one time step within the environment
        reward = self._take_action(action)

        reward = float(reward)

        if reward < 0.0 :
            done = True
        else : 
            done = False

        obs = self._next_observation()

      
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        send_until(self.client, 'RESET\n')
        response = recv_until(self.client, 5)
        if response != "DONE\n":
            raise Exception('unity server error')
        return self._next_observation()