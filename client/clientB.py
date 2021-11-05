import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

from tkinter import *
from tkinter.messagebox import *

from terrain import *
from tkinter import *
from pieces import *
from display import *
from constantes import *

def ToucheAppuie(evt): #       Gestion clavier
        piece= c.pieces[0]
        if piece == None or piece.position == -1:
                return None
        taille= len(piece.physique)

        if evt.keysym == "Left" or evt.keysym == "q" or evt.keysym == "Q":
                if piece.position != 0:
                        c.deplacer(-1)
        if evt.keysym == "Right" or evt.keysym == "d" or evt.keysym == "D" :
                if piece.position+taille != BaseDuTerrain:
                        c.deplacer(1)
        if evt.keysym == "Up" or evt.keysym == "z" or evt.keysym == "Z":
                c.rotation(1)
        if evt.keysym == "s" or evt.keysym == "S":
                c.rotation(-1)
        if evt.keysym == "a" or evt.keysym == "A":
                c.echange()
        if evt.keysym == "Down" or evt.keysym == "space":
                c.jouer()

#
#          - - -   C L A S S    C L I E N T   - - -
#
class Client(ConnectionListener):
        #
        #        - - Gestion de la Connexion - -
        #
        def __init__(self, host, port):
                self.Connect((host, port))
                self.pseudo="0"
                connection.Send({"action": "newPseudo", "pseudo": "0"})
                self.Loop()
                #
                self.etat = 0
                #
                # 0 = Pas de Partie en cours
                # 1 = Tour en cours
                # 2 = Tour en attente
                # 5 = Tour joué (en attente de l'annimation)
                #
                self.temps = 0
                self.horloge = 0
                #
                self.defaites = 0
                self.vitoires = 0
                self.points = 0
                #
                self.terrain = None         #Attribué après connexion
                self.pieces= [None,None]    #Attribué après connexion

        def Network_connected(self, data):
                print("\n Vous êtes désormais connecté au serveur ! \n")

        def Network_accepterPseudo(self, data):
                self.pseudo = data["pseudo"]
                demandeFrame.destroy() #       On détruit les elements de la fenetre de connexion
                #
                tetrisWin.bind("<Key>",ToucheAppuie)
                self.display = Display(self, tetrisWin) #       On créer un display pour la gestion de l'affichage de la nouvelle fenêtre
                self.display.afficherTetris()
                #
                T = Terrain(self.display.plateau, BaseDuTerrain, HauteurDuTerrain)
                c.terrain = T
                #
                showinfo("Connexion établie", "Vous êtes désormais connecté(e) ! \n Votre pseudo est : {0}".format(self.pseudo))

        def Network_refusPseudo(self, data):
                showwarning("Pseudo invalide", "Le pseudo est déjà utilisé, merci de recommencer.")
                Pseudo.set("")

        def Network_disconnected(self, data):
                self.pseudo = ""
                print("\n La connexion au serveur a été interrompue. \n")
                exit()

        def Network_startLoop(self,data):
                while self.pseudo != "":
                        tetrisWin.update()
                        self.Loop()
                exit()

        def Loop(self):
                connection.Pump()
                self.Pump()

        def quit(self):
                self.pseudo = ""
                tetrisWin.destroy()

        def Network_error(self, data):
                print('Error:', data['error'][1])
                connection.Close()


        #
        #        - - Gestion des Demandes/Invitations de partie - -
        #
        def demandePartie(self, pseudoJoueur2): # Envoie d'une demande de Partie
                if self.pseudo ==  pseudoJoueur2:
                        showwarning("L'opération n'a pas pu aboutir ", "Vous ne pouvez pas faire de partie seul(e)...")
                        return None
                self.Send({"action": "demandePartie", "pseudoJoueur" : pseudoJoueur2})

        def Network_requetePartie(self, data):  # Réception d'une demande de Partie
                if askyesno("Requête de partie", "{0} défie en duel, acceptez vous ?  (Il a {1} Points, vous en avez {2})".format(data["pseudo"],data["pointsB"],data["pointsA"])) == True:
                        self.Send({"action":"partieAccepte", "pseudoB": data["pseudo"]})
                else:
                        self.Send({"action":"partieRefus", "pseudoB": data["pseudo"]})

        def Network_forcePartie(self, data):    # Reception d'une partie forcée
                showinfo("Requête de partie", "{0} vous a défié en duel, vous êtes obligé d'accepter. La partie démarre quand vous acceptez.".format(data["pseudo"]))
                self.Send({"action":"partieAccepte", "pseudoB": data["pseudo"]})

        def Network_refusMessage(self, data):   # Message d'erreur/de refus
                showwarning("L'opération n'a pas pu aboutir ", data["raison"])


        #
        #        - - Gestion des Commandes de déplacement et des pièces - -
        #
        def deplacer(self, deplacement):    # Translation droite-gauche
                piece = self.pieces[0]
                piece.position+= deplacement
                name = piece.name
                physique = piece.physique
                position = piece.position
                #
                self.terrain.dessinerPiece(name, physique, position)
                self.Send({"action": "afficherPiece", "name": name, "physique" : physique, "position" : position})

        def rotation(self, deplacement):    # Rotation de la pièce
                piece = self.pieces[0]
                name = piece.name
                piece.rotate(deplacement)
                #
                physique = piece.physique
                position = piece.position
                #
                self.terrain.dessinerPiece(name, physique, position)
                self.Send({"action": "afficherPiece", "name": name, "physique" : physique, "position" : position})
                self.display.afficherPieces([p.physique for p in self.pieces],[p.name for p in self.pieces])

        def echange(self):  # Echange de la pièce actuelle avec celle sauvegardée
                piece = self.pieces[0]
                position = piece.position
                #
                (self.pieces[0],self.pieces[1]) = (self.pieces[1],self.pieces[0])
                #
                if self.pieces[1].position+len(self.pieces[0].physique) >= BaseDuTerrain:
                        self.pieces[0].position = BaseDuTerrain-len(self.pieces[0].physique)
                else:
                        self.pieces[0].position = self.pieces[1].position
                self.pieces[1].position = -1
                #
                piece = self.pieces[0]
                name = piece.name
                physique = piece.physique
                position = piece.position
                #
                self.terrain.dessinerPiece(name, physique, position)
                self.Send({"action": "afficherPiece", "name": name, "physique" : physique, "position" : position})
                self.display.afficherPieces([p.physique for p in self.pieces],[p.name for p in self.pieces])

        def Network_initialiserTerrain(self, data): # Création du terrain dans le canvas
                self.terrain.clear()
                self.terrain.initialiserTerrain()
                self.display.afficherPieces([p.physique for p in self.pieces],[p.name for p in self.pieces])

        def Network_afficherPiece(self, data):  # Afficher une certaine pièce dans la prévisualisation
                self.terrain.clearPiece()
                self.terrain.dessinerPiece(data["name"], data["physique"], data["position"])
                self.display.afficherPieces([p.physique for p in self.pieces],[p.name for p in self.pieces])

        def Network_donnerPiece(self, data):    # Donner une pièce au joueur
                self.pieces[data["nbEmplacement"]]=Piece(data["nbPiece"],self.terrain)

        def Network_clearPiece(self,data):  # Effacer les pièces actuelles dans la prévisualisation
                self.terrain.clearPiece()

        def Network_clearTerrain(self, data):   # Effacer le terrain acutel
                self.terrain.clear()

        def Network_nouvelleGrille(self, data): # Modification de la grille (pièce jouée, ligne cassée..)
                self.terrain.grille = data["grille"]

        def jouer(self):    # Action de jouer la pièce actuelle
                piece = c.pieces[0]
                physique = piece.physique
                terrain = self.terrain
                position = piece.position
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                (iTerrain,jTerrain) = terrain.size                       # Taille du terrain
                #
                if terrain.peutJouer(piece,0) == False:#       On ne peut pas jouer à la première position, alors la partie est finie
                        #
                        self.etat = -1
                        return None
                #
                check = 0
                while (check+len(piece.physique[0]) <jTerrain) and  (terrain.peutJouer(piece, check+1)==True):#       On regarde jusqu'où on peut jouer
                        check +=1
                #
                IDs = []
                self.Send({"action": "clearPiece"})
                self.terrain.clearPiece()
                aCasser= []
                for x in range(i):
                        for y in range(j):
                                if physique[x][y] != 0:
                                        terrain.grille[position+x][y+check] = piece.name
                                        id_ = terrain.canvas.create_rectangle(Marge+(x+position)*TaillePiece,  2*Marge+(4+y-j)*TaillePiece,  Marge+(x+position+1)*TaillePiece, 2*Marge+(5+y-j)*TaillePiece, fill = piece.couleur, outline="gray80")
                                        if y == j-1:
                                                IDs = IDs + [[id_,x+position,check+y]]
                                        else:
                                                IDs = [[id_,x+position,check+y]]+IDs
                                        if not check+y in aCasser:
                                                if self.terrain.checkLigne(check+y) == True:
                                                        aCasser=aCasser+[check+y]
                piece.position = -1
                self.animate(IDs, 2*Marge+(check+5.5)*TaillePiece, "Principal")
                self.Send({"action":"animate", "check": check, "physique": physique, "name" : piece.name, "position" : position})                        #
                aCasser.sort()
                for y in aCasser:
                        self.terrain.breakLigne(y)
                if len(aCasser) != 0 : self.Send({"action":"ligneCasse", "nombre" : len(aCasser)})
                self.Send({"action":"nouvelleGrille", "grille": self.terrain.grille})
                #
                self.etat = 5


        #
        #       - - Gestion Graphique et Animation - -
        #
        def Network_displayTetris(self, data):  # Permet d'afficher le message "Tetris" en haut à droite de l'écran
                self.etat = 0
                self.display.afficherTetris()
                self.display.tourDeJeu()

        def Network_startClock(self, data):  # Permet de démarer l'horloge en bas de terrain pour que les deux joueurs aient l'information sur le temps
                self.display.tourDeJeu()
                self.display.startClock(data["clock"], self.etat)

        def Network_animate(self, data):    # Relaie pour l'affichage de l'annimation de la pièce jouée par le joueur adverse
                physique = data["physique"]
                name = data["name"]
                check = data["check"]
                position = data["position"]
                terrain= self.terrain
                #
                terrain.clearPiece()
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                IDs=[]
                for x in range(i):
                        for y in range(j):
                                if physique[x][y] != 0:
                                        id_ = terrain.canvas.create_rectangle(Marge+(x+position)*TaillePiece,  2*Marge+(4+y-j)*TaillePiece,  Marge+(x+position+1)*TaillePiece, 2*Marge+(5+y-j)*TaillePiece, fill = docCouleur[name], outline="gray80")
                                        if y == j-1:
                                                IDs = IDs + [[id_,x+position,check+y]]
                                        else:
                                                IDs = [[id_,x+position,check+y]] +  IDs
                self.animate(IDs, 2*Marge+(check+6)*TaillePiece)

        def animate(self, IDs, ymax, option = None):
                # Fonction reponsable de l'animation des pièces. Si l'option est "Principal" on est sur
                #  le Client ayant effectué l'action, donc le tour se termine à la fin de l'exécution.
                plateau = self.terrain.canvas
                [x1, y1, x2, y2] = plateau.coords(IDs[-1][0])
                #
                if (y2 < ymax):
                        for ID in IDs:
                                [x1, y1, x2, y2] = plateau.coords(ID[0])
                                plateau.coords(ID[0], x1, y1+5, x2, y2+5)
                        plateau.update()
                        plateau.after(8, lambda: self.animate(IDs, ymax, option))
                #
                else:
                        for i in range(len(IDs)):
                                plateau.delete(IDs[i][0])
                        self.terrain.actualiserTerrain()
                        #
                        if option == "Principal":
                                self.Send({"action": "finDeTour"})
                                self.etat = 2



        #
        #       - - Gestion des Tours - -
        #
        def Network_nouveauTour(self, data):
                piece = self.pieces[0] #       Initialiser la piece puis l'afficher
                piece.position = 0
                name = piece.name
                physique = piece.physique
                position = piece.position
                #
                self.terrain.dessinerPiece(name, physique, position)
                self.Send({"action": "afficherPiece", "name": name, "physique" : physique, "position" : position})
                #       Lancer le temps
                self.etat = 1
                self.fctTemps()

        def fctTemps(self): # Cette fonction gère le temps de jeu (réel) du joueur.
                if self.etat == 0: # Partie annulée (autre joueur déconnecté..)
                        self.horloge = 0
                        return None
                #
                tempsTour = self.temps
                if self.horloge > tempsTour or self.etat == 5 : # Si le joueur a joué ou si le temps est écoulé
                        if self.etat != 5: # il n'a pas encore joué
                                self.jouer()
                        #
                        if self.etat !=-1: # il n'a pas perdu (après avoir été forcé de jouer)
                                self.horloge = 0
                                self.etat=2
                                return None
                #
                if self.etat == -1: #       Le joueur a perdu
                        # self.finPartie()
                        self.terrain.clearPiece()
                        self.Send({"action": "clearPiece"})
                        self.etat = 0
                        self.pieces[0].position = -1
                        self.Send({"action": "finDePartie"})
                        #
                        #       ENVOYER FIN DE PARTIE ICI <=========
                        #
                        return None
                #
                if self.etat != -1: #       Tout va bien, on augmente le temps
                        self.horloge += 100
                        self.terrain.canvas.after(100, self.fctTemps)



        #
        #       - - Autre - -
        #
        def Network_newEtat(self, data):
                self.etat = data["etat"]

        def Network_definirTemps(self, data): # Cette fonction permet de définir le temps max de jeu du joueur.
                self.temps= data["temps"]

        def Network_broadcast(self, data):  # Cette fonction est pour afficher un message en Info Box. (Envoyé depuis le broadcast du serveur)
                showinfo(data["title"], data["message"])

        def Network_afficherJoueur(self,data):
                # Cette fonction transmet la liste des joueurs connectés, leurs points, leur état,
                # au display afin qu'il puisse afficher une liste avec toutes ces informations.
                if self.pseudo == "0":
                        return None
                self.display.actualiserJoueurs(data["liste"])


