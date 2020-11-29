from tkinter import *
from random import *
import webbrowser

#VARIABLES

website_url = 'home.html'



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
    game_outline.place_forget()
    answer_outline.place(x=20, y=796)
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
        saveConfig()
        config_s[8]= int(config_s[8]) - 100
        config_s[8] = str(config_s[8]) + "\n"
        
        nextLine_btn.place_forget()
        nextPart_btn.place(x= 10,y=650)
        #START SECOND PART
    if (answerC>answerA or answerD>answerA) and (answerC>answerB or answerD>answerB) : #fin égoiste
        end = randint(0,3) #council member qui se barre aleatoirement, pour que ca soit tjrs un peu different
        if end == 0:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Chieftain Eria thinks you're not worthy of leading her tribe in a war." + "\n" + "You lose 100 units because Chieftain Eria left the council. "+ "\n")
            dialog.see("end")
            saveConfig()
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 1:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Representant Galadhlas does not approve of your strategy, and prefer to keep the elves out of the battle." + "\n" + "You lose 100 units because Representant Galadhlas left the council. "+ "\n")
            dialog.see("end")
            saveConfig()
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 2:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but Grandmaster Zedfis does not trust your leadership capabilities and deems you not wise enough to win this war." + "\n" + "You lose 100 units because Grandmaster Zedfis left the council. "+ "\n")
            dialog.see("end")
            saveConfig()
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
        if end == 3:
            dialog.insert(INSERT, '\n'+ "You finished the war council, but War chief Thralgud deems the reward for his participation in the war too low and puny." + "\n" + "You lose 100 units because War chief Tharlgud left the council. "+ "\n")
            dialog.see("end")
            saveConfig()
            config_s[7]= int(config_s[7]) - 100
            config_s[7] = str(config_s[7]) + "\n"
            
            nextLine_btn.place_forget()
            nextPart_btn.place(x= 10,y=650)
            #START SECOND PART
    if (answerA == answerD and(answerA and answerD)>(answerB and answerC)) or (answerA == answerC and(answerA and answerC)>(answerB and answerD)) or (answerB == answerD and(answerB and answerD)>(answerA and answerC)) or (answerB == answerC and(answerB and answerC)>(answerA and answerD)):
        dialog.insert(INSERT, '\n'+ "You finished the war council, everyone is ready to follow you, prepare for the battle !")
        dialog.see("end")
        saveConfig()
        nextLine_btn.place_forget()
        nextPart_btn.place(x=10,y=650)
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
    if int(config_s[7]) == 600:
        scalecastle.place(x=40, y=860)
        scalebeach.place(x=277, y=860)
        scalefield.place(x=514, y=860)
        scaleforest.place(x=751, y=860)
        scalemountain.place(x=988, y=860)
    if int(config_s[7]) < 600 :
        val_minus = (600-int(config_s[7])) / 5
        val_max_castle = scalecastle.cget("to") - val_minus
        scalecastle.config(to= val_max_castle)
        scalecastle.place(x=40, y=860)

        val_max_beach = scalebeach.cget("to") - val_minus
        scalebeach.config(to= val_max_beach)
        scalebeach.place(x=277, y=860)

        val_max_field = scalefield.cget("to") - val_minus
        scalefield.config(to= val_max_field)
        scalefield.place(x=514, y=860)

        val_max_forest = scaleforest.cget("to") - val_minus
        scaleforest.config(to= val_max_forest)
        scaleforest.place(x=751, y=860)

        val_max_mountain = scalemountain.cget("to") - val_minus
        scalemountain.config(to= val_max_mountain)
        scalemountain.place(x=988, y=860)
    if int(config_s[7]) <= 400 :
        graphic.delete(ALL)
        dialog.insert(INSERT, "Your total number of unities is under 400, there is no possible way for you to win against the Demon Lord, you lose.")
        dialog.see("end")
        imagedefeat = graphic.create_image(680, 400, image = defeat)
        newstart_btn.place(x=10, y=650)
        


def testBeach(nb, nb_d):    #Test de la victoire en pourcentage à la plage
    
    if nb == 0:
        beanounit.place(x=25, y=25)
        return ((2*nb_d)/3)
    else : 
        if (nb_d/nb)*100 < 66:
            #defeat the demon and half your units continues on to the demon king castle
            beav.place(x=25, y=25)
            return (nb - nb_d)
        elif (nb_d/nb)*100 <= 92 and (nb_d/nb)*100 >= 66:
            #tie, both garrisons lose
            beatie.place(x=25,y=25)
            return 0
        elif (nb_d/nb)*100 > 92:
            #your loss, half the d units continues on to your castle
            bead.place(x=25,y=25)
            return (nb_d- nb)


