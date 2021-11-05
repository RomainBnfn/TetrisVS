from random import *

class Partie():

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                               - - -   I N I T I L I S A T I O N   - - -                                                                           #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def __init__(self, joueurA, joueurB, server):

                self.joueurs = [joueurA,joueurB]
                self.server = server
                self.tour = 0

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                        - - -   G E S T I O N    D E B U T / F I N   P A R T I E  - - -                                                          #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def initialiserPartie(self):
                self.server.donnerPieces(self.joueurs[0],self.joueurs[1])#       On donne 2 pièces au joueur
                self.joueurs[0].Send({"action": "initialiserTerrain"})
                self.joueurs[1].Send({"action": "initialiserTerrain"})
                self.joueurs[0].Send({"action": "newEtat", "etat": 1})
                self.joueurs[1].Send({"action": "newEtat", "etat": 2})
                #
                self.nouveauTour()

        def finPartie(self):
                #
                #       Fin de partie
                #
                tick = (self.tour-1)%2
                perdant = self.joueurs[tick]
                gagnant = self.joueurs[1-tick]
                #
                perdant.Send({"action":"broadcast","title":"Tetis VS", "message":"Vous avez perdu.."})
                gagnant.Send({"action":"broadcast","title":"Tetis VS", "message":"Vous avez gagné !"})
                self.server.clearTerrain(self.joueurs)
                perdant.Send({"action": "newEtat", "etat": 0})
                gagnant.Send({"action": "newEtat", "etat": 0})
                #
                self.server.players[gagnant] = 0
                self.server.players[perdant] = 0
                #
                p = int(self.server.points[perdant])
                g = int(self.server.points[gagnant])
                #
                self.server.points[gagnant] = g + 100-(g-p)//3
                self.server.points[perdant] = p - 100+(g-p)//3

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                   - - -   G E S T I O N     D E S    T O U R S   - - -                                                               #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def joueurActuel(self):
                tick = self.tour%2
                return self.joueurs[1-tick]

        def nouveauTour(self):
                #
                tick = self.tour%2
                self.tour += 1
                tour = self.tour
                joueur = self.joueurs[tick]
                #
                tickprev = 1-tick
                self.server.donnerPiece(self.joueurs[tickprev], randint(1, 7),0)    #On
                self.server.players[self.joueurs[tickprev]] = 2
                self.joueurs[tickprev].etat = 2
                #
                #       Début du tour
                self.server.players[joueur] = 1
                joueur.etat = 1
                self.server.nouveauTour(joueur)
                [p.Send({"action":"startClock", "clock": joueur.temps}) for p in self.joueurs]
