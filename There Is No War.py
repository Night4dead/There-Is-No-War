from tkinter import *
from random import *


#VARIABLES



global index_line, lines
index_line = 0
dialogs_file = open("dialogs.txt", "r")
lines = dialogs_file.readlines()
dialogs_file.close()

config_game_file = open("config_game.txt", "r") #save player
config_s = config_game_file.readlines()
config_game_file.close()

config_test_file = open("config_test.txt", "r") #save témoin
config_test = config_test_file.readlines()
config_test_file.close()

global nb_castle, nb_beach, nb_field, nb_forest, nb_mountain
nb_castle = 0
nb_beach = 0
nb_field = 0
nb_forest = 0
nb_mountain = 0

global nb_of_A_answers, nb_of_B_answers, nb_of_C_answers, nb_of_D_answers
nb_of_A_answers = 0

nb_of_B_answers = 0

nb_of_C_answers = 0

nb_of_D_answers = 0

total_answers = 0

global first_sug, second_sug, third_sug, fourth_sug
first_sug = ""
second_sug = ""
third_sug = ""
fourth_sug = ""



#PARTIE FONCTION

def startGame(): #bah ... lance le jeu quoi
    go_btn.place_forget()
    nextLine_btn.place(x= 10,y=650)
    graphic.delete(ALL)
    imageday = graphic.create_image(680, 400, image = day)
    testGameFile() 
    

def testGameFile(): #ca cest ce qui load la save en fait
    global index_line, nb_of_A_answers, nb_of_B_answers, nb_of_C_answers, nb_of_D_answers
    
    differences = 0
    for i in range(0, len(config_test)): #test si la save player est differente de la save témoin
        
        if config_test[i] == config_s[i]:
            differences += 0
        elif config_test[i] != config_s[i]:
            differences += 1
        
    if differences != 0 : #si tas des trucs dans ta save de differents avec la save témoin (donc que tas de la data)
        dialog.insert(INSERT, "All previously saved data loaded, you can now continue the story." + "\n")
        dialog.see("end")
        index_line = int(config_s[2])
        nb_of_A_answers = int(config_s[3])

        nb_of_B_answers = int(config_s[4])

        nb_of_C_answers = int(config_s[5])
        nb_of_D_answers = int(config_s[6])

        total_answers = int(config_s[1])
        #charge la save dans le jeu 
        for i in range(0, int(config_s[2])): #insert tout le texte qui a deja etait jouer
            testInsert(i)
        nextLine()
    else: # si ta save est égale a la save témoin (donc que tas pas de save quoi)
        dialog.insert(INSERT, "No previously saved data, you are now starting the game from the beginning." + "\n")
        dialog.see("end")
        nextLine() # ce truc c pour charger les 3 premières phrases
        nextLine()
        nextLine()

            
def dispImg():
    graphic.delete(ALL)
    imagerules1 = graphic.create_image(680, 400, image = rules1)
    go_btn.place(x= 10,y=650)        


def newStart(): #truc pour reinitialiser la save IMPORTANT
    global index_line
    config_s[0] = "."
    config_s[1] = 0 #nb de cliques
    config_s[2] = 0 #numéro de la ligne
    config_s[3] = 0 #nb rep A
    config_s[4] = 0 #nb rep B
    config_s[5] = 0 #nb rep C
    config_s[6] = 0 #nb rep D
    config_s[7] = 600 #nb units player
    config_s[8] = 500 #nb units enemy
    #ATTENTION, si tu as une variable précise pour les unités, oublie pas au de la faire égale à int(config_s[8 ou 7]) parce que si tu m'es pas le int(), ca marche pas, car dans le fichier c le chiffre suivi de \n, qui est du string, attenzione okay ?
    config_s[0] = str(config_s[0]) + "\n"
    config_s[1] = str(config_s[1]) + "\n"
    config_s[2] = str(config_s[2]) + "\n"
    config_s[3] = str(config_s[3]) + "\n"
    config_s[4] = str(config_s[4]) + "\n"
    config_s[5] = str(config_s[5]) + "\n"
    config_s[6] = str(config_s[6]) + "\n"
    config_s[7] = str(config_s[7]) + "\n"
    config_s[8] = str(config_s[8]) + "\n"
    config_game_file = open("config_game.txt", "w")
    for i in range(0, len(config_s)):
        config_game_file.write(str(config_s[i]))
    config_game_file.close()
    index_line = 0
    dialog.insert(INSERT, "All saves erased, press the Start button." + "\n")
    dialog.see("end")
    newstart_btn.place_forget()
    