def testField(nb, nb_d):    #Test de la victoire en pourcentage dans le champ
    
    if nb == 0:
        fienounit.place(x=25, y=75)
        return ((2*nb_d)/3)
    else : 
        if (nb_d/nb)*100 < 55:
            #defeat the demon and half your units continues on to the demon king castle
            fiev.place(x=25, y=75)
            return (nb - nb_d)
        elif (nb_d/nb)*100 <= 82 and (nb_d/nb)*100 >= 55:
            #tie, both garrisons lose
            fietie.place(x=25, y=75)
            return 0
        elif (nb_d/nb)*100 > 82:
            #your loss, half the d units continues on to your castle
            fied.place(x=25, y=75)
            return (nb_d - nb)


def testForest(nb, nb_d):    #Test de la victoire en pourcentage dans la foret
    
    if nb == 0:
        fornounit.place(x=25, y=125)
        return ((2*nb_d)/3)
    else :
        if (nb_d/nb)*100 < 55:
            #defeat the demon and half your units continues on to the demon king castle
            forv.place(x=25, y=125)
            return (nb - nb_d)
        elif (nb_d/nb)*100 <= 82 and (nb_d/nb)*100 >= 55:
            #tie, both garrisons lose
            fortie.place(x=25, y=125)
            return 0
        elif (nb_d/nb)*100 > 82:
            #your loss, half the d units continues on to your castle
            ford.place(x=25, y=125)
            return (nb_d - nb)


def testMountain(nb, nb_d): #Test de la victoire en pourcentage dans la montagne
    
    if nb == 0:
        mounounit.place(x=25, y=175)
        return ((2*nb_d)/3)
    else : 
        if (nb_d/nb)*100 < 45:
            #defeat the demon and half your units continues on to the demon king castle
            mouv.place(x=25, y=175)
            return (nb-nb_d)
        elif (nb_d/nb)*100 <= 80 and (nb_d/nb)*100 >= 45:
            #tie, both garrisons lose
            moutie.place(x=25, y=175)
            return 0
        elif (nb_d/nb)*100 > 80:
            #your loss, half the d units continues on to your castle
            moud.place(x=25, y=175)
            return (nb_d-nb)


def testFinalBattleYourCastle():
    global nb_castle, rest_units_d_beach, rest_units_d_field, rest_units_d_forest, rest_units_d_mountain, nb_castle_d
    rest_units_d = rest_units_d_beach + rest_units_d_field + rest_units_d_forest + rest_units_d_mountain
    
    if rest_units_d == 0:
        castle_nodunit.place(x=25, y=50)
        return True
    elif (rest_units_d/nb_castle)*100 < 65:
        castlev.place(x=25,y= 50)
        return True
    elif (rest_units_d/nb_castle)*100 >= 65:
        castled.place(x=25,y= 50)
        return False
    
        
def testFinalBattleDemonCastle():
    global nb_castle_d, rest_units_beach, rest_units_field, rest_units_forest, rest_units_mountain
    rest_units = rest_units_beach + rest_units_field+rest_units_forest+rest_units_mountain
    
    if rest_units == 0:
        castled_nounit.place(x=25, y=150)
        return False
    elif (rest_units/nb_castle_d)*100 < 65:
        castledd.place(x=25, y=150)
        return False
    elif (rest_units/nb_castle_d)*100 >= 65:
        castledv.place(x=25, y=150)
        return True
    


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
    beatie.place_forget()
    fietie.place_forget()
    fortie.place_forget()
    moutie.place_forget()
    beanounit.place_forget()
    fienounit.place_forget()
    fornounit.place_forget()
    mounounit.place_forget()
    finalresult_d = testFinalBattleYourCastle()
    if (finalresult_d == True):
        finalresult = testFinalBattleDemonCastle()
        if finalresult == True:
            graphic.delete(ALL)
            imagevictory = graphic.create_image(680, 400, image = victory)
        elif finalresult == False:
            graphic.delete(ALL)
            imagedraw = graphic.create_image(680, 400, image = draw)
    else:
        finalresult = testFinalBattleDemonCastle()
        if finalresult == True:
            graphic.delete(ALL)
            imagedraw = graphic.create_image(680, 400, image = draw)
        elif finalresult == False:
            graphic.delete(ALL)
            imagedefeat = graphic.create_image(680, 400, image = defeat)
        
