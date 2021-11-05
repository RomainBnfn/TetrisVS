import sys
from time import sleep, localtime

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

from tkinter import *
from tkinter.messagebox import *
from partie import *
from random import *

TempsDeBase = 8000

docRotation = {1: [[[1,1,1,1]],[[1],[1],[1],[1]]],
               2: [[[2,2],[2,2]]],
               3: [[[0,3],[3,3],[0,3]],[[3,3,3],[0,3,0]],[[3,0],[3,3],[3,0]],[[0,3,0],[3,3,3]]],
               4 :[[[4,4,0],[0,4,4]],[[0,4],[4,4],[4,0]]],
               5: [[[0,5,5],[5,5,0]],[[5,0],[5,5],[0,5]]],
               6: [[[0,0,6],[6,6,6]],[[6,6],[0,6],[0,6]],[[6,6,6],[6,0,0]],[[6,0],[6,0],[6,6]]],
               7: [[[7,7,7],[0,0,7]],[[7,7],[7,0],[7,0]],[[7,0,0],[7,7,7]],[[0,7],[0,7],[7,7]]]}

#
#       - - - C H A N N E L   C L I E N T / S E R V E U R  - - -
#
class ClientChannel(Channel):
        #
        #        - - Connexion/Deconnexion et demande de Pseudo - -
        #
        def __init__(self, *args, **kwargs):
                #
                self.pseudo = "0"
                Channel.__init__(self, *args, **kwargs)
                #
                self.piece0=[None,None, None] # Name, Physique, Position
                self.partie = None
                self.temps = TempsDeBase
                self.etat = 0   # Attention, le self.etat n'est pas forcément le même que self._server.player(self),
                #   en effet, lors d'une demande de partie, le self._server.players(self) vaut 3, et le self.etat a
                #   pour valeur le channel du second joueur concerné.
                #
                self.Send({"action": "definirTemps", "temps" : TempsDeBase})
                self.Send({"action":"startLoop"})

        def Network_newPseudo(self, data):
                self.pseudo = data["pseudo"]

        def Network_checkPseudo(self, data):    # Permet de ne pas avoir plusieurs joueurs ayant le même pseudo.
                if etat_Insc==0:
                        self.Send({"action": "refusMessage", "raison" : "Les inscriptions sont closes !"})
                        return None

                if not data["pseudo"] in [p.pseudo for p in self._server.players]:
                        self.pseudo = data["pseudo"]
                        self.Send({"action": "accepterPseudo","pseudo": self.pseudo})
                        self._server.points[self] = 1000
                        self._server.AddPlayer(self)
                        self._server.actualiserJoueur()
                else:
                        self.Send({"action": "refusPseudo"})

        def Close(self):
                if self.pseudo == "0":
                        return None
                if self._server.players[self] == 3:
                        (self.etat).etat = 0
                        self._server.players[self.etat] = 0
                        self._server.actualiserJoueur()
                        self._server.DelPlayer(self)
                        return None
                if self._server.players[self] != 0:
                        if self.partie.joueurActuel() != self: self.partie.tour += 1
                        self.Network_finDePartie(None)
                self._server.DelPlayer(self)



        #
        #       - - Gestion des demandes/refus de Partie - -
        #
        def Network_demandePartie(self, data):
                #
                joueurA = self
                joueurB = [p for p in self._server.players if p.pseudo == data["pseudoJoueur"]][0]
                #
                if etat_Tournois == 0:
                        self.Send({"action": "refusMessage", "raison" : "Le tournois est vérouillé."})
                        return None
                if joueurB.pseudo == None:
                        self.Send({"action": "refusMessage", "raison" : "Le joueur s'est déconnecté."})
                        return None
                if self._server.players[self] == 3:
                        self.Send({"action": "refusMessage", "raison" : "Vous avez déjà une demande en attente..".format(data["pseudoJoueur"])})
                        return None
                if self._server.players[joueurB] != 0:
                        self.Send({"action": "refusMessage", "raison" : "{0} est déjà en partie!".format(data["pseudoJoueur"])})
                        return None
                if self._server.players[joueurB] == 3:
                        self.Send({"action": "refusMessage", "raison" : "{0} a déjà une demande en cours!".format(data["pseudoJoueur"])})
                        return None
                if data["pseudoJoueur"] == "0":
                        self.Send({"action": "refusMessage", "raison" : "ERREUR : Le joueur n'est pas connecté."})
                        return None
                if abs(self._server.points[joueurA]-self._server.points[joueurB]) > 300:
                        self.Send({"action": "refusMessage", "raison" : "La différence de points est trop importante. Vous avez {0} points de différence sur les 300 autorisés.".format(abs(self._server.points[joueurA]-self._server.points[joueurB]))})
                        return None
                #       - OK -
                self.etat = joueurB
                joueurB.etat = self
                #
                self._server.players[self] = 3
                self._server.players[joueurB] = 3
                self._server.actualiserJoueur()
                #
                if abs(self._server.points[joueurA]-self._server.points[joueurB]) < 200:
                        #le match est forcé, mais on envoie un message au joueur adversaire pour ne pas qu'il soit prit au dépourvu.
                        joueurB.Send({"action":"forcePartie", "pseudo": joueurB.pseudo})
                        return None
                joueurB.Send({"action": "requetePartie", "pseudo" : joueurA.pseudo, "pointsA": self._server.points[joueurA], "pointsB": self._server.points[joueurB]})

        def Network_partieRefus(self, data):
                if self.etat == 0 or self.etat == None: # Si jamais le deuxième joueur s'est déconnecté durant le temps de la demande.
                        self._server.players[self] = 0
                        self._server.actualiserJoueur()
                        return None
                #
                joueurB = self.etat
                self.etat = 0
                joueurB.etat = 0
                #
                self._server.players[self] = 0
                self._server.players[joueurB] = 0
                self._server.actualiserJoueur()
                joueurB.Send({"action": "refusMessage", "raison" : "{0} a refusé votre demande de partie!".format(self.pseudo)})

        def Network_partieAccepte(self, data):
                if self.etat == 0 or self.etat == None: # Si jamais le deuxième joueur s'est déconnecté durant le temps de l'acceptation d'un match forcé.
                        self._server.players[self] = 0
                        self._server.actualiserJoueur()
                        return None
                #
                joueurB = self.etat
                if joueurB == 0 or joueurB == None:
                        self.Send({"action": "refusMessage", "raison" : "Le joueur s'est déconnecté."})
                        return None
                if etat_Tournois == 0:
                        self.Send({"action": "refusMessage", "raison" : "Le tournois est vérouillé."})
                        self.etat.etat = 0
                        self._server.players[self.etat]=0
                        self.etat = 0
                        self._server.players[self] = 0
                        self._server.actualiserJoueur()
                        return None
                if self._server.players[joueurB] != 3:
                        self.Send({"action": "refusMessage", "raison" : "{0} est déjà en partie!".format(data["pseudoB"])})
                        return None
                if self._server.players[self] != 3:
                        self.Send({"action": "refusMessage", "raison" : "Vous êtes déjà en partie !"})
                        return None
                #
                if randint(0, 1) == 0:
                        self._server.creerPartie([self, joueurB])
                else:
                        self._server.creerPartie([joueurB,self])



        #
        #       - - Partie Relaie, transmission du message au joueur adverse - -
        #
        def Network_animate(self, data): #       On affiche à l'autre joueur
                [p.Send({"action" : "animate", "name": data["name"], "physique": data["physique"], "check": data["check"], "position" : data["position"]}) for p in self.partie.joueurs if p.pseudo != self.pseudo]

        def Network_afficherPiece(self, data): #       On affiche à l'autre joueur
                [p.Send({"action" : "afficherPiece", "name": data["name"], "physique": data["physique"], "position" : data["position"]}) for p in self.partie.joueurs if p.pseudo != self.pseudo]

        def Network_clearPiece(self, data): #       On affiche à l'autre joueur
                [p.Send({"action" : "clearPiece"}) for p in self.partie.joueurs if p.pseudo != self.pseudo]

        def Network_nouvelleGrille(self, data): #       On affiche à l'autre joueur
                [p.Send({"action": "nouvelleGrille", "grille" : data["grille"]})  for p in self.partie.joueurs if p.pseudo != self.pseudo]

        def Network_finDeTour(self, data):
                self._server.finDeTour(self)

        def Network_finDePartie(self, data):
                self.partie.finPartie()
                [p.Send({"action":"displayTetris"}) for p in self.partie.joueurs]
                [p.Send({"action":"definirTemps", "temps" : TempsDeBase}) for p in self.partie.joueurs]
                self._server.actualiserJoueur()

        def Network_ligneCasse(self, data):
                joueurB=[p for p in self.partie.joueurs if p.pseudo != self.pseudo][0]
                for i in range(data["nombre"]):
                        joueurB.temps = (joueurB.temps-1500)*0.70+1500
                joueurB.Send({"action":"definirTemps", "temps" : joueurB.temps})