def saveConfig(): #truc de sauvegarde IMPORTANT
    config_game_file = open("config_game.txt", "w")
    for i in range(0, len(config_s)):
        config_game_file.write(str(config_s[i]))
    config_game_file.close()
    dialog.insert(INSERT, "All data saved, you can now exit the game or continue playing." + "\n")
    dialog.see("end")
    print(config_s)




def nextLine():
    global index_line, lines, nb_of_A_answers, nb_of_B_answers, nb_of_C_answers, nb_of_D_answers
    line_readed = ""
    line_readed = lines[index_line]
    if line_readed == "¤": #detecte la fin du dialogue et decide de la fin
        choiceEnd(nb_of_A_answers, nb_of_B_answers, nb_of_C_answers, nb_of_D_answers)
        
        #DEBUT NEXT PART
    if "$" in set(line_readed): #truc qui arrive toute les5 questions
        randomEvent()
        index_line += 1
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
    if "*" in set(line_readed):
        #truc de choix
        nextLine_btn.place_forget()
        choiceSection(line_readed, index_line, lines)
    else: #ligne suivante 
        testInsert(index_line)
        index_line += 1
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
                
def choiceSection(readed, idx, text):
    global first_sug, second_sug, third_sug, fourth_sug
    dialog.insert(INSERT, readed + "\n")
    dialog.see("end")
    
    answerA.config(text = "A : " + text[idx+1])
    answerB.config(text = "B : " + text[idx+2])
    answerC.config(text = "C : " + text[idx+3])
    answerD.config(text = "D : " + text[idx+4])
    answerA.place(x=25, y=25)
    answerB.place(x=25, y=75)
    answerC.place(x=25, y=125)
    answerD.place(x=25, y=175)
    
def randomEvent():
    g_e = [0,1] #20% de chance d'avoir un événement où l'énemi perd des units
    b_e = [2] #10% de chance d'avoir un événement où le joueur perd des units
    result = randint(0,9)
    if result in set(g_e):
        dialog.insert(INSERT, "Messenger : Honorables council members ! News arrived from the spies that the demon army lost fifty units while passing through a volcano !" + "\n" + "\n")
        dialog.see("end")
        config_s[8] = int(config_s[8])-50
        config_s[8] = str(config_s[8])+"\n"
                      
    if result in set(b_e):
        dialog.insert(INSERT, "Messenger : Honorables council members ! A squadron of fifty soldiers stationned up north was destroyed by the demon army !" + "\n" + "\n")
        dialog.see("end")
        config_s[7] = int(config_s[7])-50
        config_s[7] = str(config_s[7])+"\n"
        
    if result not in set(g_e) and result not in set(b_e): #70% chance que rien ne se passe
        pass
 
def testInsert(idx):
    global lines
    line_readed = ""
    line_readed = lines[idx]
    #insert une chaine de caractère a la ligne suivante
    dialog.insert(INSERT,line_readed + "\n")
    dialog.see("end") #fait en sorte que la dernière ligne soit tjrs visible (autoscroll)
    
    
def chooseA():
    global nb_of_A_answers,total_answers, index_line,lines
    nb_of_A_answers +=1
    total_answers += 1
    config_s[3] = nb_of_A_answers
    config_s[3] = str(config_s[3]) + "\n"
    config_s[1] = total_answers
    config_s[1] = str(config_s[1]) + "\n"
    #if total_answers == 20:
        #dispAnswers()
    index_line += 5
    line_readed = ""
    line_readed = lines[index_line]
    testInsert(index_line)
    if "°" in set(line_readed):
        index_line += 4
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        nextLine_btn.place(x= 10,y=650)
    if "°" not in set(line_readed):
        testInsert((index_line +1))
        testInsert((index_line +2))
        testInsert((index_line +3))
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        index_line += 4
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        nextLine_btn.place(x= 10,y=650)
    

