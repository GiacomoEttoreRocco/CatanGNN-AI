import Move, Bank
from Board import Board
import random

class Player: 
    def __init__(self, id, game):
        self.id = id
        self.victoryPoints = 0
        self.game = game

        self.usedKnights = 0
        self.unusedKnights = 0
        self.justBoughtKnights = 0

        self.monopolyCard = 0
        self.justBoughtMonopolyCard = 0

        self.roadBuildingCard = 0
        self.justBoughtRoadBuildingCard = 0
        
        self.yearOfPlentyCard = 0
        self.justBoughtYearOfPlentyCard = 0

        # RESOURCES:
        self.resources = {"wood" : 0, "clay" : 0, "crop": 0, "sheep": 0, "iron":0}

        #HARBRS: 
        self.ownedHarbors = []

    def availableMoves(self, turnCardUsed):

        availableMoves = [Move.passTurn]

        if(self.resources["wood"] >= 2 and self.resources["clay"] >= 2): 
            availableMoves.append(Move.placeStreet)

        if(self.resources["wood"] >= 1  and self.resources["clay"] >= 1 and self.resources["sheep"] >= 1 and self.resources["crop"] >= 1):
            availableMoves.append(Move.placeColony)

        if(self.resources["iron"] >= 3 and self.resources["crop"] >= 2):
            availableMoves.append(Move.placeCity)

        if(self.resources["iron"] >= 1 and self.resources["crop"] >= 1 and self.resources["sheep"] >= 1):
            availableMoves.append(Move.buyDevCard)

        if("3:1" in self.ownedHarbors):
            if(self.resources["wood"] >= 3 or self.resources["clay"] >= 3 or self.resources["crop"] >= 3 or self.resources["iron"] >= 3 or self.resources["sheep"] >= 3):
                availableMoves.append(Move.tradeBank)

        if("2:1 clay" in self.ownedHarbors):
            if(self.resources["clay"] >= 2):
                availableMoves.append(Move.tradeBank)

        if("2:1 iron" in self.ownedHarbors):
            if(self.resources["iron"] >= 2):
                availableMoves.append(Move.tradeBank)

        if("2:1 crop" in self.ownedHarbors):
            if(self.resources["crop"] >= 2):
                availableMoves.append(Move.tradeBank)
        if("2:1 wood" in self.ownedHarbors):
            if(self.resources["wood"] >= 2):
                availableMoves.append(Move.tradeBank)

        if("2:1 sheep" in self.ownedHarbors):
            if(self.resources["sheep"] >= 2):
                availableMoves.append(Move.tradeBank)

        if(self.unusedKnights >= 1 and not turnCardUsed):
            availableMoves.append(Move.useKnight)    

        if(self.monopolyCard >= 1 and not turnCardUsed):
            availableMoves.append(Move.useMonopolyCard)

        if(self.roadBuildingCard >= 1 and not turnCardUsed):
            availableMoves.append(Move.useRoadBuildingCard)

        if(self.yearOfPlentyCard >= 1 and not turnCardUsed):
            availableMoves.append(Move.useYearOfPlentyCard)

        return availableMoves

    def connectedEmptyEdges(self, edge):
        p1 = edge[0]
        p2 = edge[1]
        toRet = []
        if(Board().places[p1].owner == 0 or Board().places[p1].owner == self.id):
            for p in Board().graph.listOfAdj[p1]:
                if(p2 != p):
                    edge = tuple(sorted([p1, p]))
                    if(edge.owner == 0):
                        toRet.append()

        if(Board().places[p2].owner == 0 or Board().places[p2].owner == self.id):
            for p in Board().graph.listOfAdj[p2]:
                if(p1 != p):
                    edge = tuple(sorted([p2, p]))
                    if(edge.owner == 0):
                        toRet.append()
        return toRet

    def calculatePossibleEdges(self):
        possibleEdges = []
        for edge in Board().edges.keys():
            if(Board().edges[edge] == self.id):
                print(edge)
                possibleEdges.extend(self.connectedEmptyEdges(edge))
        return possibleEdges

    def calculatePossibleInitialColony(self):
        toRet = []
        for p in Board().places:
            if(p.owner == 0):
                available = True
                for padj in Board().graph.listOfAdj[p.id]:
                    if(Board().places[padj].owner != 0):
                        available = False
                if(available):
                    toRet.append(p)
        return toRet

    def calculatePossibleInitialStreets(self):
        #toRet = []
        for p in Board().places:
            if(p.owner == self.id):
                streetOccupied = False
                toRet = []
                for padj in Board().graph.listOfAdj[p.id]:
                    edge = tuple(sorted([p.id, padj]))
                    if(Board().edges[edge] != 0):
                        streetOccupied = True
                    toRet.append(edge)

                if(not streetOccupied):
                    return toRet


    def calculatePossibleColony(self):
        possibleColonies = []
        for p in Board().places:
            if(p.owner == 0):
                for p_adj in Board().graph.listOfAdj[p.id]:
                    edge = tuple(sorted([p.id, p_adj]))
                    if(Board().edges[edge] == self.id): #controlliamo che l'arco appartenga al giocatore, edges è un dictionary che prende in input l'edge e torna il peso
                        available = True
                        for p_adj_adj in Board().graph.listOfAdj[p_adj]:
                            if(Board().places[p_adj_adj].owner != 0):
                                available = False
                        if(available):
                            possibleColonies.append(p_adj)
        return possibleColonies

    def calculatePossibleCity(self):
        possibleCities = []
        for p in Board().places:
            if(p.owner == self.id and p.isColony == 1):
                possibleCities.append(p.id)
        return possibleCities

    def calculatePossibleTrades(self):
        possibleTrades = []
        for resource in self.resources.keys():
            if(self.resources[resource] >= Bank().resourceToAsk(self, resource)):
                for resourceToAsk in self.resources.keys():
                    #if(resourceToAsk != resource):
                    possibleTrades.append((resource, resourceToAsk))
        return possibleTrades
    
    def evaluate(self, move):
        ########
        if(move == Move.discardResource):
            pass ###############################################################################################################################
       
        if(move == Move.placeFreeStreet):
            possibleEdges = self.calculatePossibleInitialStreets()
            candidateEdge = None
            max = 0
            for edge in possibleEdges: 
                valutation = self.moveValue(move, edge)
                if(max < valutation):
                    max = valutation
                    candidateEdge = edge
            return max, candidateEdge
        if(move == Move.placeFreeColony):
            possibleColony = self.calculatePossibleInitialColony()
            #print(possibleColony)
            candidateColony = None
            max = 0
            for colony in possibleColony:
                valutation = self.moveValue(move, colony)
                if(max < valutation):
                    max = valutation
                    candidateColony = colony
            return max, candidateColony        
        if(move == Move.placeStreet):
            possibleEdges = self.calculatePossibleEdges()
            candidateEdge = None
            max = 0
            for edge in possibleEdges: 
                valutation = self.moveValue(move, edge)
                if(max < valutation):
                    max = valutation
                    candidateEdge = edge
            return max, candidateEdge
        
        if(move == Move.placeColony):
            possibleColony = self.calculatePossibleColony()
            candidateColony = None
            max = 0
            for colony in possibleColony:
                valutation = self.moveValue(move, colony)
                if(max < valutation):
                    max = valutation
                    candidateColony = colony
            return max, candidateColony

        if(move == Move.placeCity):
            possibleCity = self.calculatePossibleCity()
            candidateCity = None
            max = 0
            for city in possibleCity:
                valutation = self.moveValue(move, city)
                if(max < valutation):
                    max = valutation
                    candidateCity = city
            return max, candidateCity            

        if(move == Move.buyDevCard):
            possibleCard = {"knight" : 14 - self.game.totalKnightsUsed(), "victory_point" : 5, "road_building" : 2, "year_of_plenty" : 2 , "monopoly" : 2}
            valutation = 0
            total_cards = sum(possibleCard.items())
            for card in possibleCard.keys():
                valutation = valutation + Board().moveValue(move, card) * (possibleCard[card] / total_cards)
            return valutation, None

        if(move == Move.passTurn):
            print("debug riga 233 player: ", move, "\n")
            return self.moveValue(move), None

        if(move == Move.useKnight):
            max = 0
            for tilePos in Board().tiles.identificator: 
                valutation = self.moveValue(move, tilePos)
                if(max < valutation):
                    max = valutation
                    candidatePos = tilePos
            return max, candidatePos

        if(move == Move.tradeBank):
            possibleTrades = self.calculatePossibleTrades()
            candidateTrade = None
            max = 0
            for trade in possibleTrades:
                valutation = self.moveValue(move, trade)
                if(max < valutation):
                    max = valutation
                    candidateTrade = trade
            return max, candidateTrade

        if(move == Move.useMonopolyCard):
            max = 0
            for res in Board().resources.keys():
                valutation = self.moveValue(move, res)
                if(max < valutation):
                    max = valutation
                    candidateRes = res
            return max, candidateRes

        if(move == Move.useYearOfPlentyCard):
            candidateRes = ()
            max = 0
            for res1 in Bank().resourse.key():
                for res2 in Bank().resourse.key():
                    valutation = self.moveValue(move, (res1, res2))
                    if(max < valutation):
                        max = valutation
                        candidateRes = (res1, res2)
            return max, candidateRes

    def totalCards(self):
        return sum(self.resources.items())

    def moveValue(self, move, thingNeeded = None):
        print("Pre if, riga 278 in Player :, ", move)
        if(move == Move.passTurn):
            print("Debug linea 279 in Player, pass turn case.")
            return 0.2 + random.randrange(0,2)

        if(move == Move.useKnight or move == Move.useRobber):
            previousTilePos = move(self, thingNeeded)
            toRet = 1.5
            move(self, previousTilePos, True) # ATTUALMENTE è INUTILE SIA QUESTA RIGA CHE QUELLA SOPRA
            return toRet + random.randrange(0,2)

        move(self, thingNeeded)
        #toRet = 0
        if(move == Move.placeFreeColony):
            toRet = 10
        if(move == Move.placeFreeStreet):
            toRet = 10
        if(move == Move.placeCity):
            toRet = 1
        if(move == Move.placeColony):
            toRet = 0.9
        if(move == Move.placeStreet):
            toRet = 0.7
        if(move == Move.buyDevCard):
            toRet = 0.6
        if(move == Move.tradeBank):
            toRet = 0.2
        if(move == Move.useMonopolyCard):
            toRet = 2
        if(move == Move.useRoadBuildingCard):
            toRet = 2
        if(move == Move.useYearOfPlentyCard):
            toRet = 2
        move(self, thingNeeded, undo=True)
        return toRet + random.randrange(0,2)