def resultsBeach():
    global nb_beach, rest_units_d_beach, rest_units_beach
    nb_beach_d = 130
    if int(config_s[8]) == 500:
        nb_beach_d = 130
    elif int(config_s[8]) < 500:
        val_minus_d = (500-int(config_s[8])) / 5
        nb_beach_d = nb_beach_d - val_minus_d
    units_d = randint((nb_beach_d)/2, nb_beach_d)
    rest_units_b = testBeach(nb_beach, units_d)
    dispresults_beach.place_forget()
    if rest_units_b == (units_d - nb_beach):
        rest_units_d_beach = (units_d- nb_beach)
        
        rest_units_beach = 0
    elif rest_units_b == ((2*units_d)/3):
        rest_units_d_beach = ((2*units_d)/3)
        
        rest_units_beach = 0
    elif rest_units_b == (nb_beach - units_d):
        rest_units_beach = (nb_beach - units_d)
        
        rest_units_d_beach = 0
    elif rest_units_b == 0:
        rest_units_beach = 0
        rest_units_d_beach = 0
def resultsField():
    global nb_field, rest_units_d_field, rest_units_field
    nb_field_d = 150
    if int(config_s[8]) == 500:
        nb_field_d = 150
    elif int(config_s[8]) < 500:
        val_minus_d = (500-int(config_s[8])) / 5
        nb_field_d = nb_field_d - val_minus_d
    units_d = randint((nb_field_d)/2, nb_field_d)
    rest_units_fi = testField(nb_field, units_d)
    dispresults_field.place_forget()
    if rest_units_fi == (units_d-nb_field):
        rest_units_d_field = (units_d- nb_field)
        
        rest_units_field = 0
    elif rest_units_fi == ((2*units_d)/3):
        rest_units_d_field = ((2*units_d)/3)
        
        rest_units_field = 0
    elif rest_units_fi == (nb_field -units_d):
        rest_units_field = (nb_field - units_d)
        
        rest_units_d_field = 0
    elif rest_units_fi == 0:
        rest_units_field = 0
        rest_units_d_field = 0
def resultsForest():
    global nb_forest, rest_units_d_forest, rest_units_forest
    nb_forest_d = 70
    if int(config_s[8]) == 500:
        nb_forest_d = 70
    elif int(config_s[8]) < 500:
        val_minus_d = (500-int(config_s[8])) / 5
        nb_forest_d = nb_forest_d - val_minus_d
    units_d = randint((nb_forest_d)/2, nb_forest_d)
    rest_units_fo = testForest(nb_forest, units_d)
    dispresults_forest.place_forget()
    if rest_units_fo == (units_d - nb_forest):
        rest_units_d_forest = (units_d- nb_forest)
        
        rest_units_forest = 0
    elif rest_units_fo == ((2*units_d)/3):
        rest_units_d_forest = ((2*units_d)/3)
        
        rest_units_forest = 0
    elif rest_units_fo == (nb_forest - units_d):
        rest_units_forest = (nb_forest - units_d)
        
        rest_units_d_forest = 0
    elif rest_units_fo == 0:
        rest_units_forest = 0
        rest_units_d_forest = 0
def resultsMountains():
    global nb_mountain, rest_units_d_mountain, rest_units_mountain
    nb_mountain_d = 20
    
    if int(config_s[8]) == 500:
        nb_mountain_d = 20
        units_d = randint((nb_mountain_d)/2, nb_mountain_d)
    elif int(config_s[8]) < 500 and int(config_s[8]) > 350:
        val_minus_d = (500-int(config_s[8])) / 5
        nb_mountain_d = nb_mountain_d - val_minus_d
        units_d = randint((nb_mountain_d)/2, nb_mountain_d)
    elif int(config_s[8]) <= 350:
        units_d = 0
    
    rest_units_m = testMountain(nb_mountain, units_d)
    dispresults_mountain.place_forget()
    if rest_units_m == (units_d-nb_mountain):
        rest_units_d_mountain = (units_d-nb_mountain)
        
        rest_units_mountain = 0
    elif rest_units_m == ((2*units_d)/3):
        rest_units_d_mountain = ((2*units_d)/3)
        
        rest_units_mountain = 0
    elif rest_units_m == (nb_mountain - units_d):
        rest_units_d_mountain = 0
        rest_units_mountain = (nb_mountain - units_d)
        
        
    elif rest_units_m == 0:
        rest_units_mountain = 0
        rest_units_d_mountain = 0
        
