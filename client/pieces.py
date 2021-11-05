from constantes import *

class Piece():

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                               - - -   I N I T I L I S A T I O N   - - -                                                                           #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def __init__(self,name, terrain):

                self.name = name
                #
                #       Numéro inscrit dans la grille pour trouver les couleurs
                #

                self.physique = docRotation[self.name][0]
                self.couleur = docCouleur[self.name]
                self.rotation = 0
                #
                #       Infos sur la pièces
                #        --> (Base,Hauteur) = (len(self.physique), len(self.physique[0]))
                #

                self.position = -1
                #
                # -1 : non en jeu
                # 0,1,2.. : position
                #

                self.terrain = terrain
                #


        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                                      - - -   G E S T I O N    D I V E R S E      - - -                                                                   #
        #                                                                                                                                                                                                #
        # =====================================================================================#

        def relancerPiece(self):
                self.name = randint(1, 7)
                self.physique = docRotation[self.name][0]
                self.couleur = docCouleur[self.name]
                self.rotation = 0
                self.position = -1
                return self

        def deplacer(self, direction):
                #
                #       On effectue directement le déplacement car les tests ont déjà été faits.
                #
                self.position += direction

        def rotate(self, direction):
                #
                #       On effectue directement la rotation car les tests ont déjà été faits.
                #
                terrain = self.terrain
                physique = self.physique
                (i,j) = (len(physique), len(physique[0]))       # Taille de la piece
                (iTerrain,jTerrain) = terrain.size                       # Taille du terrain
                finDeListe = len(docRotation[self.name])
                actuel = self.rotation
                #
                #       On prend le prochain élément dans la bibliothèque des rotations
                #
                self.rotation = (self.rotation+direction)%finDeListe
                self.physique = docRotation[self.name][self.rotation]
                #
                if len(self.physique)+self.position > iTerrain:
                        #
                        #       Si jamais la pièce sort du terrain avec la rotation, on la ramène dedans
                        #
                        self.position = iTerrain-len(self.physique)