#
#       - - - S E R V E U R - - -
#
class MyServer(Server):
        channelClass = ClientChannel
        #
        #       - - Connexion - -
        #
        def __init__(self, *args, **kwargs):
                Server.__init__(self, *args, **kwargs)
                self.players = {}   # La liste des joueurs, et de leurs états.
                self.points = {}    # La liste des points de chaque joueur.
                print("\n Le serveur est lancé \n")

        def Connected(self, channel, addr):
                self.AddPlayer(channel)

        def AddPlayer(self, player):
                if player.pseudo != "0" : print("[+] Un joueur s'est connecté (" + player.pseudo + ")")
                self.players[player] = 0
                #
                # 0 = Pas de Partie
                # 1 = Tour en cours
                # 2 = Tour en attente
                # 3 = En attente de réponse à une demande de Partie
                #

        def DelPlayer(self, player):
                print("[-] Un joueur s'est déconnecté (" + player.pseudo + ")")
                del self.players[player]
                del self.points[player]
                self.actualiserJoueur()

        def Launch(self):
                while True:
                        self.Pump()
                        root_console.update()
                        sleep(0.001)


        #
        #       - - Envoie de la liste des joueurs - -
        #
        def envoyerAll(self, data):
                [p.Send(data) for p in self.players if p.pseudo != "0"]

        def actualiserJoueur(self):
                liste = []
                for p in self.players:
                        #liste = liste + [[p.pseudo, p.score]]
                        if p.pseudo != "0" : liste = liste + [[p.pseudo, self.points[p],self.players[p]]]
                self.envoyerAll({"action": "afficherJoueur", "liste": liste})



        #
        #       - - Gestion des Parties - -
        #
        def donnerPiece(self, joueur, nbPiece, nbEmplacement):
                joueur.Send({"action":"donnerPiece", "nbPiece": nbPiece, "nbEmplacement": nbEmplacement})
                joueur.piece0 = [nbPiece, docRotation[nbPiece]]

        def donnerPieces(self, joueurA, joueurB):
                for i in range(2):
                        self.donnerPiece(joueurA, randint(1, 7),i)
                        self.donnerPiece(joueurB, randint(1, 7),i)

        def creerPartie(self, joueurs):
                joueurs[0].temps = TempsDeBase
                joueurs[1].temps = TempsDeBase
                #
                joueurs[0].partie = Partie(joueurs[0], joueurs[1], self)
                joueurs[1].partie = joueurs[0].partie
                joueurs[0].partie.initialiserPartie()
                #
                self.players[joueurs[0]] = 1
                self.players[joueurs[1]] = 2
                #
                self.actualiserJoueur() #Les joueurs sont occupés

        def finDeTour(self, joueur):
                self.etat = 2
                joueur.partie.nouveauTour()

        def nouveauTour(self, joueur):
                joueur.Send({"action": "nouveauTour"})

        def clearTerrain(self, joueurs):
                [p.Send({"action": "clearTerrain"}) for p in joueurs]

        def broadcast(self, title, message):
                [p.Send({"action": "broadcast", "title": title, "message": message}) for p in self.players if p.pseudo != "0"]