def fctGameSetup():
    global nb_castle, nb_beach, nb_field, nb_forest, nb_mountain, nb_castle_d
    graphic.delete(ALL)
    imagebattle = graphic.create_image(680, 400, image = battle)
     
    nb_castle = scalecastle.get()
    nb_beach = scalebeach.get()
    nb_field = scalefield.get()
    nb_forest = scaleforest.get()
    nb_mountain = scalemountain.get()
    #troupes ennemies: 130, 130, 150, 70, 20
    button_game.place_forget()

    nb_castle_d = 130
    
    if int(config_s[8]) == 500:
        nb_castle_d = 130
        
    elif int(config_s[8]) < 500:
        val_minus_d = (500-int(config_s[8])) / 5
        nb_castle_d = nb_castle_d - val_minus_d
        
      
        
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
    
    

    dispresults_beach.place(x= 500, y= 25)
    dispresults_field.place(x= 500, y= 75)
    dispresults_forest.place(x= 500, y= 125)
    dispresults_mountain.place(x= 500, y= 175)
    finish_btn.place(x=10, y=650)

def openUrl():
    webbrowser.open_new(website_url)

#PARTIE GRAPHIQUE


root = Tk()
root.geometry("1280x720")
root.title("There is no War")
root.overrideredirect(True)
root.configure(background = "#8e9dac")

graphic = Canvas(root, width = "1324", height = "736", bg = "white", bd = "10",highlightbackground= "#8e9dac", highlightthickness = "10", relief = "ridge")
graphic.place(x=20, y=20)


dialog_outline = LabelFrame(root, height = "756", width = "516", bg ="#69503a")
dialog_outline.place(x=1384, y=20)


answer_outline = LabelFrame(root, height = "264", width = "1344", bg="#69503a")
answer_outline.place(x=20, y=796)


options_outline = LabelFrame(root, height = "264", width = "516", bg= "#69503a")
options_outline.place(x=1384, y=796)


button_quit = Button(root,  text = "Quit the Game",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = root.destroy)
button_quit.place(x=1409, y=1006)

button_new = Button(root, text = "New Game",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = newStart)
button_new.place(x=1409, y=946)


button_save = Button(root, text = "Save Game",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = saveConfig)
button_save.place(x=1409, y=886)


start_btn = Button(root, text="Start Game",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = dispImg)
start_btn.place(x=1409, y=826)

website = Button(root, text="For more info...",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = openUrl)
website.place(x=1609, y=1006)

"""objets concernant le texte"""


scrollbar = Scrollbar(dialog_outline,bg  ="#eaecb9")
scrollbar.place(x=485, y=0)

dialog = Text(dialog_outline, width="55",bg  ="#eaecb9", yscrollcommand= scrollbar.set, relief = "ridge", highlightbackground = "#eaecb9", bd="10")
dialog.place(x=10,y=10)

scrollbar.config(command= dialog.yview)

go_btn = Button(dialog_outline, text="Let's go !", highlightthickness = "10", relief = "ridge", command = startGame,bg  ="#eaecb9")

nextLine_btn = Button(dialog_outline, text="Next line", highlightthickness = "10", relief = "ridge", command = nextLine,bg  ="#eaecb9")

nextPart_btn = Button(dialog_outline, text="Next Part", highlightthickness = "10", relief = "ridge", command = fctSetup,bg  ="#eaecb9")

well_btn = Button(dialog_outline, text="Well...", highlightthickness = "10", relief = "ridge", command = changeImg,bg  ="#eaecb9")

newstart_btn = Button(dialog_outline, text = "New Start", highlightthickness = "10", relief = "ridge", command = newStart,bg  ="#eaecb9")

""" objets concernant les réponses"""


answerA = Button(answer_outline, text= (first_sug), highlightthickness = "1", relief = "ridge",bg  ="#eaecb9", command = chooseA)
#answerA.place(x=25, y=25)

answerB = Button(answer_outline, text=(second_sug), highlightthickness = "1", relief = "ridge",bg  ="#eaecb9", command = chooseB)
#answerB.place(x=25, y=75)

answerC = Button(answer_outline, text=(third_sug), highlightthickness = "1", relief = "ridge",bg  ="#eaecb9", command = chooseC)
#answerC.place(x=25, y=125)

answerD = Button(answer_outline, text=(fourth_sug), highlightthickness = "1", relief = "ridge",bg  ="#eaecb9", command = chooseD)
#answerD.place(x=25, y=175)


    #OBJETS POUR SECOND JEU                           LIMITES: 40 mou, 90 fo, 170 fie, 150 bea, 150 cas



game_outline = LabelFrame(root, height = "264", width = "1344", bg= "#69503a")

button_game = Button(root, text = "Start the Battle !",bg  ="#eaecb9", highlightthickness = "10", relief = "ridge", command = fctGameSetup)