def chooseB():
    global nb_of_B_answers,total_answers, index_line
    nb_of_B_answers +=1
    total_answers += 1
    config_s[4] = nb_of_B_answers
    config_s[4] = str(config_s[4]) + "\n"
    config_s[1] = total_answers
    config_s[1] = str(config_s[1]) + "\n"
    #if total_answers == 20:
        #dispAnswers()*
    index_line += 6
    line_readed = ""
    line_readed = lines[index_line]
    testInsert(index_line)
    if "°" in set(line_readed):
        index_line += 3
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        nextLine_btn.place(x= 10,y=650)
    if "°" not in set(line_readed):
        testInsert((index_line -1))
        testInsert((index_line +1))
        testInsert((index_line +2))
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        index_line += 3
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        nextLine_btn.place(x= 10,y=650)

def chooseC():
    global nb_of_C_answers,total_answers, index_line
    nb_of_C_answers +=1
    total_answers += 1
    config_s[5] = nb_of_C_answers
    config_s[5] = str(config_s[5]) + "\n"
    config_s[1] = total_answers
    config_s[1] = str(config_s[1]) + "\n"
    #if total_answers == 20:
        #dispAnswers()
    index_line += 7
    line_readed = ""
    line_readed = lines[index_line]
    testInsert(index_line)
    if "°" in set(line_readed):
        index_line += 2
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        nextLine_btn.place(x= 10,y=650)
    
    if "°" not in set(line_readed):
        testInsert((index_line -2))
        testInsert((index_line -1))
        testInsert((index_line +1))
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        index_line += 2
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        nextLine_btn.place(x= 10,y=650)
    
def chooseD():
    global nb_of_D_answers,total_answers, index_line
    nb_of_D_answers +=1
    total_answers += 1
    config_s[6] = nb_of_D_answers
    config_s[6] = str(config_s[6]) + "\n"
    config_s[1] = total_answers
    config_s[1] = str(config_s[1]) + "\n"
    #if total_answers == 20:
        #dispAnswers()
    index_line += 8
    line_readed = ""
    line_readed = lines[index_line]
    testInsert(index_line)
    if "°" in set(line_readed):
        index_line += 1
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        nextLine_btn.place(x= 10,y=650)
    if "°" not in set(line_readed):
        testInsert((index_line -3))
        testInsert((index_line -2))
        testInsert((index_line -1))
        answerA.place_forget()
        answerB.place_forget()
        answerC.place_forget()
        answerD.place_forget()
        index_line += 1
        config_s[2] = index_line
        config_s[2] = str(config_s[2]) + "\n"
        nextLine_btn.place(x= 10,y=650)


    
