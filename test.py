nombres = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 131072]

def afficher_grille(nombres):
    # Déterminer la largeur de la case en fonction du plus grand nombre
    largeur_case = len(str(max(nombres))) + 2  # Ajouter 2 pour les espaces de chaque côté

    # Créer la grille
    grille = ""
    for i in range(16):
        # Ajouter le nombre à la grille, centré dans la case
        grille += "{:^{}}".format(nombres[i], largeur_case)
        
        # Ajouter une nouvelle ligne après chaque 4 nombres
        if (i + 1) % 4 == 0:
            grille += "\n"
    
    print(grille)

afficher_grille(nombres)
