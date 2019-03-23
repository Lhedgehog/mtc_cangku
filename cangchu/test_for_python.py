from cangku_env.shortest_path_game import Maze
import time
from math import *
import random
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        # self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        state.render()
        reward = 0
        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            s_, reward_mid, done= state.step(node.move)
            time.sleep(0.1)
            state.render()
            reward = reward + reward_mid

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            s_,reward_mid,done = state.step(m)
            time.sleep(0.1)
            state.render()
            node = node.AddChild(m, state)  # add child and descend tree
            reward = reward + reward_mid

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.end != False:  # while state is non-terminal
            s_mid,reward_mid,done_mid = state.step(random.choice(state.GetMoves()))
            time.sleep(0.1)
            state.render()
            reward = reward + reward_mid

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(reward)  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

        state.quit()

    # Output some information about the tree - can be omitted
    if (verbose):
        print (rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


if __name__ == "__main__":
    env = Maze()
    env.render()

    # while(env.end != True):
    #     m = UCT(rootstate=env, itermax=10, verbose=True)
    #     s_,reward,done = env.step(m)
    #     time.sleep(0.1)
    #     env.render()
    act = env.canvas.coords(env.rect)
    action = 2
    s, reward, done = env.step(action)
    print([s, reward, done])
    time.sleep(1)
    env.render()

    action = 2
    s, reward, done = env.step(action)
    print([s, reward, done])
    time.sleep(1)
    env.render()

    action = 1
    s, reward, done = env.step(action)
    print([s, reward, done])
    time.sleep(1)
    env.render()

    env.Clone(act)
    time.sleep(1)
    env.render()

    # env.after(100, update)






    env.mainloop()