def choiceEnd(answerA, answerB, answerC, answerD):
    
    if (answerA>answerC or answerB>answerC) and (answerA>answerD or answerB>answerD): #fin heroique
        dialog.insert(INSERT, '\n'+ "You finished the war council, every member of the council wants to help you to destroy the demon army and the domon king !" + "\n" +"The demon army lost 100 units" + "\n")
        dialog.see("end")
        config_s[8]= int(config_s[8]) - 100
        config_s[8] = str(config_s[8]) + "\n"
        saveConfig()
        nextLine_btn.place_forget()
        nextPart_btn.place(x= 10,y=650)
        #START SECOND PART
    if (answerC>answerA or answerD>answerA) and (answerC>answerB or answerD>answerB) : #fin égoiste
        end = randint(0,3) #council member qui se barre aleatoirement, pour que ca soit tjrs un peu different
        if end == 0:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Chieftain Eria thinks you're not worthy of leading her tribe in a war." + "\n" + "You lose 100 units because Chieftain Eria left the council. "+ "\n")
            dialog.see("end")
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            saveConfig()
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 1:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Representant Galadhlas does not approve of your strategy, and prefer to keep the elves out of the battle." + "\n" + "You lose 100 units because Representant Galadhlas left the council. "+ "\n")
            dialog.see("end")
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            saveConfig()
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 2:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Grandmaster Zedfis does not trust your leadership capabilities and deems you not wise enough to win this war." + "\n" + "You lose 100 units because Grandmaster Zedfis left the council. "+ "\n")
            dialog.see("end")
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            saveConfig()
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 3:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but War chief Thralgud deems the reward for his participation in the war too low and puny." + "\n" + "You lose 100 units because War chief Tharlgud left the council. "+ "\n")
            dialog.see("end")
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            saveConfig()
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
    if (answerA == answerD and(answerA and answerD)>(answerB and answerC)) or (answerA == answerC and(answerA and answerC)>(answerB and answerD)) or (answerB == answerD and(answerB and answerD)>(answerA and answerC)) or (answerB == answerC and(answerB and answerC)>(answerA and answerD)):
        dialog.insert(INSERT, '\n'+ "You finished the war council, everyone is ready to follow you, prepare for the battle !")
        dialog.see("end")
        saveConfig()
        nextLine_btn.place_forget()
        #START SECOND PART
    if answerA == answerB and answerC == answerD and answerA==answerC:
        dialog.insert(INSERT, '\n' + "MUHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAH" + "\n" + "\n" + "THERE" + "\n" + "\n" + "IS" + "\n" + "NO" "\n" + "\n" + "WAR" + "\n" + "You lost the game, the end of the world happened, just as the Demon King planned.")
        dialog.see("end")
        graphic.delete(ALL)
        imagedemon = graphic.create_image(680, 400, image = demon)
        #changement d'image, fin apocalyptique
        nextLine_btn.place_forget()
        well_btn.place(x = 10, y = 650)


def changeImg():
    graphic.delete(ALL)
    imagedefeat = graphic.create_image(680, 400, image = defeat)
    well_btn.place_forget()
    newstart_btn.place(x=10, y=650)
        

    #SECOND JEU


def fctSetup(): #Met en place le second jeu après la partie "dialogues"
    graphic.delete(ALL)
    imagerules2 = graphic.create_image(680, 400, image = rules2)
    answer_outline.place_forget()
    game_outline.place(x=20, y=796)
    nextPart_btn.place_forget()
    button_game.place(x=1250, y=1010)

    label_castle.place(x=40, y=820) #Place les colonnes
    label_beach.place(x=277, y=820)
    label_field.place(x=514, y=820)
    label_forest.place(x=751, y=820)
    label_mountain.place(x=988, y=820)

    scalecastle.place(x=40, y=860)
    scalebeach.place(x=277, y=860)
    scalefield.place(x=514, y=860)
    scaleforest.place(x=751, y=860)
    scalemountain.place(x=988, y=860)


def testBeach():    #Test de la victoire en pourcentage à la plage
    global nb_beach
    beachrand = 0
    if (nb_beach > 130):
        beachrand = randint(1,11)
        if (beachrand == 1 or beachrand == 2 or beachrand == 3 or beachrand == 4 or beachrand == 5 or beachrand == 6 or beachrand == 7):
            return True
        else:
            return False
    if (nb_beach == 130):
        beachrand = randint(1,11)
        if (beachrand == 1 or beachrand == 2 or beachrand == 3 or beachrand == 4 or beachrand == 5):
            return True
        else:
            return False
    if (nb_beach < 130 and nb_beach >= 110):
        beachrand = randint(1,11)
        if (beachrand == 1 or beachrand == 2 or beachrand == 3 or beachrand == 4):
            return True
        else:
            return False
    if (nb_beach < 110 and nb_beach >= 90):
        beachrand = randint(1,11)
        if (beachrand == 1 or beachrand == 2 or beachrand == 3):
            return True
        else:
            return False
    if (nb_beach < 90 and nb_beach >= 70):
        beachrand = randint(1,11)
        if (beachrand == 1 or beachrand == 2):
            return True
        else:
            return False
    if (nb_beach < 70 and nb_beach >= 50):
        beachrand = randint(1,11)
        if (beachrand == 1):
            return True
        else:
            return False
    if (nb_beach < 50):
        return False