# get command line argument of server, port
if len(sys.argv) != 2:
        print("Please use: python3", sys.argv[0], "host:port")
        print("e.g., python3", sys.argv[0], "localhost:31425")
        exit()

host, port = sys.argv[1].split(":")

#
#       Console du serveur : Permet l'activation // désactivation du tournois...
#

root_console = Tk()
root_console.title("Console du serveur")
root_console.minsize(470,120)
root_console.maxsize(470,120)

root_console["bg"] = "gray10"
frame= Frame(root_console, bg = "gray10", width = 300)
frame.grid(padx = 10, pady = 10)

etat_Insc=0
etat_Tournois=0
def etatIncriptions():
        global etat_Insc, ButInsc
        etat_Insc = 1 - etat_Insc
        if etat_Insc == 1 :
                ButInsc["text"] ="Inscriptions : Ouvertes"
                ButInsc["fg"] = "green"
        else :
                ButInsc["text"] ="Inscriptions : Vérouillées"
                ButInsc["fg"] = "firebrick3"
def etatTournois():
        global etat_Tournois, ButTour
        etat_Tournois = 1 - etat_Tournois
        if etat_Tournois == 1 :
                ButTour["text"] ="Tournois : Ouvert"
                ButTour["fg"] = "green"
        else :
                ButTour["text"] ="Tournois : Vérouillé"
                ButTour["fg"] = "firebrick3"

ButInsc = Button(frame, text = "Inscriptions : Vérouillées", fg="firebrick3", width = 20, command = etatIncriptions)
ButInsc.grid(row = 0, pady = 5)
ButTour = Button(frame, text = "Tournois : Vérouillé", fg="firebrick3", width = 20, command = etatTournois)
ButTour.grid(row = 0, column = 1, pady = 5)

broadcastTitle= StringVar()
broadcastTitle.set("")
broadcastMessage= StringVar()
broadcastMessage.set("")
#
Label2 = Label(frame, text = "Broadcast (Titre puis message) : ", bg="gray10", fg="white").grid(column = 0, row = 2, padx = 10, pady = 5)
#
ChampT = Entry(frame, textvariable= broadcastTitle,  bg ="gray80", fg="black", width = 15)
ChampT.focus_set()
ChampT.grid(column = 0, row = 3, pady = 5)
#
ChampM = Entry(frame, textvariable= broadcastMessage,  bg ="gray80", fg="black", width = 30)
ChampM.focus_set()
ChampM.grid(column = 1, row = 3, padx = 5)
#
def broadcast(title, message):
        s.broadcast(title, message)
        broadcastTitle.set("")
        broadcastMessage.set("")
#
Bouton = Button(frame, text ="Valider", bg= "gray25",  fg="gray90", command = lambda : broadcast(broadcastTitle.get(), broadcastMessage.get()))
Bouton.grid(column = 2, row = 3, padx = 5, pady = 5)
#

s = MyServer(localaddr=(host, int(port)))
s.Launch()
