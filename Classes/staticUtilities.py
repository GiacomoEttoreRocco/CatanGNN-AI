import matplotlib.pyplot as plt
import csv
from Classes import Board

def availableResourcesForColony(resDict):
    return resDict["wood"] >= 1 and resDict["clay"] >= 1 and resDict["sheep"] >= 1 and resDict["crop"] >= 1

def availableResourcesForCity(resDict):
    return resDict["iron"] >= 3 and resDict["crop"] >= 2

def availableResourcesForStreet(resDict):
    return resDict["wood"] >= 1 and resDict["clay"] >= 1 

def availableResourcesForDevCard(resDict):
    return resDict["crop"] >= 1 and resDict["iron"] >= 1 and resDict["sheep"] >= 1

def ownedTileByPlayer(player, tile):
    for place in tile.associatedPlaces:
        if Board.Board().places[place].owner == player.id:
            return True
    return False

def blockableTile(player, tile):
    for place in tile.associatedPlaces:
        if Board.Board().places[place].owner != player.id and Board.Board().places[place].owner != 0 and not ownedTileByPlayer(player, tile):
            # print("Owner: " , Board.Board().places[place].owner)
            return True
    return False

def plotWinners2(winnerIds, listOfAgents):
    counter = range(1, len(winnerIds) + 1)
    sum_ones = 0
    sum_twos = 0
    cumulative_ones = []
    cumulative_twos = []
    for num in winnerIds:
        if num == 1:
            sum_ones += 1
        elif num == 2:
            sum_twos += 1
        cumulative_ones.append(sum_ones)
        cumulative_twos.append(sum_twos)
    plt.figure(1)
    plt.plot(counter, cumulative_ones, color='red', label='Player ' + listOfAgents[0].name())
    plt.plot(counter, cumulative_twos, color='blue', label='Player ' + listOfAgents[1].name())
    plt.xlabel('Episodes')
    plt.ylabel('Player victories')
    handles, labels = plt.gca().get_legend_handles_labels()
    if len(handles) < 3:
        plt.legend()
    plt.pause(0.001)

def plotWinners3(winnerIds, name1, name2, name3):
    counter = range(1, len(winnerIds) + 1)
    sum_ones = 0
    sum_twos = 0
    sum_tr = 0
    cumulative_ones = []
    cumulative_twos = []
    cumulative_tr = []

    for num in winnerIds:
        if num == 1:
            sum_ones += 1
        elif num == 2:
            sum_twos += 1
        else:
            sum_tr += 1
        cumulative_ones.append(sum_ones)
        cumulative_twos.append(sum_twos)
        cumulative_tr.append(sum_tr)

    plt.figure(1)
    plt.plot(counter, cumulative_ones, color='red', label='Player ' + name1)
    plt.plot(counter, cumulative_twos, color='blue', label='Player ' + name2)
    plt.plot(counter, cumulative_tr, color='orange', label='Player ' + name3)

    plt.xlabel('Episodes')
    plt.ylabel('Player victories')
    handles, labels = plt.gca().get_legend_handles_labels()
    if len(handles) < 4:
        plt.legend()
    plt.pause(0.001)

def saveInCsv(data, nome_file):
    with open(nome_file, 'a', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(data)

def plotCsvColumns(nome_file):
    with open(nome_file, 'r') as file_csv:
        reader = csv.reader(file_csv)
        data = list(reader)
    
    # Estrai i dati dalle colonne
    colonna1 = [float(row[0]) for row in data]
    colonna2 = [float(row[1]) for row in data]
    
    # Traccia i valori delle colonne
    plt.plot(colonna1, color='red', label='Colonna 1')
    plt.plot(colonna2, color='blue', label='Colonna 2')
    
    # Imposta i titoli degli assi e la legenda
    plt.xlabel('Indice')
    plt.ylabel('Valore')
    plt.legend()
    
    # Mostra il grafico
    plt.show()

def plotCsvColumnsWithHeaders(nome_file):
    with open(nome_file, 'r') as file_csv:
        reader = csv.reader(file_csv)
        headers = next(reader)  # Salta le etichette delle colonne
        data = list(reader)
    
    # Estrai i dati dalle colonne
    colonna1 = [float(row[0]) for row in data]
    colonna2 = [float(row[1]) for row in data]
    
    # Traccia i valori delle colonne
    plt.plot(colonna1, color='red', label=headers[0])
    plt.plot(colonna2, color='blue', label=headers[1])
    
    # Imposta i titoli degli assi e la legenda
    plt.xlabel('Indice')
    plt.ylabel('Valore')
    plt.legend()
    
    # Mostra il grafico
    plt.show()