def testField():    #Test de la victoire en pourcentage dans le champ
    global nb_field
    fieldrand = 0
    if (nb_field > 150):
        fieldrand = randint(1,11)
        if (fieldrand == 1 or fieldrand == 2 or fieldrand == 3 or fieldrand == 4 or fieldrand == 5 or fieldrand == 6 or fieldrand == 7):
            return True
        else:
            return False
    if (nb_field == 150):
        fieldrand = randint(1,11)
        if (fieldrand == 1 or fieldrand == 2 or fieldrand == 3 or fieldrand == 4 or fieldrand == 5):
            return True
        else:
            return False
    if (nb_field < 150 and nb_field >= 130):
        fieldrand = randint(1,11)
        if (fieldrand == 1 or fieldrand == 2 or fieldrand == 3 or fieldrand == 4):
            return True
        else:
            return False
    if (nb_field < 130 and nb_field >= 110):
        fieldrand = randint(1,11)
        if (fieldrand == 1 or fieldrand == 2 or fieldrand == 3):
            return True
        else:
            return False
    if (nb_field < 110 and nb_field >= 90):
        fieldrand = randint(1,11)
        if (fieldrand == 1 or fieldrand == 2):
            return True
        else:
            return False
    if (nb_field < 90 and nb_field >= 70):
        fieldrand = randint(1,11)
        if (fieldrand == 1):
            return True
        else:
            return False
    if (nb_field < 70):
        return False


def testForest():    #Test de la victoire en pourcentage dans la foret
    global nb_forest
    forestrand = 0
    if (nb_forest > 70):
        forestrand = randint(1,11)
        if (forestrand == 1 or forestrand == 2 or forestrand == 3 or forestrand == 4 or forestrand == 5 or forestrand == 6 or forestrand == 7):
            return True
        else:
            return False
    if (nb_forest == 70):
        forestrand = randint(1,11)
        if (forestrand == 1 or forestrand == 2 or forestrand == 3 or forestrand == 4 or forestrand == 5):
            return True
        else:
            return False
    if (nb_forest < 70 and nb_forest >= 50):
        forestrand = randint(1,11)
        if (forestrand == 1 or forestrand == 2 or forestrand == 3):
            return True
        else:
            return False
    if (nb_forest < 50 and nb_forest >= 30):
        forestrand = randint(1,11)
        if (forestrand == 1):
            return True
        else:
            return False
    if (nb_forest < 30):
        return False


def testMountain(): #Test de la victoire en pourcentage dans la montagne
    global nb_mountain
    mountainrand = 0
    if (nb_mountain > 20):
        mountainrand = randint(1,11)
        if (mountainrand == 1 or mountainrand == 2 or mountainrand == 3 or mountainrand == 4 or mountainrand == 5 or mountainrand == 6 or mountainrand == 7):
            return True
        else:
            return False
    if (nb_mountain == 20):
        mountainrand = randint(1,11)
        if (mountainrand == 1 or mountainrand == 2 or mountainrand == 3 or mountainrand == 4 or mountainrand == 5):
            return True
        else:
            return False
    if (nb_mountain < 20 and nb_mountain >= 10):
        mountainrand = randint(1,11)
        if (mountainrand == 1 or mountainrand == 2 or mountainrand == 3):
            return True
        else:
            return False
    if (nb_mountain < 10):
        return False



