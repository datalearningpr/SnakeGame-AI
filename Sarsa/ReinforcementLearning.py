
import random
import numpy as np
import pickle

# RL object
class RL():
    def __init__(self, actions, e = 0.05, a = 0.8, g = 0.9):
        self.Q = {}

        self.A = actions
        self.e = e
        self.a = a
        self.g = g

    # method to return the Q based on (state, action)
    def getQ(self, state, action):
        # default 0
        return self.Q.get((state, action), 0.0)
    
    # set the Q
    def setQ(self, Q):
        self.Q = Q

    # load the Q from the txt
    def loadQ(self):
        self.Q =  pickle.load(open("Q.txt", "rb"))
    
    # save Q to the txt 
    def saveQ(self):
        f = open("Q.txt", "wb")
        pickle.dump(self.Q, f)
        f.close()
    
    # get the action based on the state
    def getA(self, state):
        if random.random() < self.e:
            result = random.choice(self.A)
        else:
            q_list = [self.getQ(state, a) for a in self.A]
            max_q = max(q_list)
            index = np.where(np.array(q_list) == max_q)
            result = self.A[random.choice(index[0])]
        return result

# extend the RL object to get the QLearning object
class QLearing(RL):
    # method to update Q for (state, action)
    # this is the only difference between Qlearning and SARSA
    # Qlearning is updating by choosing the action with biggest Q of the new_state
    def updateQ(self, state, action, new_state, reward):
        q = self.Q.get((state, action), None)
        if q is None:
            self.Q[(state, action)] = reward
        else:
            max_new_q = max([self.getQ(new_state, a) for a in self.A])
            self.Q[(state, action)] = q + self.a * (reward + self.g * max_new_q - q)

# extend the RL object to get the Sarsa object
class Sarsa(RL):   
    # method to update Q for (state, action)
    # this is the only difference between Qlearning and SARSA
    # Sarsa is updating by using the same action chosen by the getQ method
    def updateQ(self, state, action, new_state, new_action, reward):
        q = self.Q.get((state, action), None)
        if q is None:
            self.Q[(state, action)] = reward
        else:
            new_q = self.getQ(new_state, new_action)
            self.Q[(state, action)] = q + self.a * (reward + self.g * new_q - q)
