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

    a = rootstate.give_coor()
    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        rootstate.Clone(a)
        # rootstate.render()
        reward = 0

        # Select
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.UCTSelectChild()
            s_, reward_mid, done= rootstate.step(node.move)
            # rootstate.render()
            reward = reward + reward_mid

        # Expand
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            s_,reward_mid,done = rootstate.step(m)
            # rootstate.render()
            node = node.AddChild(m, rootstate)
            reward = reward + reward_mid

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while rootstate.end != True:  # while state is non-terminal  #limit steps
            act_tem = random.choice(rootstate.GetMoves())
            s_mid,reward_mid,done_mid = rootstate.step(act_tem)
            # rootstate.render()
            reward = reward + reward_mid

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(reward)  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    rootstate.Clone(a)
    # rootstate.render()

    # Output some information about the tree - can be omitted
    if (verbose):
        print (rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


if __name__ == "__main__":
    env = Maze("train")
    env.render()

    path = []
    i = 0
    while(env.end != True):
        i = i + 1
        m = UCT(rootstate=env, itermax=1000, verbose=False)
        path.append(m)
        s_,reward,done = env.step(m)
        print([i, m, s_, reward])
        # time.sleep(0.1)
        env.render()

    env2 = Maze("test")
    for i in path:
        action = i
        s, reward, done = env2.step(action)
        print([s, reward, done])
        time.sleep(1)
        env.render()
    print("end path")
    print(path)
    # env.after(100, update)






    env.mainloop()

