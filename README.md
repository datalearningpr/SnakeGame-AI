# SnakeGame AI

Play snake game with different methods: search methods, neural network, reinforcement learning, deep learning etc.

Hope the work here (solving one game problem by using all different methods) can help with people who wants to learn about DL, RL etc. 


### Prerequisites

Pygame

## Summary

* BFS
	
	This method is moving the snake in each step by searching a path from snake head to apple using breadth first search method
    
* A*

	This method is moving the snake in each step by searching a path from snake head to apple using A* search method

* Qlearning

	This method is training the snake to play the game by using Qlearning method
    
* Sarsa

	This method is training the snake to play the game by using Sarsa method
    
* NN

	This method is to train the Q function by using a NN to map all the possible state, so that it can train faster than the Q learning and Sarsa method
    
* DQN

	This method is the combination of NN and Qlearning, using Qlearning method to train the NN so that the snake can play the game by trying like the basic Q learning method. But DQN can deal with huge state space which makes the training fast.
    
* DDQN

	This method is just an improvement of DQN with simple modification. It helps with the overestimate problem of DQN.

## License

GPL

## Acknowledgments

Many online Q learning and DQN materials are helping a lot with the study and work done here. 

