from tkinter import *
import tkinter.font as tkFont
from tkinter.messagebox import *
from constantes import *

        # =====================================================================================#
        #                                                                                                                                                                                                #
        #                                            - - -   G E S T I O N   D E S   M E S S A G E S   - - -                                                             #
        #                                                                                                                                                                                                #
        # =====================================================================================#

class Display():

        #===========================================#
        #                                                                                                 #
        #              - - C r é a t i o n   d e   l a   f e n ê t r e  - -              #
        #                                                                                                 #
        #===========================================#

        def __init__(self, client, fenetre):

                self.client = client
                self.fenetre = fenetre
                #
                fenetre["bg"] = arrierePlanCouleur
                fenetre.title("Tetris VS")
                #
                fenetre.minsize(570+Largeur,110+Hauteur)
                fenetre.maxsize(570+Largeur,110+Hauteur)
                #
                frameAll= Frame(fenetre, bg = arrierePlanCouleur,bd = 0)
                frameAll.grid(pady=10, padx = 10, column=0, row = 0)
                #
                #               Zone de  jeu (Gauche)
                #
                frameJeu = Frame(frameAll, bg = arrierePlanCouleur,bd = 0)
                frameJeu.grid(column=0, padx = 10, row = 0)
                #
                plateau = Canvas(frameJeu, width = Largeur, height =Hauteur, bg = fondCouleur)
                plateau.grid(padx=0,pady=0,column=0)
                #
                #               Zone des commandes (Droite)
                #
                frameDroite= Frame(frameAll, bg = arrierePlanCouleur,bd = 0)
                frameDroite.grid(column=1, padx = 10, row = 0)
                #
                zonePrevisualisation= Canvas(frameDroite, width = 500, height = 255, bg = fondCouleur)
                zonePrevisualisation.grid(column=0, pady=10, row = 0)
                #
                zoneListeJoueurs= Canvas(frameDroite,  width = 500, height = 531, bg =fondCouleur)
                zoneListeJoueurs.grid(column=0, row = 1,pady=10 )
                #
                #               Zone du choix du thème (Bas droite)
                #
                #frameTheme = Frame(frameAll, bg = arrierePlanCouleur,bd = 0)
                #frameTheme.grid(column=1, padx = 10, row = 1)
                #listeThemes = ("Thème Sombre","Thème Blanc")
                #v = StringVar()
                #v.set(listeThemes[0])
                #optionTheme = OptionMenu(frameTheme, v, *listeThemes, command = lambda a: self.changementMode(a))
                #optionTheme.grid()
                #
                #               Zone des infos   (Bas, Gauche)
                #
                zoneInfos = Canvas(frameAll, bd= 2, height =60, bg =fondCouleur)
                zoneInfos.grid(column=0, row = 1, pady = 5)
                fonte = tkFont.Font(family = "Arial",size = 11)

                frameInfos = Frame(zoneInfos,  bg = fondCouleur, bd=0)
                displayInfos1 = Label(frameInfos,  bd=  0, font = fonte, text = "Pas de partie en cours..", bg = fondCouleur, fg=ecritureCouleur, width = 25)
                displayInfos1.grid(column = 0, padx =5, pady = 1, row = 0)

                displayInfos2 = Label(frameInfos, text = "0.0", font = fonte,bg = fondCouleur,  fg=ecritureCouleur)
                displayInfos2.grid(column = 0, row = 1,pady = 1 )
                frameInfos.grid(column = 0, row = 1, padx = 5, pady = 5)
                #
                self.plateau = plateau
                self.frameAll = frameAll
                self.frameJeu = frameJeu
                self.frameDroite = frameDroite
                self.zonePrevisualisation = zonePrevisualisation
                self.zoneListeJoueurs = zoneListeJoueurs
                #self.frameTheme = frameTheme
                self.zoneInfos = zoneInfos
                self.frameInfos = frameInfos
                self.displayInfos1 = displayInfos1
                self.displayInfos2 = displayInfos2

        #===========================================#
        #                                                                                                 #
        #              - - C r é a t i o n   d e   l a   f e n ê t r e  - -              #
        #                                                                                                 #
        #===========================================#

        #def changementMode(self, mode):
        #        global fondCouleur, arrierePlanCouleur, critureCouleur
        #        if mode == "Thème Sombre":
        #                fondCouleur = "gray25"
        #                arrierePlanCouleur = "gray10"
        #                ecritureCouleur = "white"
        #        if mode == "Thème Blanc":
        #                fondCouleur = "navajo white"
        #                arrierePlanCouleur = "PeachPuff3"
        #                ecritureCouleur = "saddle brown"

        #        self.fenetre["bg"]= arrierePlanCouleur
        #        self.frameAll["bg"]=  arrierePlanCouleur
        #        self.frameJeu["bg"]= arrierePlanCouleur
        #        self.plateau["bg"]= fondCouleur
        #        self.frameDroite["bg"]= arrierePlanCouleur
        #        self.zonePrevisualisation["bg"]= fondCouleur
        #        self.zoneListeJoueurs["bg"]= fondCouleur
        #        self.frameTheme["bg"] = fondCouleur
        #        self.zoneInfos["bg"]= fondCouleur
        #        self.frameInfos["bg"]= fondCouleur
        #        self.displayInfos1["bg"]= fondCouleur
        #        self.displayInfos1["fg"]= ecritureCouleur
        #        self.displayInfos2["bg"]= fondCouleur
        #        self.displayInfos2["fg"]= ecritureCouleur
        #        self.actualiserJoueurs(self.liste, fondCouleur, ecritureCouleur)
        #        self.afficherTetris()
        #        self.fenetre.update()

        def clearCanvas(self, canvas):
                for e in canvas.find_all():
                        canvas.delete(e)

        def afficherTetris(self):
                global ecritureCouleur
                colorE = ecritureCouleur
                canvas = self.zonePrevisualisation
                self.clearCanvas(canvas)
                fonte = tkFont.Font(family = "Bahnschrift SemiBold Condensed",size =35)
                canvas.create_text(252,80,text="- T E T R I S    V S -", font= fonte, fill = colorE)
                #
                fonte = tkFont.Font(family = "Calibri Light",size = 15, weight="bold")
                canvas.create_text(252,140,text="Bienvenue sur le jeu !", font= fonte, fill = colorE)
                #
                fonte = tkFont.Font(family = "Calibri Light",size = 15)
                canvas.create_text(252,170,text="Pour affronter un adversaire, envoyez lui une", font= fonte, fill = colorE)
                canvas.create_text(252,190,text="requète dans la liste ci-dessous.", font= fonte, fill = colorE)
                canvas.create_text(402,220,text="Bon jeu !", font= fonte, fill = colorE)
                canvas.update()

        def startClock(self, clock, etat):
                if self.client.etat == etat and clock >=0:
                        self.displayInfos2["text"]=(clock//100)/10
                        clock-=100
                        self.zonePrevisualisation.after(100, lambda clock=clock, etat=etat : self.startClock(clock, etat))
                else:
                        self.displayInfos2["text"]="0.0"
                self.displayInfos2.update()

        def tourDeJeu(self):
                if self.client.etat == 1:
                        self.displayInfos1["text"] = "C'est à vous de jouer."
                        self.displayInfos1["fg"] = "SpringGreen2"
                elif self.client.etat == 2:
                        self.displayInfos1["text"] = "C'est au tour de l'adversaire."
                        self.displayInfos1["fg"] = ecritureCouleur
                else:
                        self.displayInfos1["text"] = "Pas de partie en cours.."
                        self.displayInfos1["fg"] = ecritureCouleur


        def afficherPieces(self, physiques, names):
                canvas = self.zonePrevisualisation
                self.clearCanvas(canvas)
                for i in range(2):
                        (iP,jP) = (len(physiques[i]), len(physiques[i][0]))
                        for x in range(iP):
                                for y in range(jP):
                                        if physiques[i][x][y] != 0:
                                                Y = 4+y-jP
                                                canvas.create_rectangle(25+TaillePiece*x+TaillePiece*5*i,  38 +TaillePiece*Y,  25+TaillePiece*(x+1)+TaillePiece*5*i,  38 +TaillePiece*(Y+1), fill = docCouleur[names[i]], outline = "gray80")
                fonte = tkFont.Font(family = "Calibri Light",size = 13)
                canvas.create_text(75, 18,text="Pièce actuelle :", font= fonte, fill = ecritureCouleur)
                canvas.create_text(335, 18 ,text="Pièce sauvegardée :", font= fonte, fill = ecritureCouleur)

        def actualiserJoueurs(self, liste):
                global fondCouleur, ecritureCouleur
                canvas = self.zoneListeJoueurs
                #self.liste = liste
                self.clearCanvas(canvas)
                canvas.grid_propagate(0)
                #
                canvasDefil = Canvas(canvas,width = 480, height = 800 ,bg =fondCouleur, scrollregion=(0, 0, 1000, 1000))
                canvasDefil.config(bd=0, highlightcolor = fondCouleur , bg = fondCouleur,borderwidth=0, highlightthickness=0)
                canvasDefil.update()
                #
                scroll= Scrollbar(canvas, orient="vertical")
                scroll.config(command=canvasDefil.yview)

                canvasDefil.config(width=480,height=519)
                canvasDefil.config(yscrollcommand=scroll.set)
                canvasDefil.grid(column=0, row = 0, sticky="ew")
                canvasDefil.grid_propagate(0)

                frameDefil = Frame(canvasDefil, width=480, height = 780,bg=fondCouleur)
                interior_id= canvasDefil.create_window(0, 0, window=frameDefil, anchor=NW )
                def _configure_interior(event):
                    # update the scrollbars to match the size of the inner frame
                        size = (frameDefil.winfo_reqwidth(), frameDefil.winfo_reqheight())
                        canvasDefil.config(scrollregion="0 0 %s %s" % size)
                        if frameDefil.winfo_reqwidth() != canvasDefil.winfo_width():
                                # update the canvas's width to fit the inner frame
                                canvasDefil.config(width=frameDefil.winfo_reqwidth())
                frameDefil.bind('<Configure>', _configure_interior)

                def _configure_canvas(event):
                        if frameDefil.winfo_reqwidth() != canvasDefil.winfo_width():
                                # update the inner frame's width to fill the canvas
                                canvasDefil.itemconfigure(interior_id, width=canvasDefil.winfo_width())
                canvasDefil.bind('<Configure>', _configure_canvas)

                canvasDefil.grid(column=1, row=0, sticky="ns", padx = 20, pady = 7)
                scroll.grid(column=2, row = 0,  sticky="nse", padx = 12)
                #
                #
                liste = sorted(liste, key=lambda joueur: joueur[1])
                #
                joueurs = [i[0] for i in liste]
                points = [str(i[1])+" Points" for i in liste]
                etat = [i[2] for i in liste]
                #
                fonte = tkFont.Font(family = "Arial",size = 14)
                Label(frameDefil, text="Liste des joueurs:", bd=0, width=16, height= 2, font = fonte, bg=fondCouleur,fg=ecritureCouleur).grid(row=1, pady=2, column=1,sticky= "ew")
                fonte = tkFont.Font(family = "Arial",size = 13)
                #
                l = len(joueurs)
                for i in range(l):
                        if joueurs[i] == self.client.pseudo:
                                Label(frameDefil, text=joueurs[i], bd=0, width=16,font = fonte, bg=fondCouleur,fg="DeepSkyBlue2").grid(row=l-i+1, pady=2, column=1)
                                Label(frameDefil, text=points[i], bd=0, width=16,font = fonte, bg=fondCouleur,fg="DeepSkyBlue2").grid(row=l-i+1, pady=2, column=2)
                        else:
                                Label(frameDefil, text=joueurs[i], bd=0, width=16,font = fonte, bg=fondCouleur,fg=ecritureCouleur).grid(row=l-i+1, pady=2, column=1)
                                Label(frameDefil, text=points[i], bd=0, width=16,font = fonte, bg=fondCouleur,fg=ecritureCouleur).grid(row=l-i+1, pady=2, column=2)
                        #
                        if joueurs[i] == self.client.pseudo:
                                Button(frameDefil, text="Vous" ,width=10,bg='white',fg="DeepSkyBlue2").grid(row=l-i+1, padx = 2, pady=3, column=0)
                        elif etat[i] == 0:
                                Button(frameDefil, text="Inviter" ,width=10,bg='white',fg="green", command= lambda i=i: self.client.demandePartie(joueurs[i])).grid(row=l-i+1, padx = 2, pady=3, column=0)
                        elif etat[i] == 3:
                                Button(frameDefil, text="En attente" ,width=10,bg='white',fg="orange",command = lambda i=i: showwarning("Utilisateur indisponible", "Désolé, mais {0} a déjà reçu une invitation.".format(joueurs[i]))).grid(row=l-i+1, padx = 2, pady=3, column=0)
                        else:
                                Button(frameDefil, text="En partie" ,width=10,bg='white',fg="red",command = lambda i=i: showwarning("Utilisateur indisponible", "Désolé, mais {0} est occupé(e).".format(joueurs[i]))).grid(row=l-i+1, padx = 2, pady=3, column=0)