label_castle = Label(root, text = "Units in the castle :", highlightbackground = "#eaecb9", bd="10", relief = "ridge",bg  ="#eaecb9")  #Colonnes des differents terrains
label_beach = Label(root, text = "Units on the beach :", highlightbackground = "#eaecb9", bd="10", relief = "ridge",bg  ="#eaecb9")
label_field = Label(root, text = "Units on the field :", highlightbackground = "#eaecb9", bd="10", relief = "ridge",bg  ="#eaecb9")
label_forest = Label(root, text = "Units in the forest :", highlightbackground = "#eaecb9", bd="10", relief = "ridge",bg  ="#eaecb9")
label_mountain = Label(root, text = "Units in the moutains :", highlightbackground = "#eaecb9", bd="10", relief = "ridge",bg  ="#eaecb9")


varcastle = DoubleVar()
varbeach = DoubleVar()
varfield = DoubleVar()
varforest = DoubleVar()
varmountain = DoubleVar()


scalecastle = Scale(root, width = "50", from_ = 10, to = 150, highlightbackground = "#eaecb9", relief = "ridge", bd="10", variable = varcastle,bg  ="#eaecb9",troughcolor = "#e7dfb1")
scalebeach = Scale(root, width = "50", from_ = 0, to = 150, highlightbackground = "#eaecb9", relief = "ridge", bd="10", variable = varbeach,bg  ="#eaecb9",troughcolor = "#e7dfb1")
scalefield = Scale(root, width = "50", from_ = 0, to = 170, highlightbackground = "#eaecb9", relief = "ridge", bd="10", variable = varfield,bg  ="#eaecb9",troughcolor = "#e7dfb1")
scaleforest = Scale(root, width = "50", from_ = 0, to = 90, highlightbackground = "#eaecb9", relief = "ridge", bd="10", variable = varforest,bg  ="#eaecb9",troughcolor = "#e7dfb1")
scalemountain = Scale(root, width = "50", from_ = 0, to = 40, highlightbackground = "#eaecb9", relief = "ridge", bd="10", variable = varmountain,bg  ="#eaecb9",troughcolor = "#e7dfb1")




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

dispresults_beach = Button(game_outline, text = "See the results of the battle at the beach.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9", command = resultsBeach )
dispresults_field = Button(game_outline, text = "See the results of the battle at the field.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9", command = resultsField)
dispresults_forest = Button(game_outline, text = "See the results of the battle at the forest.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9", command = resultsForest)
dispresults_mountain = Button(game_outline, text = "See the results of the battle at the mountain.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9", command = resultsMountains)

beav = Label(game_outline, text ="Our units have won the battle on the beach battlefield !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
beatie = Label(game_outline, text="Our units and the Demon King's army units have destroyed each other on the beach battlefield !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
bead = Label(game_outline, text ="Our units have lost the battle on the beach battlefield !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
beanounit = Label(game_outline, text ="There was no units on the beach battlefield ! The Demon Army passed through !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fiev = Label(game_outline, text ="We won the battle in the meadows !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fietie = Label(game_outline, text="The enemy and us have destroyed each other in the meadows !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fied = Label(game_outline, text ="We lost the battle in the meadows !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fienounit = Label(game_outline, text ="There was no units in the meadows ! The Demon Army passed through !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
forv = Label(game_outline, text ="We are victorious in the forest !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fortie = Label(game_outline, text="We annihilated each other in the forest !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
ford = Label(game_outline, text ="We have been defeated in the forest !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
fornounit = Label(game_outline, text ="There was no units in the forest ! The Demon Army passed through !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
mouv = Label(game_outline, text ="The mountain's units won !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
moutie = Label(game_outline, text="The mountain's units have perished while destroying the demons' units !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
moud = Label(game_outline, text ="The mountain's units failed !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
mounounit = Label(game_outline, text ="There was no units in the mountain ! The Demon Army passed through !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")

castledv = Label(game_outline, text="You broke inside the Demon King's Castle and killed him !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
castledd = Label(game_outline, text="You broke inside the Demon King's Castle but you were wiped out by the Demons !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
castlev = Label(game_outline, text="Some Demons broke inside your castle, but the soldiers eliminated them !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
castled = Label(game_outline, text="Some Demons broke inside your castle and killed everyone !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")

finish_btn = Button(dialog_outline, text = "Let's finish this battle !", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9", command = FinalBattle)

castled_nounit = Label(game_outline, text="You have no more units left on the battlefields, you couldn't infiltrate the Demon King's castle.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")
castle_nodunit = Label(game_outline, text="There was no more demon's units left on the battlefields, they couldn't infiltrate your castle.", highlightthickness = "10", relief = "ridge",bg  ="#eaecb9")

root.mainloop()










         