def testFinalBattle():
    global nb_castle, testBea, testFie, testFor, testMou
    castlerand = 0
    if (testBea == True and testFie == True and testFor == True and testMou == True): #Test si victoire sur tous les champs de bataille
        if (nb_castle >= 130):
            return True
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5 or castlerand == 6 or castlerand == 7):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == True and testFor == True and testMou == False):  #Test si victoire sur 3 champs de bataille
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5 or castlerand == 6 or castlerand == 7):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == False and testFor == True and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5 or castlerand == 6 or castlerand == 7):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == True and testFor == False and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5 or castlerand == 6 or castlerand == 7):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == False and testFie == True and testFor == True and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5 or castlerand == 6 or castlerand == 7):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == True and testFor == False and testMou == False): #Test si victoire sur 2 champs de bataille
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == False and testFor == True and testMou == False):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == False and testFie == True and testFor == True and testMou == False):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == False and testFor == False and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == False and testFie == True and testFor == False and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == False and testFie == False and testFor == True and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4 or castlerand == 5):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3):
                return True
            else:
                return False
        if (nb_castle < 100 and nb_castle >=50):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 50):
            return False
    if (testBea == True and testFie == False and testFor == False and testMou == False): #Test si victoire sur 1 champ de bataille
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 100):
            return False
    if (testBea == False and testFie == True and testFor == False and testMou == False):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 100):
            return False
    if (testBea == False and testFie == False and testFor == True and testMou == False):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 100):
            return False
    if (testBea == False and testFie == False and testFor == False and testMou == True):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2 or castlerand == 3 or castlerand == 4):
                return True
            else:
                return False
        if (nb_castle < 130 and nb_castle >=100):
            castlerand = randint(1,11)
            if (castlerand == 1):
                return True
            else:
                return False
        if (nb_castle < 100):
            return False
    if (testBea == False and testFie == False and testFor == False and testMou == False):
        if (nb_castle >= 130):
            castlerand = randint(1,11)
            if (castlerand == 1 or castlerand == 2):
                return True
            else:
                return False
        if (nb_castle < 130):
            return False


def FinalBattle():
    finish_btn.place_forget()
    beav.place_forget()
    bead.place_forget()
    fiev.place_forget()
    fied.place_forget()
    forv.place_forget()
    ford.place_forget()
    mouv.place_forget()
    moud.place_forget()

    finalresult = testFinalBattle()
    if (finalresult == True):
        graphic.delete(ALL)
        imagevictory = graphic.create_image(680, 400, image = victory)
    else:
        graphic.delete(ALL)
        imagedefeat = graphic.create_image(680, 400, image = defeat)
        

def fctGameSetup():
    global nb_castle, nb_beach, nb_field, nb_forest, nb_mountain, testBea, testFie, testFor, testMou
    graphic.delete(ALL)
    imagebattle = graphic.create_image(680, 400, image = battle)
    
    nb_castle = scalecastle.get()
    nb_beach = scalebeach.get()
    nb_field = scalefield.get()
    nb_forest = scaleforest.get()
    nb_mountain = scalemountain.get()
    #troupes ennemies: 130, 130, 150, 70, 20
    button_game.place_forget()
    
    label_castle.place_forget()
    label_beach.place_forget()
    label_field.place_forget()
    label_forest.place_forget()
    label_mountain.place_forget()

    scalecastle.place_forget()
    scalebeach.place_forget()
    scalefield.place_forget()
    scaleforest.place_forget()
    scalemountain.place_forget()
    
    testBea = testBeach()
    if (testBea == True):
        beav.place(x=25, y=25)
    else:
        bead.place(x=25, y=25)
    testFie = testField()
    if (testFie == True):
        fiev.place(x=25, y=75)
    else:
        fied.place(x=25, y=75)
    testFor = testForest()
    if (testFor == True):
        forv.place(x=25, y=125)
    else:
        ford.place(x=25, y=125)
    testMou = testMountain()
    if (testMou == True):
        mouv.place(x=25, y=175)
    else:
        moud.place(x=25, y=175)

    finish_btn.place(x=10, y=650)



#PARTIE GRAPHIQUE


root = Tk()
root.geometry("1920x1080")
root.title("There is no War")
root.overrideredirect(True)


graphic = Canvas(root, width = "1324", height = "736", bg = "white", bd = "10", highlightthickness = "10", relief = "ridge")
graphic.place(x=20, y=20)


dialog_outline = LabelFrame(root, height = "756", width = "516", text = "Dialogs")
dialog_outline.place(x=1384, y=20)


answer_outline = LabelFrame(root, height = "264", width = "1344", text = "Answers")
answer_outline.place(x=20, y=796)


