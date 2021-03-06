import random
import math
#agent.py imports both classes from the environment module, class agent and class environment
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from math import sqrt

#polymorphism makes LearningAgent inherit everything agent has.  
class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=True, epsilon=1.0, alpha=0.5,decay_rate=.02):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        #get the turn number from the environment class and add 1 so we don't divide by 0
        self.trials = 0.0
 #       self.decay_rate=decay_rate
        

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        # the route_to function chooses a random intersection from environment's self.intersections
        self.planner.route_to(destination)
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        print self.trials
        self.trials += 1.0
        print self.trials
        if testing:
            self.epsilon=0
            self.alpha=0
        else:
            x=sqrt(self.trials)
            self.epsilon=1/pow(x,1.3)
 #           self.epsilon -= self.decay_rate
        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """
        
        # Collect data about the environment
        #the waypoint is the next point to go to.  it uses the next_waypoint function from the planner module to find the next move to make to reach the destination in the optimal way
        #we go to the planner app which uses variables from env to find right way to get to destination
        waypoint = self.planner.next_waypoint() # The next waypoint
        #the sense funciton from the environment class is called to get information about the environment or sensor inputs (the interseciton lights and traffic).  this helps us construct our current state
        #the sense function only uses functions and info from environment class
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        
        # NOTE : you are not allowed to engineer eatures outside of the inputs available.
        # Because the aim of this project is to teach Reinforcement Learning, we have placed 
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With the hand-engineered features, this learning process gets entirely negated.
        
        # Set 'state' as a tuple of relevant data for the agent
        #need to add input for light
        state = (waypoint, inputs['light'], inputs['oncoming'], inputs['left'])
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given stat

        maxQ = -100
        #cycle through each possible direction in valid_actions
        #if its greater than the current qvalue, set that to the max
        # ('None','forward','left','right'):
 #           qval = self.Q[state][ii]
#            if qval > maxQ:

        for ii in self.Q[state]:
            if maxQ < self.Q[state][ii]:
                maxQ = self.Q[state][ii]
        return maxQ
              


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        #state=(deadline,waypoint)
        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if self.learning:
            if state not in self.Q.keys():
     #           mydict={None:0, 'forward':0, 'left':0, 'right':0}
                self.Q[state] =self.Q.get(state, {None:0.0, 'forward':0.0, 'left':0.0, 'right':0.0})
        return
            
        

    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None


        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # Otherwise, choose an action with the highest Q-value for the current state
        # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        #we have an exploration vs exploitation trade off.  we want to explore random values instead of taking the highest q values everytime.  in the beginning we'll explore a bit.  epsilon is higher and when we pick a random number its likely we'll have a greater value for epsilon.  epsilon gets lower everytime though.  this makes us choose the highest q value instead.  this also decreases our chances of exploring randomly.

        if not self.learning:
            action = random.choice(self.valid_actions)
            
        else: #if self.learning
            if self.epsilon > random.random():
                action = random.choice(self.valid_actions)
                print self.Q[state]
            #this else statement occurs when epsilon is less and the probability is 1-epsilon
            else:
            #create an empty list of the valid actions.  all the maxQ's that tie are stored here so they can be picked randomly from.
            #we find the action in the state we're dealing with that corresponds with the maxQ, store it in the list, and choose the action
                valid_acts=[]
                print valid_acts
                maxQ = self.get_maxQ(state)
                for ii in self.Q[state]:
                    print self.Q[state]
                    if maxQ==self.Q[state][ii]:
                        valid_acts.append(ii)
                    print valid_acts,maxQ
                action=random.choice(valid_acts)
                #add it to choose a random one if they're the same
 
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        #we started with arbitrary utilities by initializing everything to 0.  We update it slowly with this learning rate
        if self.learning == True:
            currentQ = self.Q[state][action]
            self.Q[state][action] = reward*self.alpha + currentQ*(1-self.alpha)
        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        #get the surrounding traffic, waypoint, deadline, traffic lights information
        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        #learn it act may not need to do anything.  ask meaning if that first part of act
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent)
    
    ##############
    #this is in environment file
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run()


if __name__ == '__main__':
    run()
