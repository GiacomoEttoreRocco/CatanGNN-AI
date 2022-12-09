import Classes as c
import pygame
import Graphics.GameView as GameView
import time

def goNextIfInvio():
    event = pygame.event.wait()
    #print("EVENT: ---------------------> ", event)
    while event.type != pygame.KEYDOWN:
        event = pygame.event.wait()
    view.updateGameScreen()

def doTurnGraphic(game: c.Game, player: c.Player, withGraphic = False):
    #player.printStats()
    turnCardUsed = False # SI PUò USARE UNA SOLA CARTA SVILUPPO A TURNO.
    player.unusedKnights = player.unusedKnights + player.justBoughtKnights
    player.justBoughtKnights = 0
    player.monopolyCard += player.justBoughtMonopolyCard
    player.justBoughtMonopolyCard = 0
    player.roadBuildingCard += player.justBoughtRoadBuildingCard
    player.justBoughtRoadBuildingCard = 0
    player.yearOfPlentyCard += player.justBoughtYearOfPlentyCard
    player.justBoughtYearOfPlentyCard = 0
    view.updateGameScreen() 
    if(player.unusedKnights > 0 and not turnCardUsed):
        actualEvaluation = c.Board.Board().actualEvaluation()
        afterKnight, place = player.evaluate(c.Move.useKnight)
        if(afterKnight > actualEvaluation):
            c.Move.useKnight(player, place)
            print("BEFORE ROLL DICE: ", c.Move.useKnight, "\n")
            view.updateGameScreen()
            turnCardUsed = True 
    if(game.checkWon(player)):
        return
    ####################################################################### ROLL DICES #####################################################################   
    dicesValue = game.rollDice()
    ########################################################################################################################################################
    print("Dice value: ", dicesValue)
    if(dicesValue == 7):
        print("############# SEVEN! #############")
        ev, pos = player.evaluate(c.Move.useRobber)
        #print("POS: ", pos)
        c.Move.useRobber(player, pos)
        #print("POS: ", pos)
    else:
        game.dice_production(dicesValue)
    move, thingNeeded = game.bestMove(player, turnCardUsed)
    move(player, thingNeeded)
    goNextIfInvio()
    print("Player ", player.id, " mossa: ", move, " ")
    if(game.checkWon(player)):
        return
    if(move in c.Move.cardMoves()):
            turnCardUsed = True
    while(move != c.Move.passTurn and not game.checkWon(player)): # move è una funzione 
        move, thingNeeded = game.bestMove(player, turnCardUsed)
        move(player, thingNeeded)
        goNextIfInvio()
        print("Player ", player.id, " mossa: ", move, " ")
        if(move in c.Move.cardMoves()):
            turnCardUsed = True

def playGameWithGraphic(game, view):
    running = True
    GameView.GameView.setupAndDisplayBoard(view)
    GameView.GameView.setupPlaces(view)
    GameView.GameView.updateGameScreen(view)
    pygame.display.update()
    turn = 1 
    won = False
    # START INIZIALE
    for p in game.players:
        game.doInitialChoise(p)
        goNextIfInvio()

    for p in sorted(game.players, reverse=True):
        game.doInitialChoise(p)
        goNextIfInvio()

    while won == False:
        playerTurn = game.players[turn%game.nplayer]
        turn += 1
        #playerTurn.printStats()
        doTurnGraphic(game, playerTurn)
        if(playerTurn.victoryPoints >= 10):
            return playerTurn
        if(turn % 4 == 0):
            print("========================================== Start of turn: ", str(int(turn/4)), "=========================================================")
    goNextIfInvio()
    pygame.quit()

g = c.Game.Game()
view = GameView.GameView(g)
playGameWithGraphic(g, view)