options_outline = LabelFrame(root, height = "264", width = "516", text = "Options")
options_outline.place(x=1384, y=796)


button_quit = Button(root,  text = "Quit the Game", command = root.destroy)
button_quit.place(x=1409, y=1006)

button_new = Button(root, text = "New Game", command = newStart)
button_new.place(x=1409, y=946)


button_save = Button(root, text = "Save Game", command = saveConfig)
button_save.place(x=1409, y=886)


start_btn = Button(root, text="Start Game", command = dispImg)
start_btn.place(x=1409, y=826)



"""objets concernant le texte"""


scrollbar = Scrollbar(dialog_outline)
scrollbar.place(x=485, y=0)

dialog = Text(dialog_outline, width="55", yscrollcommand= scrollbar.set)
dialog.place(x=10,y=10)

scrollbar.config(command= dialog.yview)

go_btn = Button(dialog_outline, text="Let's go !", command = startGame)

nextLine_btn = Button(dialog_outline, text="Next line", command = nextLine)

nextPart_btn = Button(dialog_outline, text="Next Part", command = fctSetup)

well_btn = Button(dialog_outline, text="Well...", command = changeImg)

newstart_btn = Button(dialog_outline, text = "New Start", command = newStart)

""" objets concernant les réponses"""


answerA = Button(answer_outline, text= (first_sug), command = chooseA)
#answerA.place(x=25, y=25)

answerB = Button(answer_outline, text=(second_sug), command = chooseB)
#answerB.place(x=25, y=75)

answerC = Button(answer_outline, text=(third_sug), command = chooseC)
#answerC.place(x=25, y=125)

answerD = Button(answer_outline, text=(fourth_sug), command = chooseD)
#answerD.place(x=25, y=175)


    #OBJETS POUR SECOND JEU                           LIMITES: 40 mou, 90 fo, 170 fie, 150 bea, 150 cas



game_outline = LabelFrame(root, height = "264", width = "1344")

button_game = Button(root, text = "Start the Battle !", command = fctGameSetup)

label_castle = Label(root, text = "Units in the castle :")  #Colonnes des differents terrains
label_beach = Label(root, text = "Units on the beach :")
label_field = Label(root, text = "Units on the field :")
label_forest = Label(root, text = "Units in the forest :")
label_mountain = Label(root, text = "Units in the moutains :")


varcastle = DoubleVar()
varbeach = DoubleVar()
varfield = DoubleVar()
varforest = DoubleVar()
varmountain = DoubleVar()


scalecastle = Scale(root, width = "50", from_ = 0, to = 150, variable = varcastle)
scalebeach = Scale(root, width = "50", from_ = 0, to = 150, variable = varbeach)
scalefield = Scale(root, width = "50", from_ = 0, to = 170, variable = varfield)
scaleforest = Scale(root, width = "50", from_ = 0, to = 90, variable = varforest)
scalemountain = Scale(root, width = "50", from_ = 0, to = 40, variable = varmountain)




title = PhotoImage(file="title.png")
imagestart = graphic.create_image(680, 400, image = title)
day = PhotoImage(file="day.png")
demon = PhotoImage(file="demon.png")
rules1 = PhotoImage(file="rulesdia.png")
rules2 = PhotoImage(file="rulesga.png")
victory = PhotoImage(file="victory.png")
defeat = PhotoImage(file="defeat.png")
battle = PhotoImage(file="battle.png")


    #OBJETS BATAILLE


beav = Label(game_outline, text ="Our units have won the battle on the beach battlefield !")
bead = Label(game_outline, text ="Our units have lost the battle on the beach battlefield !")
fiev = Label(game_outline, text ="We won the battle on the fields !")
fied = Label(game_outline, text ="We lost the battle on the fields !")
forv = Label(game_outline, text ="We are victorious in the forest !")
ford = Label(game_outline, text ="We have been defeated in the forest !")
mouv = Label(game_outline, text ="The mountain's units won !")
moud = Label(game_outline, text ="The mountain's units failed !")


finish_btn = Button(dialog_outline, text = "Let's finish this battle !", command = FinalBattle)


root.mainloop()










         