#
#          - - -   L A N C E M E N T   - - -
#
if len(sys.argv) != 2:
    print("Please use: python3", sys.argv[0], "host:port")
    print("e.g., python3", sys.argv[0], "localhost:31425")
    exit()

host, port = sys.argv[1].split(":")

c = Client(host, int(port))


tetrisWin= Tk() # Fenêtre de demande du Pseudo
tetrisWin["bg"] = arrierePlanCouleur
tetrisWin.title("Tetris : Connexion")
#
tetrisWin.minsize(440,120)
tetrisWin.maxsize(440,120)
#
demandeFrame= Frame(tetrisWin, bg=arrierePlanCouleur)
Pseudo= StringVar()
Pseudo.set("")
#
def demanderPseudoServeur(Pseudo):
        #
        if Pseudo.get() == "0" or Pseudo.get() == "":
                showwarning("Pseudo invalide", "Le pseudo est invalide, merci de recommencer.")
                Pseudo.set("")
        elif len(Pseudo.get()) > 16:
                showwarning("Pseudo invalide", "Désolé, les pseudos ne peuvent pas dépasser 16 caratères.")
                Pseudo.set("")
        else:
                c.Send({"action":"checkPseudo","pseudo" : Pseudo.get()})
                c.Loop
#

fonte = tkFont.Font(family = "Bahnschrift SemiBold Condensed",size = 35)
Label1 = Label(demandeFrame, text = "- T E T R I S   V S -", font= fonte, bg=arrierePlanCouleur, fg=ecritureCouleur).grid(column = 0, row = 0, columnspan = 3, padx = 5, pady = 5)
#
fonte = tkFont.Font(family = "Arial",size = 12)
Label2 = Label(demandeFrame, text = "Rentrez votre pseudo : ", font= fonte, bg=arrierePlanCouleur, fg=ecritureCouleur).grid(column = 0, row = 1, padx = 10, pady = 5)
#
Champ = Entry(demandeFrame, textvariable= Pseudo, font= fonte,  bg ="gray80", fg="black")
Champ.focus_set()
Champ.grid(column = 1, row = 1, pady = 5)
#
fonte = tkFont.Font(family = "Arial",size = 11)
Bouton = Button(demandeFrame, text ="Valider", bg= fondCouleur, font = fonte,  fg=ecritureCouleur, command = lambda : demanderPseudoServeur(Pseudo) )
Bouton.grid(column = 2, row = 1, padx = 5, pady = 5)
#
demandeFrame.grid()

c.Loop()
