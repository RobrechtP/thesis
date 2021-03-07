import numpy as np


class Simulation:
    def __init__(self, filename):
        """
        Parses .pomdp file and loads info into this object's fields.

        Attributes:
            discount
            values
            states
            actions
            observations
            T (action, curr_state, next_state)
            Z (action, new_state, observation)
            R (action, start_state, new_state, obs)
        """
        f = open(filename, 'r')
        self.contents = [
            x.strip() for x in f.readlines()
            if (not (x.startswith("#") or x.isspace()))
        ]

        # set up transition function T, observation function Z, and
        # reward R, step number and accumulated reward
        self.T = {}
        self.Z = {}
        self.R = {}
        self.step_am = 0
        self.reward = 0

        # go through line by line
        i = 0
        while i < len(self.contents):
            line = self.contents[i]
            if line.startswith('discount'):
                i = self.__get_discount(i)
            elif line.startswith('values'):
                i = self.__get_value(i)
            elif line.startswith('states'):
                i = self.__get_states(i)
            elif line.startswith('actions'):
                i = self.__get_actions(i)
            elif line.startswith('observations'):
                i = self.__get_observations(i)
            elif line.startswith('T'):
                i = self.__get_transition(i)
            elif line.startswith('O'):
                i = self.__get_observation(i)
            elif line.startswith('R'):
                i = self.__get_reward(i)
            elif line.startswith('start'):
                i = self.__get_state(i)
            else:
                print("Unrecognized line: " + line)
                i+=1

        # cleanup
        f.close()

    def __get_state(self,i):
        line = self.contents[i+1]
        probs = [float(x) for x in line.split()]
        self.state = np.random.choice(len(probs), 1, p=probs)[0]
        return i + 2


        return i

    def __get_discount(self, i):
        line = self.contents[i]
        self.discount = float(line.split()[1])
        return i + 1

    def __get_value(self, i):
        # Currently just supports "values: reward". I.e. currently
        # meaningless.
        line = self.contents[i]
        self.values = line.split()[1]
        return i + 1

    def __get_states(self, i):
        line = self.contents[i]
        self.states = line.split()[1:]
        if is_numeric(self.states):
            no_states = int(self.states[0])
            self.states = [str(x) for x in range(no_states)]
        return i + 1

    def __get_actions(self, i):
        line = self.contents[i]
        self.actions = line.split()[1:]
        if is_numeric(self.actions):
            no_actions = int(self.actions[0])
            self.actions = [str(x) for x in range(no_actions)]
        return i + 1

    def __get_observations(self, i):
        line = self.contents[i]
        self.observations = line.split()[1:]
        if is_numeric(self.observations):
            no_observations = int(self.observations[0])
            self.observations = [str(x) for x in range(no_observations)]
        return i + 1

    def __get_transition(self, i):
        line = self.contents[i]
        pieces = [x for x in line.split() if (x.find(':') == -1)]
        action = self.actions.index(pieces[0])

        if len(pieces) == 4:
            # case 1: T: <action> : <start-state> : <next-state> %f
            start_state = self.states.index(pieces[1])
            next_state = self.states.index(pieces[2])
            prob = float(pieces[3])
            self.T[(action, start_state, next_state)] = prob
            return i + 1
        elif len(pieces) == 3:
            # case 2: T: <action> : <start-state> : <next-state>
            # %f
            start_state = self.states.index(pieces[1])
            next_state = self.states.index(pieces[2])
            next_line = self.contents[i+1]
            prob = float(next_line)
            self.T[(action, start_state, next_state)] = prob
            return i + 2
        elif len(pieces) == 2:
            # case 3: T: <action> : <start-state>
            # %f %f ... %f
            start_state = self.states.index(pieces[1])
            next_line = self.contents[i+1]
            probs = next_line.split()
            assert len(probs) == len(self.states)
            for j in range(len(probs)):
                prob = float(probs[j])
                self.T[(action, start_state, j)] = prob
            return i + 2
        elif len(pieces) == 1:
            next_line = self.contents[i+1]
            if next_line == "identity":
                # case 4: T: <action>
                # identity
                for j in range(len(self.states)):
                    for k in range(len(self.states)):
                        prob = 1.0 if j == k else 0.0
                        self.T[(action, j, k)] = prob
                return i + 2
            elif next_line == "uniform":
                # case 5: T: <action>
                # uniform
                prob = 1.0 / float(len(self.states))
                for j in range(len(self.states)):
                    for k in range(len(self.states)):
                        self.T[(action, j, k)] = prob
                return i + 2
            else:
                # case 6: T: <action>
                # %f %f ... %f
                # %f %f ... %f
                # ...
                # %f %f ... %f
                for j in range(len(self.states)):
                    probs = next_line.split()
                    assert len(probs) == len(self.states)
                    for k in range(len(probs)):
                        prob = float(probs[k])
                        self.T[(action, j, k)] = prob
                    next_line = self.contents[i+2+j]
                return i + 1 + len(self.states)
        else:
            raise Exception("Cannot parse line " + line)

    def __get_observation(self, i):
        line = self.contents[i]
        pieces = [x for x in line.split() if (x.find(':') == -1)]
        if pieces[0] == "*":
            # Case when action does not affect observation
            action = None
        else:
            action = self.actions.index(pieces[0])

        if len(pieces) == 4:
            # case 1: O: <action> : <next-state> : <obs> %f
            next_state = self.states.index(pieces[1])
            obs = self.observations.index(pieces[2])
            prob = float(pieces[3])
            self.Z[(action, next_state, obs)] = prob
            return i + 1
        elif len(pieces) == 3:
            # case 2: O: <action> : <next-state> : <obs>
            # %f
            next_state = self.states.index(pieces[1])
            obs = self.observations.index(pieces[2])
            next_line = self.contents[i+1]
            prob = float(next_line)
            self.Z[(action, next_state, obs)] = prob
            return i + 2
        elif len(pieces) == 2:
            # case 3: O: <action> : <next-state>
            # %f %f ... %f
            next_state = self.states.index(pieces[1])
            next_line = self.contents[i+1]
            probs = next_line.split()
            assert len(probs) == len(self.observations)
            for j in range(len(probs)):
                prob = float(probs[j])
                self.Z[(action, next_state, j)] = prob
            return i + 2
        elif len(pieces) == 1:
            next_line = self.contents[i+1]
            if next_line == "identity":
                # case 4: O: <action>
                # identity
                for j in range(len(self.states)):
                    for k in range(len(self.observations)):
                        prob = 1.0 if j == k else 0.0
                        self.Z[(action, j, k)] = prob
                return i + 2
            elif next_line == "uniform":
                # case 5: O: <action>
                # uniform
                prob = 1.0 / float(len(self.observations))
                for j in range(len(self.states)):
                    for k in range(len(self.observations)):
                        self.Z[(action, j, k)] = prob
                return i + 2
            else:
                # case 6: O: <action>
                # %f %f ... %f
                # %f %f ... %f
                # ...
                # %f %f ... %f
                for j in range(len(self.states)):
                    probs = next_line.split()
                    assert len(probs) == len(self.observations)
                    for k in range(len(probs)):
                        prob = float(probs[k])
                        self.Z[(action, j, k)] = prob
                    next_line = self.contents[i+2+j]
                return i + 1 + len(self.states)
        else:
            raise Exception("Cannot parse line: " + line)

    def __get_reward(self, i):
        """
        Wild card * are allowed when specifying a single reward
        probability. They are not allowed when specifying a vector or
        matrix of probabilities.
        """
        line = self.contents[i]
        pieces = [x for x in line.split() if (x.find(':') == -1)]
        if pieces[0] == "*":
            action = None
        else:
            action = self.actions.index(pieces[0])

        if len(pieces) == 5 or len(pieces) == 4:
            # case 1:
            # R: <action> : <start-state> : <next-state> : <obs> %f
            # any of <start-state>, <next-state>, and <obs> can be *
            # %f can be on the next line (case where len(pieces) == 4)
            start_state_raw = pieces[1]
            next_state_raw = pieces[2]
            obs_raw = pieces[3]
            prob = float(pieces[4]) if len(pieces) == 5 \
                else float(self.contents[i+1])
            self.__reward_ss(
                action, start_state_raw, next_state_raw, obs_raw, prob)
            return i + 1 if len(pieces) == 5 else i + 2
        elif len(pieces == 3):
            # case 2: R: <action> : <start-state> : <next-state>
            # %f %f ... %f
            start_state = self.states.index(pieces[1])
            next_state = self.states.index(pieces[2])
            next_line = self.contents[i+1]
            probs = next_line.split()
            assert len(probs) == len(self.observations)
            for j in range(len(probs)):
                prob = float(probs[j])
                self.R[(action, start_state, next_state, j)] = prob
            return i + 2
        elif len(pieces == 2):
            # case 3: R: <action> : <start-state>
            # %f %f ... %f
            # %f %f ... %f
            # ...
            # %f %f ... %f
            start_state = self.states.index(pieces[1])
            next_line = self.contents[i+1]
            for j in range(len(self.states)):
                probs = next_line.split()
                assert len(probs) == len(self.observations)
                for k in range(len(probs)):
                    prob = float(probs[k])
                    self.R[(action, start_state, j, k)] = prob
                next_line = self.contents[i+2+j]
            return i + 1 + len(self.states)
        else:
            raise Exception("Cannot parse line: " + line)

    def __reward_ss(self, a, start_state_raw, next_state_raw, obs_raw, prob):
        """
        reward_ss means we're at the start state of the unrolling of the
        reward expression. start_state_raw could be * or the name of the
        real start state.
        """
        if start_state_raw == '*':
            for i in range(len(self.states)):
                self.__reward_ns(a, i, next_state_raw, obs_raw, prob)
        else:
            start_state = self.states.index(start_state_raw)
            self.__reward_ns(a, start_state, next_state_raw, obs_raw, prob)

    def __reward_ns(self, a, start_state, next_state_raw, obs_raw, prob):
        """
        reward_ns means we're at the next state of the unrolling of the
        reward expression. start_state is the number of the real start
        state, and next_state_raw could be * or the name of the real
        next state.
        """
        if next_state_raw == '*':
            for i in range(len(self.states)):
                self.__reward_ob(a, start_state, i, obs_raw, prob)
        else:
            next_state = self.states.index(next_state_raw)
            self.__reward_ob(a, start_state, next_state, obs_raw, prob)

    def __reward_ob(self, a, start_state, next_state, obs_raw, prob):
        """
        reward_ob means we're at the observation of the unrolling of the
        reward expression. start_state is the number of the real start
        state, next_state is the number of the real next state, and
        obs_raw could be * or the name of the real observation.
        """
        if obs_raw == '*':
            for i in range(len(self.observations)):
                self.R[(a, start_state, next_state, i)] = prob
        else:
            obs = self.observations.index(obs_raw)
            self.R[(a, start_state, next_state, obs)] = prob

    def set_transitions(self, transitions):
        """
        set the current transition function to the given list of all transitions
        :param transitions: list of the transitions corresponding to each action (ensure correct order)
                The transitions for an action are given as a complete 2d list, where an entry indicates the probability,
                the first index indicates the state in which the action is taken and the second indicates the next state
        """
        for action_num in range(len(transitions)):
            for curr_state in range(len(transitions[action_num])):
                for next_state in range(len(transitions[action_num][curr_state])):
                    self.T[(action_num,curr_state,next_state)] = transitions[action_num][curr_state][next_state]

    def step(self, action_num):
        next_state_probs = []
        for i in range(len(self.states)):
            next_state_probs.append(self.T[action_num,self.state,i])
        start_state = self.state
        self.state = np.random.choice(len(self.states),1,p=next_state_probs)[0]

        obs_probs = []
        for i in range(len(self.observations)):
            if (action_num,self.state,i) in self.Z:
                obs_probs.append(self.Z[action_num,self.state,i])
            else:
                obs_probs.append(self.Z[None,self.state,i])
        obs = np.random.choice(len(self.observations),1,p=obs_probs)[0]

        if (action_num,start_state,self.state,obs) in self.R:
            self.reward = self.reward * self.discount + self.R[action_num,start_state,self.state,obs]
        else:
            self.reward = self.reward * self.discount + self.R[None,start_state,self.state,obs]
        self.step_am += 1
        return obs




    def print_summary(self):
        print ("discount:", self.discount)
        print ("values:", self.values)
        print ("states:", self.states)
        print ("actions:", self.actions)
        print ("observations:", self.observations)
        print ("")
        print ("T:", self.T)
        print ("")
        print ("Z:", self.Z)
        print ("")
        print ("R:", self.R)
        print("")
        print("state:", self.state)
        print("")
        print("reward:", self.reward)


    def set_transition(self, t): #added to set the transition function as given by t:nparray(a,s,s'), assumed to have correct dims
        for action in range(len(t)):
            for start_state in range(len(t[action])):
                for next_state in range(len(t[action][start_state])):
                    self.T[(action, start_state, next_state)] = t[action][start_state][next_state]

    def get_transition(self):
        nactions = len(self.actions)
        nstates = len(self.states)
        t = np.zeros((nactions, nstates, nstates))
        for a in range(nactions):
            for s1 in range(nstates):
                for s2 in range(nstates):
                    t[a][s1][s2] = self.T[(a,s1,s2)]
        return t




def is_numeric(lst):
    if len(lst) == 1:
        try:
            int(lst[0])
            return True
        except Exception:
            return False
    else:
        return False
