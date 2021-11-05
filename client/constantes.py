#
#       Tous les paramètres
#

BaseDuTerrain = 10      # Nombre de cases dans le terrain (hauteur)
HauteurDuTerrain = 12   # Nombre de cases dans le terrain (base)

TaillePiece = 50

Marge = 10

Largeur = 7 + BaseDuTerrain * TaillePiece
Hauteur = 12 + (HauteurDuTerrain + 4) * TaillePiece

docCouleur = { 1: "firebrick3",
               2: "PaleTurquoise3",
               3: "lightgreen",
               4: "LightPink2",
               5: "gold",
               6: "darkorange",
               7: "orchid3"}

docRotation = {1: [[[1,1,1,1]],[[1],[1],[1],[1]]],
               2: [[[2,2],[2,2]]],
               3: [[[0,3],[3,3],[0,3]],[[3,3,3],[0,3,0]],[[3,0],[3,3],[3,0]],[[0,3,0],[3,3,3]]],
               4 :[[[4,4,0],[0,4,4]],[[0,4],[4,4],[4,0]]],
               5: [[[0,5,5],[5,5,0]],[[5,0],[5,5],[0,5]]],
               6: [[[0,0,6],[6,6,6]],[[6,6],[0,6],[0,6]],[[6,6,6],[6,0,0]],[[6,0],[6,0],[6,6]]],
               7: [[[7,7,7],[0,0,7]],[[7,7],[7,0],[7,0]],[[7,0,0],[7,7,7]],[[0,7],[0,7],[7,7]]],
               8: [[[8,8],[0,8],[8,0]]]}

fondCouleur = "gray25"
arrierePlanCouleur = "gray10"
ecritureCouleur = "white"
