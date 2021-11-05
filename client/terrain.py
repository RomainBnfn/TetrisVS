from tkinter import *
import time
from constantes import *

class Terrain():

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                               - - -   I N I T I L I S A T I O N   - - -                                                                           #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def __init__(self, canvas, BaseDuTerrain, HauteurDuTerrain):

                self.size=(BaseDuTerrain,HauteurDuTerrain)
                #
                #       Taille de la grille de jeu (UNIQUEMENT : Pas au dessus)
                #               Exemple : (10,12)
                #

                self.grille = []
                for x in range(BaseDuTerrain):
                        L = []
                        for y in range(HauteurDuTerrain):
                                L.append(0)
                        self.grille .append(L)
                #
                #       Stoque les états du terrain
                #

                self.IdGrille = []
                for x in range(BaseDuTerrain):
                        L = []
                        for y in range(HauteurDuTerrain):
                                L.append(0)
                        self.IdGrille .append(L)
                #
                #       Stoque les ID de la grille
                #

                self.IdGrilleUp = []
                for x in range(BaseDuTerrain):
                        L = []
                        for y in range(4):
                                L.append(0)
                        self.IdGrilleUp.append(L)
                #
                #       Stoque les ID de la grille de prévisualisation (en haut)
                #

                self.canvas = canvas
                #
                #       Stoque le canevas de la fenêtre
                #
                #

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                   - - -   G E S T I O N   G R A P H I Q U E   - - -                                                                  #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def initialiserTerrain(self):
                #
                #       Initialiser la grille graphique : créer des rectangles pour faire une grille
                #
                (i,j) = self.size
                self.__init__(self.canvas, i, j)
                plateau = self.canvas
                #
                for x in range(i):
                        for y in range(4):
                                #
                                #       Créer un rectangle, puis son ID sauvegarder dans la grille ID
                                #
                                id_ = plateau.create_rectangle(Marge+x*TaillePiece,  Marge+(y)*TaillePiece, Marge+(x+1)*TaillePiece, Marge+(y+1)*TaillePiece, fill =fondCouleur, outline=fondCouleur)
                                plateau.addtag_above("grillePrevEtiq", id_)
                                self.IdGrilleUp[x][y] = id_
                #
                for x in range(i):
                         for y in range(j):
                                #
                                #       Idem pour le terrain de jeu eu dessous
                                #
                                id_ = plateau.create_rectangle(Marge+x*TaillePiece,  2*Marge+(y+4)*TaillePiece,  Marge+(x+1)*TaillePiece, 2*Marge+(y+5)*TaillePiece, fill =fondCouleur, outline="gray40")
                                plateau.addtag_above("grilleEtiq", id_)
                                self.IdGrille[x][y] = id_
                                #self.grille[x][y] = 0

                plateau.update()


        def clear(self):
                #
                #       Uniquement en fin de partie !
                #
               for e in self.canvas.find_all():
                        self.canvas.delete(e)


        def actualiserTerrain(self): #       Une simple acutalisation du terrain
                (i,j) = self.size
                plateau = self.canvas
                #
                for x in range(i):
                        for y in range(j):
                                #
                                #       Actualiser la grille en modifiant les états
                                #
                                if self.grille[x][y] != 0:
                                        plateau.itemconfigure(self.IdGrille[x][y], fill =docCouleur[self.grille[x][y]])
                                else:
                                        plateau.itemconfigure(self.IdGrille[x][y], fill =fondCouleur, outline="gray40")
                        plateau.update()
                 #


        def dessinerPiece(self,name, physique, position):
                #
                #       Cette fonction permet juste d'afficher une pièce en prévisualisation, pas sur le terrain.
                #
                plateau = self.canvas
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                (iTerrain,jTerrain) = self.size                       # Taille du terrain
                self.clearPiece()       #Clear les autres pièces
                for x in range(i):
                        for y in range(j):
                                if physique[x][y] != 0:
                                        X =x+position
                                        Y = 4+y-j
                                        plateau.coords(self.IdGrilleUp[X][Y],Marge+X*TaillePiece,  Marge+(Y)*TaillePiece, Marge+(X+1)*TaillePiece, Marge+(Y+1)*TaillePiece)
                                        plateau.itemconfigure(self.IdGrilleUp[X][Y], fill = docCouleur[name], outline="gray80")
                plateau.update()


        def clearPiece(self):
                global fondCouleur
                #
                #       Clear l'ancienne prévision
                #
                plateau = self.canvas
                (iTerrain,jTerrain) = self.size                       # Taille du terrain
                #
                for x in range(iTerrain):
                        for y in range(4):
                                plateau.coords(self.IdGrilleUp[x][y],5+Marge+x*TaillePiece,  5+Marge+(y)*TaillePiece, -5+Marge+(x+1)*TaillePiece, -5+Marge+(y+1)*TaillePiece)
                                plateau.itemconfigure(self.IdGrilleUp[x][y], fill =fondCouleur, outline=fondCouleur)
                                #Taille plus petite pour ne pas voir les bordures

        def prevision(self, piece):
                plateau = self.canvas
                physique = piece.physique
                position = piece.position
                terrain = self
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                (iTerrain,jTerrain) = self.size                       # Taille du terrain
                #
                if position == -1:
                        #
                        #       La pièce n'est pas en jeu
                        #
                        return None
                #
                self.actualiserTerrain()   #Pour effacer les anciennes previsualisations
                #
                if terrain.peutJouer(piece,0) == True:
                        #
                        #       Si on peut jouer
                        #
                        check = 0
                        while (check+j <jTerrain) and (self.peutJouer(piece, check+1)==True):
                                #
                                #       On regarde jusqu'où on peut jouer
                                #
                                check +=1
                        #
                        for x in range(i):
                                for y in range(j):
                                        if piece.physique[x][y] != 0:
                                                #
                                                #       Affichage
                                                #
                                                plateau.itemconfigure(terrain.IdGrille[x+position][y+check], fill ="gray")
                        plateau.update()


        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                   - - -   G E S T I O N    D E S   T E S T S   - - -                                                                  #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def checkLigne(self, ligne):
                (iTerrain,jTerrain) = self.size                       # Taille du terrain
                ligne = int(ligne)
                x = 0
                #
                while (x <iTerrain) and (self.grille[x][ligne] != 0) and (self.grille[x][ligne] == int(self.grille[x][ligne])):
                        if x == iTerrain-1:
                                return True
                        x+=1
                return False



        def breakLigne(self, ligne):
                (iTerrain,jTerrain) = self.size                       # Taille du terrain
                #
                for x in range(iTerrain):
                        #
                        #       On remplace la ligne cassée par les lignes au dessus, puis on rajoute une rangée de 0 au dessus
                        #
                        (self.grille[x]).pop(ligne)
                        self.grille[x]=[0]+self.grille[x]


        def peutJouer(self, piece, check):
                position = piece.position
                physique = piece.physique
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                #
                #       On regarde si la pièce peut renter en position (position, check)
                #
                for x in range(i):
                        for y in range(j):
                                if (physique[x][y] != 0) and (self.grille[position+x][y+check]!=0):
                                        return False
                return True
