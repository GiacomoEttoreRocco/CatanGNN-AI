from Classes import Bank, Board
from Classes.MoveTypes import *
from Classes.Strategy.StrategyEuristic import StrategyEuristic
from Classes.staticUtilities import *
from Command import commands, controller
from RL.DQGNN import DQGNNagent
import random

class ReinforcementLearningStrategyGnn(StrategyEuristic):
    def __init__(self): # diventerà un singleton
        print("RANDOM EURISTIC CONSTRUCTOR")
        # self.macroDQN = DQGNNagent(11, 10) 
        # self.eps = self.macroDQN.EPS

    def name(self):
        return "REUR"

    def bestAction(self, player):  #, previousReward):
        if(player.game.actualTurn<player.game.nplayers):
            return self.chooseParameters(commands.FirstChoiseCommand, player)
        elif(player.game.actualTurn<player.game.nplayers*2):
            return self.chooseParameters(commands.SecondChoiseCommand, player)
        else:
            # graph = Board.Board().boardStateGraph(player)
            # glob = player.globalFeaturesToTensor()
            # RICORDATI CHE VANNO GESTITE LE FORCED MOVES, in futuro.
            idActions = player.availableTurnActionsId()
            if(len(idActions) == 1 and idActions[0] == 0):
                return commands.PassTurnCommand, None, True
            # bestMove = self.macroDQN.step(graph, glob, player.availableTurnActionsId()) 
            bestMove = random.choice(bestMove)
        return self.chooseParameters(idToCommand(bestMove), player) # bestAction, thingsNeeded, onlyPassTurn
        