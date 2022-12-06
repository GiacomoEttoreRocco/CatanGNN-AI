import Player
from Board import Board
from Bank import Bank
from CatanGraph import Place

def placeFreeStreet(player, edge, undo = False, justCheck = False):
    previousLongestStreetOwner = player.game.longestStreetPlayer(justCheck)
    if(not undo):
        Board().edges[edge] = player.id
        player.nStreets+=1
        player.ownedStreets.append(edge)
    else:
        Board().edges[edge] = 0
        player.nStreets-=1
        del player.ownedStreets[-1]

    actualLongestStreetOwner = player.game.longestStreetPlayer(justCheck)
    if(previousLongestStreetOwner != actualLongestStreetOwner):
        actualLongestStreetOwner.victoryPoints += 2
        previousLongestStreetOwner.victoryPoints -= 2

def placeFreeColony(player: Player, place: Place, undo = False):
    if(not undo):
        Board().places[place.id].owner = player.id
        Board().places[place.id].isColony = True
        player.victoryPoints+=1
        player.nColonies+=1
        player.ownedColonies.append(place.id)
    else:
        Board().places[place.id].owner = 0
        Board().places[place.id].isColony = False
        player.victoryPoints-=1
        player.nColonies-=1
        del player.ownedColonies[-1]

def placeStreet(player, edge, undo = False, justCheck = False):
    previousLongestStreetOwner = player.game.longestStreetPlayer(justCheck)
    if(not undo):
        player.useResource("wood")
        player.useResource("clay")
        Board().edges[edge] = player.id
        player.nStreets+=1
        player.ownedStreets.append(edge)
        # actualLongestStreetOwner = player.game.longestStreetPlayer(justCheck)
        # if(previousLongestStreetOwner != actualLongestStreetOwner):
        #     actualLongestStreetOwner.victoryPoints += 2
        #     previousLongestStreetOwner.victoryPoints -= 2
    else:
        Bank().giveResource(player, "wood")   
        Bank().giveResource(player, "clay")    
        Board().edges[edge] = 0
        player.nStreets-=1
        del player.ownedStreets[-1]
    actualLongestStreetOwner = player.game.longestStreetPlayer(justCheck)
    if(previousLongestStreetOwner != actualLongestStreetOwner):
        actualLongestStreetOwner.victoryPoints += 2
        previousLongestStreetOwner.victoryPoints -= 2


def placeColony(player, place: Place, undo = False):
    if(not undo):
        player.useResource("wood")
        player.useResource("clay")
        player.useResource("crop")
        player.useResource("sheep")

        place.owner = player.id
        place.isColony = True

        player.victoryPoints+=1
        player.nColonies+=1
        player.ownedColonies.append(place.id)

        if(place.harbor != ""):
            player.ownedHarbors.append(place.harbor)
    else:
        Bank().giveResource(player, "wood")   
        Bank().giveResource(player, "clay")  
        Bank().giveResource(player, "crop")   
        Bank().giveResource(player, "sheep")  

        place.owner = 0
        place.isColony = False
        player.victoryPoints-=1
        player.nColonies-=1
        del player.ownedColonies[-1]

        if(place.harbor != ""):
            del player.ownedHarbors[-1]

def placeCity(player, place: Place, undo = False):
    if(not undo):
        player.useResource("iron")
        player.useResource("iron")
        player.useResource("iron")
        player.useResource("crop")
        player.useResource("crop")

        Board().places[place.id].isColony = False
        Board().places[place.id].isCity = True
        player.victoryPoints+=1
        player.nCities+=1
        player.nColonies-=1
        player.ownedCities.append(place.id)


    else:
        Bank().giveResource(player, "iron")
        Bank().giveResource(player, "iron")
        Bank().giveResource(player, "iron")
        Bank().giveResource(player, "crop")
        Bank().giveResource(player, "crop")

        Board().places[place.id].isColony = True
        Board().places[place.id].isCity = False
        player.victoryPoints-=1
        player.nCities-=1
        player.nColonies+=1
        del player.ownedCities[-1]

def buyDevCard(player, card, undo = False):
    if(not undo):
        player.useResource("iron")
        player.useResource("crop")
        player.useResource("sheep")

        card = Board().deck[0] ##### IL DECK VIENE TOCCATO QUA

        if(card == "knight"):
            player.justBoughtKnights += 1
        if(card == "monopoly"):
            player.justBoughtMonopolyCard += 1
        if(card == "road_building"):
            player.justBoughtRoadBuildingCard += 1
        if(card == "year_of_plenty"):
            player.justBoughtYearOfPlentyCard += 1
        if(card == "victory_point"):
            player.victoryPoints += 1
            player.victoryPointsCards += 1
        Board().deck = Board().deck[1:] 

    else:
        print("Debug: BUG wrong way. (riga 114 move")
        Bank().giveResource(player, "iron")
        Bank().giveResource(player, "crop")
        Bank().giveResource(player, "sheep")

def discardResource(player, resource, undo = False):
    if(not undo):
        print("debug riga 124 move")
        player.useResource(resource)
    else:
        print("debug riga 124 move, undo")
        Bank().giveResource(player, resource)

def passTurn(player, temp):
    pass

def useRobber(player, tilePosition, undo = False):
    previousPosition = Board().robberTile
    Board().robberTile = tilePosition
    return previousPosition

def useKnight(player, tilePosition, undo = False, justCheck = False):
    largArmy = player.game.largestArmy(justCheck)
    previousPosition = Board().robberTile
    Board().robberTile = tilePosition
    if(not undo):
        player.unusedKnights -= 1
        player.usedKnights += 1
    else:
        player.unusedKnights += 1
        player.usedKnights -= 1
    postMoveLargArmy = player.game.largestArmy(justCheck)
    if(largArmy != postMoveLargArmy):
        postMoveLargArmy.victoryPoints += 2 
        largArmy.victoryPoints -= 2
    return previousPosition

def tradeBank(player, coupleOfResources, undo = False):
    toTake, toGive = coupleOfResources
    if(not undo):
        Bank().giveResource(player, toTake)
        for _ in range(0, Bank().resourceToAsk(player, toGive)):
            player.useResource(toGive)
        #print("TAKEN 1", toTake, " GIVEN ", Bank().resourceToAsk(player, toGive), toGive)
    else:
        player.useResource(toTake)
        for i in range(0, Bank().resourceToAsk(player, toGive)):
            Bank().giveResource(player, toGive)
        #print("UNDO OF: TAKEN 1", toTake, " GIVEN ", Bank().resourceToAsk(player, toGive), toGive)

def useMonopolyCard(player, resource):
    player.monopolyCard = player.monopolyCard - 1
    sum = 0
    for p in player.game.players:
        sum = sum + p.resources[resource]
        p.resources[resource] = 0
    player.resources[resource] = sum
    return
    
def useRoadBuildingCard(player, edges, undo = False):

    if(not undo):
        player.roadBuildingCard -= 1
    else:
        player.roadBuildingCard += 1

    placeFreeStreet(player, edges[0], undo)
    placeFreeStreet(player, edges[1], undo)

def useYearOfPlentyCard(player, resources, undo = False):
    if not undo:
        Bank().giveResource(player, resources[0])
        Bank().giveResource(player, resources[1])
    else:
        player.useResource(resources[0])
        player.useResource(resources[1])

def cardMoves():
    return [useMonopolyCard, useKnight, useYearOfPlentyCard, useRoadBuildingCard]

        