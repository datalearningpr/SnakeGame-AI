
import pickle
import random
import numpy as np
from collections import deque
from keras.models import load_model, Sequential   
from keras.layers import Dense 
from keras.optimizers import Adam

# DQN object
class DQN():
    def __init__(self, s_size, a_size, e = 0.01, g = 0.9, memory_size = 1500, learning_rate = 0.001):
        self.s_size = s_size
        self.a_size = a_size
        self.e = e
        self.g = g
        self.memory = deque(maxlen = memory_size)
        self.learning_rate = learning_rate

        self.q_model = self._build_model()
        self.target_model = self._build_model()
        self.copy_weights()

    # the model is just a normal 2 layer FNN
    def _build_model(self):
        model = Sequential()
        model.add(Dense(25, input_dim = self.s_size, activation = 'relu'))
        model.add(Dense(25, activation = 'relu'))
        model.add(Dense(self.a_size, activation = 'linear'))
        model.compile(loss = "mean_squared_error", optimizer = Adam(lr = self.learning_rate))
        return model

    # after certain trainings, we copy the weights from q_model to target model
    # this is one of the tricks DQN uses to stablize the model training process
    def copy_weights(self):
        self.target_model.set_weights(self.q_model.get_weights())

    # store the training data to a memory with fixed size, so that old memory dies out
    # when training data, randomly get data from the memory
    # this is one of the tricks DQN uses to break the correlation between the training data 
    def store_train_data(self, old_state, old_action, reward, state, is_done):
        self.memory.append((old_state, old_action, reward, state, is_done))

    # method to train the model
    def train(self, batch_size):
        # randomly get batch size data from the memory
        minibatch = random.sample(self.memory, batch_size)
        # for DQN, use the target_model to get the action and the max Q
        for old_state, old_action, reward, state, is_done in minibatch:
            target = self.q_model.predict(old_state)
            if is_done:
                target[0][old_action] = reward
            else:
                a = self.target_model.predict(state)[0]
                t = self.target_model.predict(state)[0]
                target[0][old_action] = reward + self.g * t[np.argmax(a)]
            self.q_model.fit(old_state, target, epochs = 1, verbose = 0)

    # get action based on the max Q
    def get_action(self, state):
        if random.random() < self.e:
            return random.choice(range(self.a_size))
        act = self.q_model.predict(state)  
        return np.argmax(act[0])

    # save model
    def save_model(self):
        self.q_model.save('q_model.h5')

    # load model from archive
    def load_model(self):
        self.q_model = load_model('q_model.h5')
        self.target_model = load_model('q_model.h5')
