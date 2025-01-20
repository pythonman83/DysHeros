# Code complet du jeu en 2D pour pouvoir le transfomer en exécutable.

# Importation des bibliothèques nécessaires.

# pygame : pour créer des jeux et des animations.
# sys : pour interagir avec le système, comme quitter le programme proprement.
# random : pour choisir des valeurs aléatoires, utile pour les obstacles.
# os : pour gérer les chemins de fichiers.
# math : pour des opérations mathématiques complexes, comme les angles 
# (mise en place du design du compte à rebours avant de commencer le jeu).
# pyzt : pour gérer les fuseaux horaires.
# datetime : classe datetime du module datetime pour manipuler les dates et heures.
import pygame
import sys
import random
import os
import math
import pytz  
from datetime import datetime
import locale


# Fonction pour obtenir le chemin absolu vers une ressource
# Cela est utile pour rendre le jeu compatible avec PyInstaller qui permettra de transformer
# ce code en exécutable (.exe), 
# qui regroupe toutes les ressources ensemble
# "relative_path" est le chemin relatif de la ressource.

# Définition d'une fonction nommée 'resource_path' qui prend un argument 'relative_path'
def resource_path(relative_path):
    """Obtenir le chemin absolu vers la ressource, fonctionne pour PyInstaller."""

    # Essaie d'exécuter le bloc de code suivant
    try:
        # Si PyInstaller est utilisé, il définit une variable spéciale '_MEIPASS'
        # qui contient le chemin vers le répertoire temporaire où les fichiers sont extraits.
        base_path = sys._MEIPASS
    # Si une erreur de type 'AttributeError' se produit (c'est-à-dire que '_MEIPASS' n'existe pas)
    except AttributeError:
        # Alors, nous définissons 'base_path' comme le répertoire courant
        # 'os.path.abspath(".")' renvoie le chemin absolu du répertoire courant.
        # le "." représente le répertoire courant, 
        # c'est-à-dire le dossier dans lequel le script Python est exécuté.
        base_path = os.path.abspath(".")

    # Renvoie le chemin complet de la ressource en combinant 'base_path' et 'relative_path'
    # 'os.path.join(base_path, relative_path)' combine les deux chemins pour 
    # former un chemin complet.
    return os.path.join(base_path, relative_path)


# Initialiser tous les modules de pygame.
# Cette fonction doit être appelée avant d'utiliser d'autres fonctions de pygame.
pygame.init()

# Initialiser le module mixer de pygame.
# Le module mixer est utilisé pour jouer des sons et de la musique.
pygame.mixer.init()


# Chargement de l'icône pour la fenêtre.
# Utilisation de la fonction resource_path pour obtenir le chemin de l'icône de la fenêtre.
icon_image_path = resource_path("window_icone.png")  

# Chargement de l'image de l'icône en mémoire en utilisant le module pygame.
icon_image = pygame.image.load(icon_image_path)

# Définition de l'icône de la fenêtre avec l'image chargée.
pygame.display.set_icon(icon_image)


# Définition de la largeur et de la hauteur de la fenêtre de jeu.
# WIDTH = largeur de la fenêtre en pixels (800 pixels).
# HEIGHT = hauteur de la fenêtre en pixels (600 pixels).
WIDTH, HEIGHT = 800, 600

# Création de la fenêtre de jeu avec la taille précédente.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Définition du titre de la fenêtre de jeu.
pygame.display.set_caption("Jeu thérapeutique pour les troubles Dys (Dylexie, dyspraxie, dysgraphie)")

# Définition des couleurs utilisées dans le jeu en format RGB (Rouge, Vert, Bleu).
# BLACK = noir (0, 0, 0) = Fond d'écran final pour affichage des textes du jeu. 
# GREEN = vert (0, 255, 0) = Couleur du cercle autour du décompte d'avant jeu.
# WHITE = blanc (255, 255, 255) = Couleur de texte s"affichage des résultats et de l'horodatage.
# OR = couleur or (255, 215, 0) = Couleur de certains textes.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
OR = (255, 215, 0)


# Charge la musique de fond du jeu à partir du fichier spécifié.
# 'resource_path("aventure_son.mp3")' renvoie le chemin complet du fichier de musique
# 'pygame.mixer.music.load()' charge le fichier de musique pour qu'il puisse être joué.
pygame.mixer.music.load(resource_path("aventure_son.mp3"))

# Définit le volume de la musique à 0.09 (9% du volume maximal).
# 'pygame.mixer.music.set_volume(0.09)' ajuste le volume de la musique.
pygame.mixer.music.set_volume(0.09)

# Joue la musique en boucle.
# 'pygame.mixer.music.play(-1)' commence à jouer la musique et la répète indéfiniment.
# Le paramètre '-1' indique que la musique doit être jouée en boucle.
pygame.mixer.music.play(-1)



# Charge le son de fin de jeu à partir du fichier spécifié.
# 'resource_path("game_over.wav")' renvoie le chemin complet du fichier sonore.
# 'pygame.mixer.Sound()' crée un objet sonore à partir du fichier spécifié.
game_over_sound = pygame.mixer.Sound(resource_path("game_over.wav"))

# Charge le son de bonus collecté à partir du fichier spécifié.
# 'resource_path("bonus_collected.wav")' renvoie le chemin complet du fichier sonore.
# 'pygame.mixer.Sound()' crée un objet sonore à partir du fichier spécifié.
bonus_sound = pygame.mixer.Sound(resource_path("bonus_collected.wav"))

# Définit le volume du son de fin de jeu à 1.0 (100% du volume maximal).
# 'game_over_sound.set_volume(1.0)' ajuste le volume du son de fin de jeu.
game_over_sound.set_volume(1.0)

# Définit le volume du son de bonus collecté à 1.0 (100% du volume maximal).
# 'bonus_sound.set_volume(1.0)' ajuste le volume du son de bonus collecté.
bonus_sound.set_volume(1.0)


# Charge le fichier audio du son d'alerte pour le combat final.
# "pygame.mixer.Sound()" charge un fichier son pour le jouer plus tard : 
# ici, on utilise la fonction "resource_path()"
# pour obtenir le chemin du fichier "final_alert.wav" 
# (assurez-vous que le fichier se trouve dans le dossier correct).
final_alert_sound = pygame.mixer.Sound(resource_path("final_alert.wav"))

# Définit le volume du son chargé pour qu'il joue à pleine puissance (volume maximal).
# "final_alert_sound.set_volume(1.0)" ajuste le volume entre 
# 0.0 (silencieux) et 1.0 (volume maximal).
final_alert_sound.set_volume(1.0)  # Vous pouvez ajuster ce niveau selon vos préférences


# Chargement de l'image d'introduction.
# L'image est redimensionnée à une taille de 350 x 150 pixels.

# Charge l'image d'introduction à partir du fichier spécifié.
# 'resource_path("leo_hero.png")' renvoie le chemin complet du fichier image
# 'pygame.image.load()' charge l'image à partir du fichier spécifié
# 'convert_alpha()' convertit l'image en un format qui prend en charge la transparence.
intro_image = pygame.image.load(resource_path("leo_hero1.png")).convert_alpha()

# Redimensionne l'image d'introduction à une taille de 350 x 150 pixels.
# 'pygame.transform.smoothscale()' redimensionne l'image de manière fluide 
# pour éviter les artefacts (Éléments graphiques interactifs.).
intro_image = pygame.transform.smoothscale(intro_image, (350, 150))

# Création d'une nouvelle surface avec la taille de l'image d'introduction 
# et un coin arrondi de 30 pixels.

# Crée une nouvelle surface avec la même taille que l'image d'introduction
# 'pygame.Surface()' crée une nouvelle surface
# 'intro_image.get_size()' obtient la taille de l'image d'introduction
# 'pygame.SRCALPHA' indique que la surface prend en charge la transparence
rounded_image = pygame.Surface(intro_image.get_size(), pygame.SRCALPHA)

# Définit le rayon des coins arrondis à 30 pixels.
corner_radius = 30

# Obtient le rectangle de la nouvelle surface.
# 'get_rect()' obtient le rectangle de la surface.
rect = rounded_image.get_rect()


# Dessine un rectangle avec des coins arrondis pour créer un effet visuel autour de l'image.

# Dessine un rectangle sur la surface 'rounded_image'
# 'pygame.draw.rect()' dessine un rectangle sur une surface
# 'rounded_image' est la surface sur laquelle le rectangle est dessiné
# '(255, 255, 255, 255)' est la couleur du rectangle (blanc avec transparence)
# 'rect' est le rectangle définissant la position et la taille du rectangle
# 'border_radius=corner_radius' définit le rayon des coins arrondis du rectangle
pygame.draw.rect(rounded_image, (255, 255, 255, 255), rect, border_radius=corner_radius)

# Superposition de l'image d'introduction sur le rectangle arrondi.

# Superpose l'image d'introduction sur la surface 'rounded_image'.
# 'rounded_image.blit()' superpose une image sur une autre surface.
# 'intro_image' est l'image à superposer.
# '(0, 0)' est la position où l'image est superposée (coin supérieur gauche).
# 'special_flags=pygame.BLEND_RGBA_MIN' applique un effet de mélange pour gérer la transparence.
rounded_image.blit(intro_image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

# Réinitialisation de "intro_image" pour utiliser la nouvelle version avec bords arrondis.

# Réinitialise 'intro_image' pour qu'elle utilise la nouvelle version avec des bords arrondis.
# 'intro_image' est maintenant la surface 'rounded_image' avec les bords arrondis.
intro_image = rounded_image


# Fonction pour obtenir la date et l'heure actuelles
# Définition d'une fonction nommée get_date_time pour obtenir la date et l'heure actuelles.
def get_date_time():
    
    # Configuration de la langue en français pour afficher le jour en français
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    
    # Définition du fuseau horaire sur 'Europe/Paris' en utilisant le module 'pytz'.
    timezone = pytz.timezone('Europe/Paris')
    
    # Obtention de la date et de l'heure actuelles dans le fuseau horaire spécifié.
    now = datetime.now(timezone)
    
    # Formatage de la date dans le format "jour en lettres-jour-mois-année".
    date_str = now.strftime("%A %d-%m-%Y")
    
    # Formatage de l'heure dans le format "heures:minutes:secondes".
    time_str = now.strftime("%H:%M:%S")
    
    # Retourne la date et l'heure sous forme de chaînes de caractères
    return date_str, time_str



# Texte de l'histoire du jeu, qui sera affiché avant de commencer l'aventure
# Il présente le scénario et le personnage principal "Léo"..
story_text = """
Fonctionnement et intrigue du jeu :
________________________________________

La quête de Léo, le héros des Dys
________________________________________

Appuyez sur les touches du clavier 'haut/bas'
pour accélérer, arrêter ou reprendre le défilement du texte, lisez-le, à votre rythme.

Utiliser les touches fléches de votre clavier pour le déplacement du personnage.

Vous pouvez aussi mettre le jeu en plein écran ou en sortir, en utilisant la touche 'F'
de votre clavier.

La quête de Léo, le héros des Dys raconte l'histoire de Léo, un jeune garçon courageux vivant
avec la dyslexie, la dyspraxie et la dysgraphie.

Il découvre une porte mystérieuse qui le mène dans le "Monde des Dys",
un univers parallèle symbolisant les défis auxquels font face les enfants comme lui.

Léo y rencontre des obstacles représentant ses difficultés quotidiennes,
mais aussi des power-ups magiques qui lui offrent des capacités pour les surmonter.

Au fil de son aventure, les défis deviennent plus complexes,
mais Léo gagne en confiance et en force.

Finalement, après avoir affronté un dernier combat difficile,
il réalise que ce monde était une métaphore de ses luttes personnelles,
mais qu'il a la force intérieure pour les surmonter.

De retour dans sa chambre, il comprend que, bien que les obstacles persistent,
il est capable de les affronter un à un.

Ce jeu a pour but de donner aux joueurs Dys la possibilité de voir chaque difficulté
comme une opportunité de grandir, quel que soit leur âges et leur(s) trouble(s).
En se disant : "Si Léo peut le faire, moi aussi je peux le faire".
________________________________________

Ce jeu est conçu pour être une aventure ludique et motivante pour les enfants et adultes 
atteints de troubles d'apprentissage Dys (dyslexie, dyspraxie, dysgraphie).
 
Voici une brève définition pour chacun des trois troubles Dys :
1-Dyslexie : 
Trouble de l'apprentissage de la lecture qui se caractérise par des difficultés 
à identifier et décoder les mots, à percevoir les sons des lettres et des syllabes
et à comprendre le sens du texte. 
Elle entraîne des erreurs fréquentes de lecture et de lentes progressions.
2-Dyspraxie : 
Trouble du développement moteur affectant la planification et la coordination des gestes. 
Elle est traduite par des difficultés à réaliser des mouvements précis 
ou des séquences de mouvements, comme l'écriture, le découpage ou même des gestes quotidiens.
3-Dysgraphie : 
Trouble de l'apprentissage de l'écriture qui se manifeste par une écriture lente, 
illisible ou incohérente. 
Il est souvent difficile pour les personnes atteintes de maintenir une posture 
adéquate pour écrire et de gérer la pression exercée sur l'outil d'écriture, 
ce qui peut rendre l'écriture fatigante.
Ces troubles peuvent affecter différemment chaque individu et nécessitent 
souvent un soutien et des adaptations pour faciliter l'apprentissage et la vie quotidienne.

Bonne aventure avec Léo.
________________________________________
"""

# Fonction pour couper le texte en plusieurs lignes pour qu'il s'adapte bien à l'écran
# "text" est le texte à afficher, "font" est la police de caractères utilisée, 
# "max_width" est la largeur maximum autorisée.
# Cela crée une liste de lignes à afficher une à une sur l'écran.
def wrap_text(text, font, max_width):
    # Divise le texte en une liste de mots en utilisant l'espace comme séparateur.
    words = text.split(' ')

    # Initialise une liste vide pour stocker les lignes de texte.
    lines = []

    # Initialise une liste vide pour stocker les mots de la ligne actuelle.
    current_line = []

    # Parcourt chaque mot dans la liste de mots.
    for word in words:
        # Ajoute le mot à la ligne actuelle.
        current_line.append(word)

        # Calcule la largeur de la ligne actuelle en joignant les mots avec des espaces.
        width, _ = font.size(' '.join(current_line))

        # Si la largeur de la ligne actuelle dépasse la largeur maximum autorisée.
        if width > max_width:
            # Retire le dernier mot ajouté à la ligne actuelle.
            current_line.pop()

            # Ajoute la ligne actuelle à la liste des lignes.
            lines.append(' '.join(current_line))

            # Réinitialise la ligne actuelle avec le mot retiré.
            current_line = [word]

    # Si des mots restent dans la ligne actuelle après la boucle.
    if current_line:
        # Ajoute la dernière ligne à la liste des lignes.
        lines.append(' '.join(current_line))

    # Renvoie la liste des lignes de texte.
    return lines


# Fonction pour faire défiler le texte de l'histoire sur l'écran.
# Cela affiche le texte ligne par ligne et permet de le faire défiler aussi
# à l'aide des touches du clavier.

def scroll_text():
    # Utilisation de la variable globale 'screen' pour accéder à l'écran de jeu.
    global screen

    # Création d'une police d'écriture de taille 43 pixels pour le texte.
    # 'pygame.font.Font(None, 43)' crée une police de caractères de taille 43 pixels.
    font = pygame.font.Font(None, 43)

    # La largeur maximale du texte est la largeur de la fenêtre (WIDTH) 
    # moins 35 pixels de marge.
    # 'max_text_width' est la largeur maximale autorisée pour le texte.
    max_text_width = WIDTH - 35

    # Appel de la fonction wrap_text pour obtenir le texte formaté par lignes.
    # 'wrapped_text' est une liste qui contiendra le texte formaté par lignes.
    wrapped_text = []

    # Parcourt chaque paragraphe du texte de l'histoire.
    # 'story_text.splitlines()' divise le texte en paragraphes.
    for paragraph in story_text.splitlines():
        # Ajoute les lignes formatées du paragraphe à 'wrapped_text'.
        # 'wrap_text(paragraph, font, max_text_width)' renvoie une liste de lignes formatées.
        wrapped_text.extend(wrap_text(paragraph, font, max_text_width))

    # Initialisation de la position 'Y' de défilement, commence hors de l'écran en bas.
    # 'scroll_y' est la position verticale de défilement du texte.
    scroll_y = HEIGHT

    # Espacement entre chaque ligne, fixé à 35 pixels.
    # 'line_spacing' est l'espacement vertical entre chaque ligne de texte.
    line_spacing = 35

    # Hauteur totale du texte (nombre de lignes multiplié par l'espacement entre lignes).
    # 'total_height' est la hauteur totale du texte à afficher.
    total_height = len(wrapped_text) * line_spacing

    # Vitesse de défilement initiale fixée à 1 pixel par image.
    # 'scroll_speed' est la vitesse à laquelle le texte défile.
    scroll_speed = 1

    # Variable pour savoir si on est en mode plein écran ou non.
    # 'fullscreen' est une variable qui indique si le jeu est en mode plein écran.
    fullscreen = False

    # Indicateur pour savoir si le jeu est en cours d'exécution.
    # 'running' est une variable qui indique si le jeu est en cours d'exécution.
    running = True

    # Boucle tant que la variable 'running' est vraie.
    while running:
        
        # Efface le contenu de l'écran en le remplissant entièrement de noir.
        # "screen.fill(BLACK)" applique une couleur noire à toute la surface de l'écran 
        # pour le réinitialiser.
        screen.fill(BLACK)
        
        # Obtention et affichage de la date et de l'heure
        # Appel de la fonction 'get_date_time' pour obtenir 
        # la date et l'heure actuelles sous forme de chaînes
        date_str, time_str = get_date_time()

        # Rendu de la date sous forme de texte avec la police spécifiée et en blanc.
        date_surface = font.render(date_str, True, WHITE)

        # Rendu de l'heure sous forme de texte avec la police spécifiée et en blanc.
        time_surface = font.render(time_str, True, WHITE)

    
        # Positionnement de la date et de l'heure.
        # Création d'un rectangle pour centrer l'affichage de la date
        # Le centre du rectangle est positionné horizontalement au milieu de l'écran (WIDTH // 2)
        # et verticalement à 20 pixels depuis le haut de l'écran
        date_rect = date_surface.get_rect(center=(WIDTH // 2, 20))
        # Création d'un rectangle pour centrer l'affichage de l'heure
        # Le centre du rectangle est positionné horizontalement au milieu de l'écran (WIDTH // 2)
        # et verticalement à une position de HEIGHT - 400, soit 400 pixels 
        # au-dessus du bas de l'écran
        time_rect = time_surface.get_rect(center=(WIDTH // 2, HEIGHT - 400))
        
        # Affichage de la date et de l'heure
        # Affichage de la surface contenant la date '(date_surface)' 
        # à la position définie par 'date_rect'
        # Cela permet de dessiner le texte de la date sur l'écran 
        # aux coordonnées spécifiées par 'date_rect'
        screen.blit(date_surface, date_rect)
        # Affichage de la surface contenant l'heure '(time_surface)' 
        # à la position définie par 'time_rect'
        # Cela permet de dessiner le texte de l'heure sur l'écran 
        # aux coordonnées spécifiées par 'time_rect'
        screen.blit(time_surface, time_rect)
        
        # Prépare la position de l'image d'introduction pour l'afficher au centre de l'écran
        # Utilise "get_rect()" pour obtenir un rectangle autour de l'image 
        # et le centre à une position spécifique.
        # "(WIDTH // 2, HEIGHT // 2 - 190)" place le centre de l'image horizontalement 
        # au milieu de l'écran
        # et 190 pixels au-dessus du centre vertical
        intro_image_rect = intro_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 190))
        
        
        # Affiche l'image d'introduction sur l'écran aux coordonnées spécifiées 
        # par "intro_image_rect".
        # "screen.blit(intro_image, intro_image_rect)". 
        # dessine l'image sur l'écran en fonction du rectangle défini.
        screen.blit(intro_image, intro_image_rect)

        # Boucle à travers chaque ligne du texte en utilisant 
        # son index et le contenu de la ligne.
        for i, line in enumerate(wrapped_text):
            # Rend la ligne de texte actuelle sur une nouvelle surface de texte.
            # "font.render()" dessine le texte sur une surface, prenant comme paramètres la ligne,
            # une valeur True pour lisser le texte (anti-aliasing), 
            # et la couleur du texte (ici "OR")
            text_surface = font.render(line, True, OR)
            # Crée un rectangle autour de la surface de texte pour le positionnement.
            # "text_surface.get_rect()" crée un rectangle pour la surface de texte,
            # "center=" le centre à une position spécifique.
            # Ici, "WIDTH // 2" positionne horizontalement au centre, et
            # "scroll_y + i * line_spacing" ajuste verticalement 
            # en fonction du défilement et de l'espacement.
            text_rect = text_surface.get_rect(center=(WIDTH // 2, scroll_y + i * line_spacing))
            # Affiche la surface de texte sur l'écran à la position définie par text_rect.
            # "screen.blit()" dessine la surface de texte sur l'écran 
            # aux coordonnées définies par le rectangle.
            screen.blit(text_surface, text_rect)

        # Défilement du texte vers le haut en fonction de la vitesse.
        scroll_y -= scroll_speed

        # Vérifie si tout le texte a défilé hors de l'écran, si c'est le cas 
        # la boucle doit être arrêtée.
        if scroll_y + total_height < 0:
            # Définit la variable "running" sur False pour arrêter la boucle
            running = False

        # Parcourt chaque événement qui a eu lieu depuis le dernier appel pour les gérer un par un
        for event in pygame.event.get():
            # Vérifie si l'événement actuel est de type "QUIT" (l'utilisateur veut quitter le jeu)
            if event.type == pygame.QUIT:
                # Ferme Pygame correctement
                pygame.quit()
                # Arrête le programme en fermant Python
                sys.exit()
            
            # Vérifie si une touche du clavier a été enfoncée
            elif event.type == pygame.KEYDOWN:
                # Vérifie si la touche enfoncée est "f" pour basculer en mode plein écran
                if event.key == pygame.K_f:
                    # Inverse l'état du plein écran : si activé, le désactive, et vice versa
                    fullscreen = not fullscreen


                    # Si le mode plein écran est activé
                    if fullscreen:
                        # Redimensionne la fenêtre pour s'afficher en plein écran
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        
                    # Si le mode plein écran est désactivé
                    else:
                        # Redimensionne la fenêtre à sa taille d'origine sans le plein écran
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        
                        
                # Vérifie si la touche enfoncée est la flèche "Haut"
                elif event.key == pygame.K_UP:
                    # Augmente la vitesse de défilement d'une unité, avec un maximum de 5
                    scroll_speed = min(scroll_speed + 1, 5)
                    
                    
                # Vérifie si la touche enfoncée est la flèche "Bas"
                elif event.key == pygame.K_DOWN:
                    # Réduit la vitesse de défilement d'une unité, 
                    # avec un minimum de 0 (arrêt complet)
                    scroll_speed = max(scroll_speed - 1, 0)
                    

        # Rafraîchit l'écran pour que les modifications soient affichées.
        pygame.display.flip()
        # Contrôle la vitesse de la boucle pour la limiter à 30 images par seconde.
        pygame.time.Clock().tick(30)
        

# Définition de la fonction 'countdown', qui gère le décompte avant le début du jeu
# Cette fonction affichera un compte à rebours de 5 à 0 pour annoncer le début de l'aventure
def countdown():
    # Crée une police de caractères de taille 95 pour afficher 
    # les grands chiffres du compte à rebours
    font = pygame.font.Font(None, 95)
    
    # Définition du texte qui sera affiché en haut, avant le compte à rebours
    countdown_text = "La quête de Léo va commencer dans :"
    
    # Création de la surface contenant le texte de compte à rebours
    # Ici, "pygame.font.Font(None, 50)" définit une police de taille 50
    # ".render()" transforme le texte en une image (surface), 
    # avec "True" pour lisser les bords et la couleur "WHITE"
    countdown_surface = pygame.font.Font(None, 50).render(countdown_text, True, WHITE)
    
    # Variable qui stocke la durée totale du compte à rebours en secondes, 
    # ici 5 secondes pour aller de 9 à 0
    total_time = 9

    # Définition de la taille maximale du rayon pour dessiner un arc de cercle 
    # autour du compte à rebours
    # Cet arc montrera visuellement le temps restant
    max_radius = 110
    

    # Boucle de décompte qui commence à la valeur de "total_time" (5) et va jusqu'à -1
    # La boucle décrémente de 1 à chaque itération pour afficher le compte à rebours de 5 à 0
    for i in range(total_time, -1, -1):
        # Remplit l'écran avec la couleur noire pour effacer l'image précédente
        # Cela garantit que chaque chiffre du compte à rebours apparaît 
        # proprement sans chevauchement
        screen.fill(BLACK)
        # Affiche le texte d'introduction du compte à rebours au centre de l'écran
        # "screen.blit()" dessine la surface de texte 
        # (countdown_surface) aux coordonnées spécifiées
        # WIDTH // 2 - 300 positionne le texte horizontalement au centre moins 300 pixels,
        # HEIGHT // 2 - 130 positionne le texte verticalement légèrement au-dessus du centre
        screen.blit(countdown_surface, (WIDTH // 2 - 300, HEIGHT // 2 - 130))


        # Convertit le chiffre actuel du compte à rebours en texte 
        # et crée une surface pour l'afficher
        # "font.render(str(i), True, WHITE)" 
        # transforme le chiffre en chaîne de caractères avec "str(i)",
        # puis le rend (dessine) sur une surface avec une couleur blanche (WHITE) 
        # et anti-aliasing activé (True)
        count_surface = font.render(str(i), True, WHITE)
        
        
        # Affiche le chiffre du compte à rebours au centre de l'écran
        # "screen.blit(count_surface, (WIDTH // 2 - 20, HEIGHT // 2))" 
        # place l'image du chiffre au centre,
        # en ajustant horizontalement de -20 pixels pour un centrage plus précis
        screen.blit(count_surface, (WIDTH // 2 - 20, HEIGHT // 2))
        
        
        # Calcule l'angle de l'arc de cercle à afficher autour du chiffre, 
        # proportionnel au temps restant
        # "(i / total_time) * 360" calcule une portion de cercle : 
        # on divise le temps restant (i) par le temps total,
        # puis on multiplie par 360 pour obtenir l'angle correspondant en degrés
        angle = (i / total_time) * 360
        

        # Dessine un arc de cercle rouge qui représente le temps restant 
        # avant la fin du compte à rebours
        # "pygame.draw.arc()" crée un arc de cercle sur l'écran ; 
        # on utilise "screen" pour le dessiner
        # "(255, 0, 0)" définit la couleur rouge ; 
        # le tuple 
        # (WIDTH // 2 - max_radius, HEIGHT // 2 - max_radius + 40, 2 * max_radius, 2 * max_radius)
        # définit la position et la taille de l'arc centré sur l'écran avec 
        # un décalage vertical de 40 pixels.
        # Le 0 est l'angle de départ (en radians), 
        # et "angle * (math.pi / 180)" convertit l'angle en degrés en radians
        # "max_radius" définit l'épaisseur de l'arc
        pygame.draw.arc(screen, (255, 0, 0), (WIDTH // 2 - max_radius, HEIGHT // 2 - max_radius + 40, 2 * max_radius, 2 * max_radius), 0, angle * (math.pi / 180), max_radius)
        
        
        # Rend le chiffre actuel du compte à rebours sur une surface de texte pour affichage
        # Ici, "font.render(str(i), True, WHITE)" 
        # convertit le chiffre "i" en texte avec la couleur blanche (WHITE)
        count_surface = font.render(str(i), True, WHITE)
        
        
        # Affiche le chiffre du compte à rebours au centre de l'écran
        # "screen.blit(count_surface, (WIDTH // 2 - 20, HEIGHT // 2))" 
        # place la surface contenant le chiffre au centre
        screen.blit(count_surface, (WIDTH // 2 - 20, HEIGHT // 2))
        
        
        # Dessine un deuxième arc de cercle, plus fin et de couleur verte, 
        # pour indiquer le même temps restant
        # "pygame.draw.arc()" crée cet arc sur l'écran avec la couleur verte (GREEN)
        # Les mêmes paramètres de position et taille sont utilisés, 
        # mais l'épaisseur est de 10 pixels cette fois-ci
        pygame.draw.arc(screen, GREEN, (WIDTH // 2 - max_radius, HEIGHT // 2 - max_radius + 40, 2 * max_radius, 2 * max_radius), 0, angle * (math.pi / 180), 10)
        
        
        # Met à jour l'écran pour afficher l'arc de cercle et le chiffre du compte à rebours
        # "pygame.display.flip()" rafraîchit l'écran avec les nouveaux éléments affichés
        pygame.display.flip()
        
        
        # Attend une seconde avant de passer au chiffre suivant pour créer l'effet de décompte
        # "pygame.time.delay(1000)" retarde le programme d'exactement 1000 millisecondes, 
        # soit 1 seconde
        pygame.time.delay(1000)
        
        
        

# Fonction qui charge aléatoirement un fond d'écran parmi plusieurs options disponibles
# Cela permet de changer l'apparence du jeu durant chaque partie pour plus de variété visuelle
def load_random_background():
    
    # Liste des fichiers d'image de fond disponibles dans le dossier du projet
    # Chaque fichier correspond à une image de fond possible que l'on pourra afficher dans le jeu
    backgrounds = ["background1.png", "background2.png", "background3.png", "background4.png", "background5.png", "background6.png"]
    
    # Sélectionne un fichier d'image aléatoirement dans la liste des fonds d'écran
    # "random.choice(backgrounds)" choisit un des éléments de la liste au hasard
    chosen_background = random.choice(backgrounds)
    
    # Charge l'image de fond choisie et la convertit pour être compatible 
    # avec l'affichage dans Pygame
    # "pygame.image.load()" charge le fichier d'image, "resource_path()" 
    # fournit le chemin complet du fichier,
    # et ".convert()" optimise l'image pour un affichage plus rapide dans Pygame
    bg = pygame.image.load(resource_path(chosen_background)).convert()
    
    # Redimensionne l'image de fond chargée pour qu'elle corresponde 
    # exactement à la taille de la fenêtre du jeu
    # "pygame.transform.scale(bg, (WIDTH, HEIGHT))" 
    # ajuste la taille de l'image aux dimensions définies par WIDTH et HEIGHT
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))


# Définition de la classe 'Mobile' pour représenter les obstacles mobiles dans le jeu
# Cette classe gère l'apparence, la position et le mouvement des obstacles qui tombent
class Mobile(pygame.sprite.Sprite):
    
    # Initialisation de la classe Mobile avec l'image, 
    # la vitesse de chute et le niveau actuel du jeu
    def __init__(self, image, vitesse_chute, niveau):
        # Appelle le constructeur de la classe parente pygame.sprite.Sprite
        super().__init__()
        
        # Redimensionne l'image de l'obstacle pour qu'elle mesure 
        # 45 pixels de large et 45 pixels de haut
        # "pygame.transform.scale(image, (45, 45))" ajuste la taille de l'image fournie.
        self.image = pygame.transform.scale(image, (45, 45))
        
        # Obtient un rectangle (rect) autour de l'image pour gérer la position et les collisions
        # "self.image.get_rect()" génère un rectangle basé sur les dimensions de l'image.
        self.rect = self.image.get_rect()
        
        # Stocke la vitesse de chute de l'obstacle. 
        # pour déterminer la rapidité de son déplacement.
        self.vitesse_chute = vitesse_chute
        
        # Définition de la direction de chute initiale, par défaut vers le bas.
        self.direction = 'bas'

        # Vérifie si le niveau est supérieur ou égal à 12 
        # pour modifier la position initiale et direction de l'obstacle.
        if niveau >= 12:
            # Choisit une direction aléatoire pour l'apparition de l'obstacle. 
            # parmi 'gauche', 'droite' et 'bas'
            self.direction = random.choice(['gauche', 'droite', 'bas'])
            
            # Si la direction est 'gauche', positionne l'obstacle à gauche de l'écran
            if self.direction == 'gauche':
                # Place l'obstacle juste en dehors de l'écran à gauche
                self.rect.x = -self.rect.width
                # Place l'obstacle à une hauteur aléatoire sur l'écran
                self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            
            # Si la direction est 'droite', positionne l'obstacle à droite de l'écran
            elif self.direction == 'droite':
                # Place l'obstacle juste en dehors de l'écran à droite
                self.rect.x = WIDTH
                # Place l'obstacle à une hauteur aléatoire sur l'écran
                self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            
            # Si la direction est 'bas', positionne l'obstacle en haut de l'écran
            else:
                # Place l'obstacle à une position horizontale aléatoire
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                # Place l'obstacle juste en dehors de l'écran en haut
                self.rect.y = -self.rect.height

        # Si le niveau est inférieur à 12, tous les obstacles commencent en haut de l'écran
        else:
            # Place l'obstacle à une position horizontale aléatoire en haut de l'écran
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            # Place l'obstacle juste en dehors de l'écran en haut
            self.rect.y = -self.rect.height

    # Méthode pour mettre à jour la position de l'obstacle à chaque itération du jeu
    def update(self):
        
        # Mise à jour de la position de l'obstacle selon la direction définie.
        if self.direction == 'gauche':
            # Déplace l'obstacle vers la droite s'il est apparu à gauche
            self.rect.x += self.vitesse_chute
        
        elif self.direction == 'droite':
            # Déplace l'obstacle vers la gauche s'il est apparu à droite.
            self.rect.x -= self.vitesse_chute
        
        else:
            # Déplace l'obstacle vers le bas pour une chute verticale.
            self.rect.y += self.vitesse_chute

        # Vérifie si l'obstacle est complètement sorti de l'écran pour le supprimer
        # Si l'obstacle est en dessous, à gauche ou à droite de l'écran, on le retire
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            # Supprime l'obstacle en appelant la méthode "kill()" pour libérer de la mémoire.
            self.kill()


# Définition de la classe 'PowerUp' pour représenter les objets 'power-ups' dans le jeu
# Cette classe gère l'apparence, la position et le mouvement des 'power-ups' qui tombent
class PowerUp(pygame.sprite.Sprite):
    
    # Initialisation de la classe 'PowerUp' avec l'image, 
    # la vitesse de chute et le type de 'power-up'.
    def __init__(self, image, vitesse_chute, powerup_type):
        # Appelle le constructeur de la classe parente pygame.sprite.Sprite.
        super().__init__()
        
        # Associe l'image fournie au power-up pour définir son apparence dans le jeu.
        self.image = image
        
        # Obtient un rectangle (rect) autour de l'image pour gérer la position et les collisions
        # "self.image.get_rect()" génère un rectangle basé sur les dimensions de l'image
        self.rect = self.image.get_rect()
        
        # Stocke la vitesse de chute du power-up pour déterminer la rapidité de son déplacement
        self.vitesse_chute = vitesse_chute
        
        # Stocke le type de 'power-up' (par exemple, bonus de vie, augmentation de puissance, etc.)
        # pour que le jeu puisse identifier l'effet du 'power-up' lorsqu'il est collecté.
        self.type = powerup_type
        
        # Définit la position initiale du 'power-up' en haut de l'écran 
        # avec une position 'x' aléatoire
        # "self.rect.x" est placé à une position aléatoire horizontale 
        # pour varier le point de départ
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        
        # Place le 'power-up' juste au-dessus du haut de l'écran pour 
        # qu'il commence à tomber depuis cette position.
        self.rect.y = -self.rect.height

    # Méthode pour mettre à jour la position du power-up à chaque itération du jeu
    def update(self):
        
        # Déplace le power-up vers le bas en ajoutant la vitesse de chute à sa position Y
        # Cela crée un mouvement vertical descendant pour simuler la chute du power-up
        self.rect.y += self.vitesse_chute
        
        # Vérifie si le power-up est complètement sorti de l'écran par le bas pour le supprimer
        # Si le haut du rectangle du power-up est plus bas que la hauteur de l'écran, on le retire
        if self.rect.top > HEIGHT:
            # Supprime le power-up en appelant la méthode "kill()" pour libérer de la mémoire
            self.kill()


# Fonction principale du jeu
# La fonction "main()" est le cœur du jeu : 
# elle gère tout ce qui se passe dans le jeu, y compris
# l'affichage des éléments à l'écran, les interactions avec le joueur, 
# et la logique du jeu (comme le score et le niveau)
def main():
    
    # Déclaration de variables globales nécessaires au fonctionnement du jeu
    # Les variables globales sont partagées dans toutes les fonctions du programme
    # Ici, on déclare les variables globales utilisées 
    # dans la fonction "main()" pour contrôler divers aspects du jeu
    
    # Déclare la variable "player_rect" pour stocker la position et la taille du joueur
    global player_rect
    
    # Déclare la variable "obstacles" pour gérer le groupe de tous 
    # les obstacles qui apparaissent dans le jeu
    global obstacles
    
    # Déclare la variable "powerups" pour gérer le groupe de tous 
    # les power-ups que le joueur peut collecter
    global powerups
    
    # Déclare la variable "score" pour stocker le score actuel du joueur
    global score
    
    # Déclare la variable "level" pour garder en mémoire le niveau actuel du joueur dans le jeu
    global level
    
    # Déclare la variable "invincible" pour indiquer si le joueur 
    # est invincible (protégé des obstacles) ou non
    global invincible
    
    # Déclare la variable "slow_obstacles" pour indiquer si les obstacles 
    # se déplacent plus lentement à cause d’un power-up
    global slow_obstacles
    
    # Déclare la variable "powerup_timer" pour suivre le temps écoulé 
    # pendant lequel un power-up est actif
    global powerup_timer
    
    # Déclare la variable "spawn_timer" pour mesurer le temps écoulé 
    # entre l'apparition de chaque nouvel obstacle
    global spawn_timer
    
    # Déclare la variable "background" pour stocker l'image de fond d'écran 
    # actuellement affichée dans le jeu
    global background
    
    # Déclare la variable "spawn_interval" pour définir l'intervalle de temps 
    # entre l'apparition de nouveaux obstacles
    global spawn_interval
    
    # Déclare la variable "last_score_update" pour stocker le moment où le score 
    # a été mis à jour pour la dernière fois
    global last_score_update
    
    # Déclare la variable "player_speed" pour gérer la vitesse de déplacement 
    # du joueur dans le jeu
    global player_speed
    
    # Déclare la variable "fullscreen" pour indiquer si le jeu est en mode plein écran 
    # (occupant tout l'écran) ou non
    global fullscreen
    
    # Déclare la variable "screen" pour gérer l'écran de jeu et afficher 
    # tous les éléments (joueur, obstacles, etc.)
    global screen
    
    # Déclare la variable "bonus_collected" pour indiquer si un bonus 
    # a été collecté récemment par le joueur
    global bonus_collected
    
    # Déclare la variable "bonus_display_timer" pour mesurer le temps écoulé 
    # depuis que le dernier bonus a été collecté
    global bonus_display_timer
    
    # Déclare la variable "bonus_collected_count" pour compter le nombre total 
    # de bonus collectés par le joueur
    global bonus_collected_count


    # Initialisation des variables de jeu pour le suivi du nombre de bonus collectés
    bonus_collected_count = 0

    # Création de groupes de sprites pour gérer les obstacles et les power-ups
    
    # Crée un groupe de sprites pour gérer tous les obstacles dans le jeu
    # "pygame.sprite.Group()" crée un groupe qui peut contenir plusieurs objets (sprites) 
    # de type obstacle
    # Cela permet de les gérer facilement ensemble, 
    # comme pour les déplacements ou les collisions.
    obstacles = pygame.sprite.Group()
    
    
    # Crée un groupe de sprites pour gérer tous les 'power-ups' dans le jeu
    # "pygame.sprite.Group()" crée également un groupe pour les 'power-ups', 
    # facilitant leur gestion
    # Les 'power-ups' peuvent être ajoutés, mis à jour et vérifiés pour les collisions.
    powerups = pygame.sprite.Group()

    # Définition des timers pour contrôler l'apparition des obstacles et le déroulement du jeu
    # Cette section initialise les variables utilisées pour gérer le timing et l’état du jeu
    
    # Initialise le "spawn_timer" à 0 pour démarrer le compte du temps écoulé 
    # avant l'apparition d'un nouvel obstacle
    spawn_timer = 0
    
    # Définit "spawn_interval" à 60 pour espacer l’apparition des obstacles
    # Cet intervalle est exprimé en images (frames) : 
    # 60 correspond à 1 seconde si le jeu fonctionne à 60 images par seconde.
    spawn_interval = 60  # Intervalle entre apparitions des obstacles, exprimé en images.
    
    # Définit la "player_speed" à 5, qui est la vitesse de déplacement du joueur dans le jeu
    # Une valeur plus élevée permettrait au joueur de se déplacer plus rapidement
    player_speed = 5  # Vitesse de déplacement du joueur.
    
    # Initialise le "score" du joueur à 0, 
    # car le joueur commence le jeu sans avoir marqué de points
    score = 0  # Initialisation du score du joueur à 0.
    
    # Définit le "level" à 1 pour indiquer que le joueur commence au niveau 1
    level = 1  # Définition du niveau de départ du joueur
    
    # Définit "invincible" sur False car le joueur n’est pas invincible au départ
    # Lorsque ce statut est activé, le joueur est temporairement protégé des obstacles.
    invincible = False  # Statut d'invincibilité du joueur (désactivé au départ).
    
    # Définit "slow_obstacles" sur False car les obstacles ne sont pas ralentis par défaut
    # Ce statut peut être activé temporairement par un power-up 
    # pour diminuer la vitesse des obstacles
    slow_obstacles = False  # Indicateur pour ralentir les obstacles (désactivé).
    
    # Initialise le "powerup_timer" à 0 pour suivre le temps pendant lequel un power-up est actif
    powerup_timer = 0  # Timer pour mesurer la durée des effets de power-ups
    
    # Définit "fullscreen" sur False, ce qui signifie que le jeu démarre en mode fenêtre
    # Lorsqu’il est activé, le jeu s'affiche en mode plein écran
    fullscreen = False  # Mode plein écran désactivé par défaut
    
    # Initialise "bonus_collected" à False, car le joueur n’a pas encore collecté 
    # de bonus au début du jeu
    bonus_collected = False  # Indicateur pour savoir si un bonus a été collecté
    
    # Initialise "bonus_display_timer" à 0 pour mesurer la durée d’affichage 
    # d’un message lorsqu’un bonus est collecté
    bonus_display_timer = 0  # Timer pour afficher un message lorsqu'un bonus est collecté



    # Stocke l'heure de la dernière mise à jour du score en millisecondes
    # "pygame.time.get_ticks()" renvoie le nombre de 
    # millisecondes écoulées depuis le début du jeu
    # Cette valeur est utilisée pour savoir quand le score doit être mis à jour
    last_score_update = pygame.time.get_ticks()
    
    
    # Charge une image de fond aléatoire au début de la partie
    # "load_random_background()" est une fonction qui choisit une image parmi plusieurs options
    # Elle permet de varier l'apparence du fond d'écran durant chaque partie
    background = load_random_background()

    # Chargement de l'image du joueur et redimensionnement
    # La fonction "pygame.image.load()" charge l'image, et "convert_alpha()" 
    # conserve sa transparence
    player_img = pygame.image.load(resource_path("player.png")).convert_alpha()
    
    # Redimensionne l'image du joueur pour qu'elle mesure exactement 55x55 pixels
    # "pygame.transform.smoothscale()" ajuste la taille de l'image 
    # et lisse les bords pour une meilleure qualité
    # Cela permet d'obtenir une image de joueur cohérente en taille 
    # avec les autres éléments du jeu
    player_img = pygame.transform.smoothscale(player_img, (80, 80))  

    # Crée un rectangle de collision pour le joueur à partir de l'image redimensionnée
    # "player_img.get_rect()" génère un rectangle (rect) autour de l'image, 
    # qui sera utilisé pour la position et les collisions
    # Ce rectangle permettra de détecter quand le joueur entre en contact 
    # avec des obstacles ou des power-ups
    player_rect = player_img.get_rect()
    
    
    # Positionne le rectangle du joueur au centre de l'écran, en bas
    # "player_rect.center" place le centre du rectangle à une position spécifique
    # Ici, "WIDTH // 2" le centre horizontalement, et "HEIGHT - 50" 
    # le place légèrement au-dessus du bas de l'écran
    player_rect.center = (WIDTH // 2, HEIGHT - 50)
    

    # Chargement des images pour les différents types d'obstacles
    
    # Chargement de l'image pour l'obstacle de petite taille
    # "pygame.image.load()" charge l'image à partir du fichier "obstacle_small.png" 
    # et "resource_path()" assure que le chemin du fichier est correct
    # "convert_alpha()" permet de gérer la transparence de l'image, 
    # pour qu'elle s'affiche correctement dans le jeu
    obstacle_small = pygame.image.load(resource_path("obstacle_small.png")).convert_alpha()
    
    
    # Chargement de l'image pour l'obstacle de taille moyenne
    # Cette image est chargée de manière similaire à celle de l'obstacle petit,
    # mais provient d'un fichier différent, "obstacle_medium.png"
    obstacle_medium = pygame.image.load(resource_path("obstacle_medium.png")).convert_alpha()
    
    
    # Chargement de l'image pour l'obstacle de grande taille
    # De même, cette ligne charge l'image pour l'obstacle grand, 
    # en utilisant le fichier "obstacle_large.png" et en gérant la transparence 
    # avec "convert_alpha()"
    obstacle_large = pygame.image.load(resource_path("obstacle_large.png")).convert_alpha()
    
    

    # Chargement de l'image du power-up et redimensionnement à 40x40 pixels
    
    # Chargement de l'image pour le power-up
    # "pygame.image.load()" charge l'image à partir du fichier "powerup.png"
    # "resource_path()" garantit que le chemin du fichier est correct
    # "convert_alpha()" permet de gérer la transparence de l'image 
    # pour qu'elle s'affiche sans bords indésirables
    powerup_img = pygame.image.load(resource_path("powerup.png")).convert_alpha()
    
    
    # Redimensionnement de l'image du power-up à une taille de 35x35 pixels
    # "pygame.transform.scale()" ajuste la taille de l'image, 
    # ici pour qu'elle soit plus petite et s'intègre mieux au jeu
    powerup_img = pygame.transform.scale(powerup_img, (35, 35))

    # Création de l'horloge pour contrôler la vitesse du jeu
    
    # Création de l'horloge pour contrôler la vitesse de la boucle du jeu
    # "pygame.time.Clock()" crée un objet 'horloge' qui permet de limiter 
    # le nombre d'images par seconde
    # Cela aide à maintenir une vitesse constante pour le déroulement du jeu
    clock = pygame.time.Clock()
    
    
    # Variable pour indiquer si le jeu est en cours
    # "running = True" signifie que la boucle principale du jeu fonctionnera 
    # jusqu'à ce que cette variable soit False
    running = True  # Contrôle l'état de la boucle principale du jeu
    
    
    # Indicateur pour vérifier si l'alerte de combat final a été affichée
    # "alert_displayed = False" signifie que l'alerte ne s'affiche qu'une fois, 
    # et une fois affichée, cette variable sera mise à True pour éviter de la répéter
    alert_displayed = False  # Indicateur pour savoir si l'alerte de combat final a été affichée
    

    # Boucle principale du jeu
    # Cette boucle continue de s'exécuter tant que la variable "running" est True
    # Elle gère tous les éléments du jeu, comme l'affichage, le mouvement et les interactions
    while running:
        
        
        # Gère les événements du jeu (comme appuyer sur une touche ou fermer la fenêtre)
        # "pygame.event.get()" récupère tous les événements récents qui se sont produits
        # La boucle "for" parcourt chaque événement un par un pour vérifier ce qu'il faut faire
        for event in pygame.event.get():
            
            # Vérifie si l'événement est de type "QUIT", 
            # ce qui signifie que l'utilisateur veut fermer la fenêtre
            if event.type == pygame.QUIT:
                
                # Si la fenêtre est fermée, on arrête la boucle principale du jeu
                # En mettant "running = False", la boucle "while" s'arrête, 
                # ce qui met fin au jeu
                running = False
                
                
            # Vérifie si l'événement est de type "KEYDOWN", 
            # ce qui signifie qu'une touche a été enfoncée
            elif event.type == pygame.KEYDOWN:
                
                # Vérifie si la touche enfoncée est la touche "f"
                # "pygame.K_f" correspond à la touche "f" du clavier
                if event.key == pygame.K_f:
                    
                    # Bascule le mode plein écran entre activé et désactivé
                    # "fullscreen = not fullscreen" change la valeur
                    # de "fullscreen" de True à False ou inversement
                    # Cela signifie que si le plein écran est activé, 
                    # il sera désactivé, et vice versa
                    fullscreen = not fullscreen
                    

                    # Applique le mode plein écran si la variable "fullscreen" est True
                    # "pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)" 
                    # ajuste la fenêtre pour qu'elle prenne tout l'écran
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    
                    # Sinon, restaure la fenêtre à sa taille normale si "fullscreen" est False
                    else:
                        # "pygame.display.set_mode((WIDTH, HEIGHT))" 
                        # crée une fenêtre de jeu avec les dimensions standard
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        

        # Gère le déplacement du joueur en fonction des touches directionnelles pressées
        # "pygame.key.get_pressed()" vérifie l'état de chaque touche 
        # et renvoie un dictionnaire de touches pressées
        # Ce dictionnaire permet de savoir quelles touches 
        # sont actuellement enfoncées pour contrôler le mouvement du joueur
        keys = pygame.key.get_pressed()
        

        # Vérifie si la touche directionnelle gauche est enfoncée 
        # et si le joueur n'est pas déjà au bord gauche de l'écran
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            
            # Déplace le joueur vers la gauche en réduisant sa position X 
            # d'un montant égal à "player_speed"
            player_rect.x -= player_speed 
            
             
        # Vérifie si la touche directionnelle droite est enfoncée 
        # et si le joueur n'est pas déjà au bord droit de l'écran
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            
            # Déplace le joueur vers la droite en augmentant sa position X 
            # d'un montant égal à "player_speed"
            player_rect.x += player_speed  
            
            
        # Vérifie si la touche directionnelle haut est enfoncée 
        # et si le joueur n'est pas déjà au bord supérieur de l'écran
        if keys[pygame.K_UP] and player_rect.top > 0:
            
            # Déplace le joueur vers le haut en réduisant sa position Y 
            # d'un montant égal à "player_speed"
            player_rect.y -= player_speed 
            
             
        # Vérifie si la touche directionnelle bas est enfoncée 
        # et si le joueur n'est pas déjà au bord inférieur de l'écran
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            
            # Déplace le joueur vers le bas en augmentant sa position Y 
            # d'un montant égal à "player_speed"
            player_rect.y += player_speed  

        # Incrémente le timer pour contrôler l'apparition des obstacles
        # "spawn_timer" augmente de 1 à chaque cycle de la boucle pour mesurer le temps écoulé
        spawn_timer += 1
        

        
        # Crée un nouvel obstacle lorsque le timer atteint l'intervalle défini pour l'apparition
        # "spawn_timer >= spawn_interval" vérifie si le temps écoulé depuis le dernier obstacle
        # a atteint la durée spécifiée par "spawn_interval"
        if spawn_timer >= spawn_interval:
            
            # Choisit aléatoirement le type d'obstacle (petit, moyen ou grand)
            # "random.choice()" sélectionne un élément au hasard 
            # dans la liste des types d'obstacles
            obstacle_type = random.choice(["small", "medium", "large"])
            
            
            # Définit l'image, la taille et la vitesse de l'obstacle en fonction du type choisi
            # Utilise une expression conditionnelle pour chaque type d'obstacle
            # - Si "obstacle_type" est "small", utilise l'image "obstacle_small" 
            # avec une taille de 25x25 pixels et une vitesse de 7 + niveau
            # - Si "obstacle_type" est "medium", utilise "obstacle_medium" 
            # avec une taille de 45x45 pixels et une vitesse de 5 + niveau
            # - Si "obstacle_type" est "large", utilise "obstacle_large" 
            # avec une taille de 65x65 pixels et une vitesse de 3 + niveau
            img, size, speed = (obstacle_small, (25, 25), 7 + level) if obstacle_type == "small" else \
                               (obstacle_medium, (45, 45), 5 + level) if obstacle_type == "medium" else \
                               (obstacle_large, (65, 65), 3 + level)
                               
            
            # Redimensionne l'image de l'obstacle à la taille définie par "size"
            # "pygame.transform.scale(img, size)" 
            # ajuste les dimensions de l'image pour qu'elle corresponde 
            # au type d'obstacle (petit, moyen ou grand)
            img = pygame.transform.scale(img, size)
            
            # Crée un nouvel obstacle en utilisant l'image redimensionnée, 
            # la vitesse et le niveau actuel
            # La classe "Mobile" est utilisée pour créer un objet obstacle 
            # avec ses propriétés spécifiques  
            new_obstacle = Mobile(img, speed, level)
            
            # Ajoute le nouvel obstacle au groupe d'obstacles
            # "obstacles.add(new_obstacle)" permet de gérer facilement 
            # tous les obstacles ensemble dans le groupe  
            obstacles.add(new_obstacle)
            
            # Réinitialise le timer d'apparition des obstacles à 0
            # Cela permet de redémarrer le compte à rebours avant 
            # la création du prochain obstacle  
            spawn_timer = 0 
             

            
            # Crée un power-up aléatoirement avec une probabilité d'affichage de 30 %
            # "random.random()" génère un nombre décimal entre 0 et 1
            # Si ce nombre est inférieur à 0.3, alors un power-up sera créé 
            # (soit environ 30 % de chances)
            if random.random() < 0.3:
                
                # Choisit aléatoirement le type de power-up entre "invincible" et "slow"
                # "random.choice()" sélectionne un des deux types 
                # de power-ups de manière aléatoire
                powerup_type = random.choice(["invincible", "slow"])
                
                # Crée un nouvel objet power-up avec l'image "powerup_img", 
                # une vitesse de chute de 3, et le type choisi
                # La classe "PowerUp" est utilisée pour définir 
                # le comportement et les propriétés du power-up
                new_powerup = PowerUp(powerup_img, 3, powerup_type)
                
                # Ajoute le power-up créé au groupe de power-ups pour pouvoir 
                # le gérer avec d'autres power-ups
                powerups.add(new_powerup)
                

        # Met à jour la position de chaque obstacle et power-up dans leurs groupes respectifs
        # "obstacles.update()" et "powerups.update()" 
        # appellent la méthode update() pour chaque objet dans ces groupes
        # Cela permet de déplacer les obstacles et power-ups en fonction de leurs propriétés
        obstacles.update()
        powerups.update()
        
        

        # Vérifie s'il y a des collisions entre le joueur et chaque obstacle
        # La boucle "for" parcourt tous les obstacles dans le groupe "obstacles"
        for obstacle in obstacles:
            
            # Vérifie si le rectangle du joueur entre en collision avec 
            # le rectangle de l'obstacle
            # "player_rect.colliderect(obstacle.rect)" 
            # renvoie True si les rectangles se chevauchent (collision)
            # "and not invincible" s'assure que la collision n'est 
            # prise en compte que si le joueur n'est pas invincible
            if player_rect.colliderect(obstacle.rect) and not invincible:
                
                # Joue le son de fin de partie pour indiquer que le joueur a touché un obstacle
                game_over_sound.play()
                
                # Fait une pause de 3 secondes pour permettre au joueur de voir la fin de partie
                pygame.time.delay(3000)
                
                # Affiche l'écran de fin de jeu avec le score, 
                # le niveau et le nombre de bonus collectés
                # "display_game_over()" est une fonction qui affiche 
                # ces informations pour le joueur  
                display_game_over(score, level, bonus_collected_count)
                
                # Met fin à la partie en arrêtant la boucle principale du jeu
                # "running = False" arrête la boucle "while" et quitte le jeu
                running = False  
                

        # Vérifie s'il y a des collisions entre le joueur et chaque power-up
        # La boucle "for" parcourt tous les power-ups dans le groupe "powerups"
        for powerup in powerups:
            
             # Vérifie si le rectangle du joueur entre 
             # en collision avec le rectangle du power-up
            # "player_rect.colliderect(powerup.rect)" renvoie True 
            # si les rectangles se chevauchent (collision)
            if player_rect.colliderect(powerup.rect):
                
                
                # Active l'effet du power-up en fonction de son type
                # La condition suivante vérifie si le type de power-up est "invincible"
                if powerup.type == "invincible":
                    
                    # Active l'état d'invincibilité du joueur pour le protéger des obstacles
                    invincible = True
                    
                    # Démarre un timer pour mesurer la durée de l'effet d'invincibilité
                    # "pygame.time.get_ticks()" enregistre le temps actuel en millisecondes
                    powerup_timer = pygame.time.get_ticks()
                    
                    
                # Vérifie si le type de power-up est "slow" (ralentissement des obstacles)
                elif powerup.type == "slow":
                    
                    # Active l'effet de ralentissement des obstacles
                    # "slow_obstacles = True" indique que les obstacles se déplaceront plus lentement
                    slow_obstacles = True
                    
                    # Démarre un timer pour mesurer la durée de l'effet 
                    # de ralentissement des obstacles
                    # "pygame.time.get_ticks()" enregistre le temps actuel en millisecondes
                    powerup_timer = pygame.time.get_ticks()
                    
                # Joue le son de collecte de bonus pour signaler au joueur qu'il a obtenu un power-up
                bonus_sound.play()
                
                # Active un indicateur pour signaler que le joueur a collecté un bonus  
                bonus_collected = True
                
                # Démarre un timer pour gérer l'affichage du message de bonus collecté
                # "pygame.time.get_ticks()" enregistre le temps actuel, 
                # utilisé pour afficher un message temporaire  
                bonus_display_timer = pygame.time.get_ticks()
                
                # Incrémente le compteur de bonus collectés pour le suivi 
                # des bonus obtenus par le joueur  
                bonus_collected_count += 1 
                
                # Supprime le power-up après la collision pour qu'il 
                # ne soit plus affiché ni collecté à nouveau 
                powerup.kill()  

        # Vérifie la durée d'activation des effets des power-ups, 
        # qui est limitée à 6 secondes
        # Cette condition vérifie si l'un des deux effets 
        # (invincibilité ou ralentissement) est actif
        if invincible or slow_obstacles:
            
            
            # Calcule le temps écoulé depuis que le power-up a été activé
            # "pygame.time.get_ticks()" renvoie le temps actuel en millisecondes
            # En soustrayant "powerup_timer", on obtient la durée d'activation du power-up
            # Si cette durée dépasse 6000 millisecondes (6 secondes), 
            # l'effet du power-up doit se terminer
            if pygame.time.get_ticks() - powerup_timer > 6000:
                
                # Désactive l'effet d'invincibilité si celui-ci est actif
                invincible = False
                
                # Désactive l'effet de ralentissement des obstacles si celui-ci est actif
                slow_obstacles = False
                

        # Met à jour le score toutes les secondes pour récompenser le joueur au fil du temps
        # "current_time" enregistre le temps actuel en millisecondes 
        # à chaque passage dans la boucle de jeu
        current_time = pygame.time.get_ticks()
        
        # Vérifie si une seconde (1000 millisecondes) s'est écoulée depuis 
        # la dernière mise à jour du score
        # "current_time - last_score_update" 
        # calcule le temps écoulé depuis la dernière mise à jour
        # Si ce temps est supérieur ou égal à 1000, on ajoute un point au score
        if current_time - last_score_update >= 1000:
            
            # Incrémente le score du joueur de 1 pour chaque seconde passée
            score += 1
            
            # Met à jour "last_score_update" pour enregistrer l'heure actuelle
            # Cela permet de recommencer le compte pour une autre seconde 
            # avant la prochaine mise à jour du score
            last_score_update = current_time
            

            # Augmente le niveau et ajuste les paramètres du jeu tous les 10 points de score
            # "score % 10 == 0" signifie que le niveau augmente lorsque 
            # le score est un multiple de 10
            # Par exemple, lorsque le score est 10, 20, 30, etc., le niveau change
            if score % 10 == 0:
                
                # Incrémente le niveau du joueur de 1
                # Chaque augmentation de niveau rend le jeu plus difficile
                level += 1
                
                # Réduit l'intervalle d'apparition des obstacles 
                # pour les faire apparaître plus souvent
                # "spawn_interval = max(20, spawn_interval - 5)" 
                # diminue l'intervalle par 5, mais pas en dessous de 20
                spawn_interval = max(20, spawn_interval - 5)
                
                # Augmente la vitesse du joueur pour qu'il se déplace plus rapidement
                # "player_speed = min(10, player_speed + 0.5)" 
                # augmente la vitesse par 0.5, mais ne dépasse pas 10
                player_speed = min(10, player_speed + 0.5)
                
                # Change le fond d'écran de manière aléatoire 
                # à chaque changement de niveau pour varier les visuels
                background = load_random_background()
                
                
                

        # Vérifie si le niveau est supérieur ou égal à 12 et si l'alerte n'a pas déjà été affichée
        # "level >= 12" déclenche le combat final à partir du niveau 12
        # "not alert_displayed" s'assure que l'alerte ne s'affiche qu'une seule fois
        if level >= 12 and not alert_displayed:
            
            # Arrête la musique de fond pour mieux faire entendre le son d'alerte
            pygame.mixer.music.stop()
            
            # Joue le son d'alerte du combat final en boucle
            # "final_alert_sound.play()" 
            # fait jouer le son une seule fois, puis s'arrête de jouer le son 
            final_alert_sound.play(-1)
              
            # Prépare le texte d'alerte à afficher au centre de l'écran
            # "pygame.font.Font(None, 48)" crée une police de taille 48 pour le texte
            # ".render()" transforme le texte en une image (surface) 
            # avec une couleur rouge (255, 0, 0)
            alert_text = pygame.font.Font(None, 78).render("Attention ! Combat final.", True, (255, 0, 0))
            
            
            # Affiche le texte d'alerte au centre de l'écran
            # "screen.blit(alert_text, ...)" dessine le texte à une position 
            # centrée horizontalement
            # et légèrement ajustée verticalement
            screen.blit(alert_text, (WIDTH // 2 - alert_text.get_width() // 2, HEIGHT // 2 + alert_text.get_height() - 240 // 2))
            
            
            # Rafraîchit l'écran pour afficher l'alerte de combat final
            pygame.display.flip()
            
            # Fait une pause de 6 secondes pour que l'alerte reste visible 
            # avant de reprendre le jeu
            pygame.time.delay(6000)
            
            # Arrête le son d'alerte du combat final après la pause 
            final_alert_sound.stop()
            
            # Relance la musique de fond du jeu en boucle pour continuer l'ambiance sonore
            pygame.mixer.music.play(-1)
            
            # Marque l'alerte comme ayant déjà été affichée pour éviter de la rejouer 
            alert_displayed = True

        # Affiche l'écran de niveau final et termine la partie si le niveau atteint 34
        # "if level >= 34" vérifie si le niveau est 34 ou plus, marquant la fin de la partie
        if level >= 34:
            
            # Appelle la fonction pour afficher l'écran du niveau final
            # "display_final_level_screen()" 
            # est une fonction qui montre un écran spécial pour la fin de partie (fond noir)
            display_final_level_screen()
            
            
            # Met fin à la boucle principale du jeu pour terminer la partie
            # "running = False" arrête la boucle "while" en réglant "running" sur False
            running = False


        # Affiche l'image de fond aux coordonnées (0, 0) pour couvrir tout l'écran
        # "screen.blit(background, (0, 0))" place l'image de fond à l'origine de l'écran
        screen.blit(background, (0, 0))
        
        
        # Affiche l'image du joueur à sa position actuelle définie par "player_rect"
        # "screen.blit(player_img, player_rect)" dessine le joueur à sa position mise à jour
        screen.blit(player_img, player_rect)
        
        
        # Affiche chaque obstacle présent dans le groupe "obstacles" à sa position actuelle
        # La boucle "for" parcourt tous les objets "obstacle" du groupe "obstacles"
        for obstacle in obstacles:
            
            # Dessine l'image de l'obstacle à sa position définie par "obstacle.rect"
            # "screen.blit(obstacle.image, obstacle.rect)" place chaque obstacle sur l'écran
            screen.blit(obstacle.image, obstacle.rect)
        
        
        # Affiche chaque power-up présent dans le groupe "powerups" à sa position actuelle
        # La boucle "for" parcourt tous les objets "powerup" du groupe "powerups"
        for powerup in powerups:
            
            # Dessine l'image du power-up à sa position définie par "powerup.rect"
            # "screen.blit(powerup.image, powerup.rect)" place chaque power-up sur l'écran
            screen.blit(powerup.image, powerup.rect)
            

        # Affiche le nombre total de bonus collectés par le joueur
        # Crée une surface de texte pour afficher le nombre de bonus collectés 
        # avec une police de taille 38
        # "pygame.font.Font(None, 38).render()" génère un texte avec la couleur blanche (WHITE)
        bonus_collected_text = pygame.font.Font(None, 38).render(f"Bonus collectés : {bonus_collected_count}", True, WHITE)
        
        # Affiche le texte du nombre de bonus collectés en haut à gauche 
        # de l'écran aux coordonnées (10, 90)
        # "screen.blit(bonus_collected_text, (10, 80))" place le texte à la position souhaitée
        screen.blit(bonus_collected_text, (10, 90))
        

        # Affiche un message temporaire si un bonus a été collecté récemment
        # "if bonus_collected" vérifie si le joueur a collecté un bonus récemment
        if bonus_collected:
            
            # Crée une surface de texte pour afficher le message "Bonus collecté !"
            # "pygame.font.Font(None, 38).render()" génère le texte avec 
            # une police de taille 38 et une couleur blanche (WHITE)
            bonus_text = pygame.font.Font(None, 38).render("Bonus collecté !", True, WHITE)
            
            # Affiche le message de bonus collecté au centre de l'écran
            # "screen.blit(bonus_text, (WIDTH // 2 - 100, HEIGHT // 2))" 
            # centre le texte horizontalement en soustrayant 100 pixels
            screen.blit(bonus_text, (WIDTH // 2 - 100, HEIGHT // 2))
            
            
            # Vérifie si plus d'une secondes (1000 millisecondes) 
            # se sont écoulées depuis la collecte du bonus
            # "pygame.time.get_ticks() - bonus_display_timer" 
            # calcule le temps écoulé depuis l'apparition du message
            # Si ce temps dépasse 1000 millisecondes, le message de bonus collecté disparaît
            if pygame.time.get_ticks() - bonus_display_timer > 1000:
                
                # Réinitialise "bonus_collected" à False pour ne plus afficher le message
                bonus_collected = False

        # Affiche le score et le niveau actuel du joueur sur l'écran
        # Crée une surface de texte pour afficher le score du 
        # joueur avec une police de taille 38
        # "pygame.font.Font(None, 38).render()" 
        # génère le texte "Score : " suivi de la valeur actuelle du score, en blanc (WHITE)
        score_text = pygame.font.Font(None, 38).render(f"Score : {score}", True, WHITE)
        
        # Crée une surface de texte pour afficher le niveau actuel du joueur 
        # avec une police de taille 38
        # "pygame.font.Font(None, 38).render()" 
        # génère le texte "Niveau : " suivi de la valeur actuelle du niveau, en blanc (WHITE)
        level_text = pygame.font.Font(None, 38).render(f"Niveau : {level}", True, WHITE)
        
        # Affiche le texte du score en haut à gauche de l'écran aux coordonnées (10, 10)
        # "screen.blit(score_text, (10, 10))" place le texte du score dans le coin supérieur gauche
        screen.blit(score_text, (10, 10))
        
        # Affiche le texte du niveau juste en dessous du score, aux coordonnées (10, 50)
        # "screen.blit(level_text, (10, 50))" 
        # place le texte du niveau sous le score pour garder l'affichage organisé
        screen.blit(level_text, (10, 50))


        # Affiche le message "Invincible !" si l'effet d'invincibilité est activé
        # "if invincible" vérifie si le joueur est actuellement invincible
        if invincible:
            
            # Crée une surface de texte pour afficher "Invincible !" 
            # avec une police de taille 38
            # "pygame.font.Font(None, 38).render()" 
            # génère le texte en jaune doré (255, 215, 0) pour indiquer l'invincibilité
            invincible_text = pygame.font.Font(None, 38).render("Invincible !", True, (255, 215, 0))
            
            # Affiche le texte "Invincible !" dans le coin supérieur droit de l'écran, 
            # aux coordonnées (WIDTH - 150, 10)
            # "screen.blit(invincible_text, (WIDTH - 150, 10))" 
            # place le texte à droite de l'écran, 150 pixels avant le bord
            screen.blit(invincible_text, (WIDTH - 150, 10))
            
        
        # Affiche le message "Obstacles ralentis !" si l'effet de ralentissement 
        # des obstacles est activé
        # "if slow_obstacles" vérifie si l'effet de ralentissement est actif
        if slow_obstacles:
            
            # Crée une surface de texte pour afficher "Obstacles ralentis !" 
            # avec une police de taille 38
            # "pygame.font.Font(None, 38).render()" 
            # génère le texte en orange (255, 165, 0) pour indiquer le ralentissement
            slow_text = pygame.font.Font(None, 38).render("Obstacles ralentis !", True, (255, 165, 0))
            
            # Affiche le texte "Obstacles ralentis !" 
            # dans le coin supérieur droit de l'écran, aux coordonnées (WIDTH - 250, 50)
            # "screen.blit(slow_text, (WIDTH - 250, 50))" 
            # place le texte un peu plus bas pour éviter le chevauchement avec "Invincible !"
            screen.blit(slow_text, (WIDTH - 250, 50))


        # Rafraîchit l'écran pour afficher toutes les mises à jour visuelles du jeu
        # "pygame.display.flip()" met à jour l'écran pour refléter les modifications effectuées
        # Cela inclut les déplacements, les changements de score, les effets visuels, etc.
        pygame.display.flip()
        
        
        # Limite la vitesse de la boucle de jeu à 60 images par seconde (FPS) 
        # pour garantir un déroulement fluide
        # "clock.tick(60)" contrôle le nombre d'images par seconde (60 ici) 
        # pour une expérience fluide
        # Cela empêche le jeu de s'exécuter trop vite, rendant l'action plus stable et prévisible
        clock.tick(60)
        

    # Quitte Pygame une fois que la boucle principale du jeu est terminée
    # "pygame.quit()" ferme proprement toutes les fonctionnalités de Pygame 
    # et libère les ressources utilisées
    pygame.quit()
    

# Fonction pour afficher l'écran de fin de partie
# Elle montre le score final, le niveau atteint et le nombre total de bonus collectés
def display_game_over(final_score, final_level, final_bonus):
    
    # Remplit l'écran de noir pour préparer l'affichage des messages de fin de partie
    # "screen.fill(BLACK)" applique la couleur noire à toute la surface de l'écran
    screen.fill(BLACK)
    
    # Création des polices de caractères pour les messages de fin de partie
    # "pygame.font.Font(None, taille)" crée une police avec la taille spécifiée
    game_over_font = pygame.font.Font(None, 92)  # Police pour le message "GAME OVER !"
    message_font = pygame.font.Font(None, 48)  # Police pour les informations de score et de niveau
    small_font = pygame.font.Font(None, 42)  # Police pour le message de rejouer ou quitter

    # Messages de fin de partie
    # "game_over_font.render()" crée une surface de texte avec le message "GAME OVER !" en rouge
    game_over_text = game_over_font.render("GAME OVER !", True, (255, 0, 0))
    
    # "message_font.render()" crée une surface de texte pour afficher le score final en blanc
    score_text = message_font.render(f"Votre score final est de : {final_score}", True, OR)
    
    # Crée une surface de texte pour afficher le niveau atteint en blanc
    level_text = message_font.render(f"Vous avez atteint le niveau : {final_level}", True, WHITE)
    
    # Crée une surface de texte pour afficher le nombre total de bonus collectés en blanc
    bonus_text = message_font.render(f"Nombre de bonus collectés : {final_bonus}", True, WHITE)
    
    # Crée une surface de texte pour demander au joueur s'il veut rejouer ou quitter en blanc
    replay_text = small_font.render("Voulez-vous rejouer (R) ou quitter (Q) ?", True, OR)

    # Affichage des messages de fin de partie sur l'écran
    # "screen.blit()" place chaque message à une position spécifique sur l'écran
    
    
    # Affiche le message "GAME OVER !" au centre de l'écran, légèrement au-dessus du milieu
    # "screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))" 
    # place le texte en fonction de la taille de l'écran :
    # - "WIDTH // 2" représente la moitié de la largeur totale de l'écran 
    # (c'est le centre horizontal)
    # - On soustrait 200 pixels pour centrer horizontalement le texte "GAME OVER !" 
    # (ajusté selon la largeur du texte)
    # - "HEIGHT // 2" représente la moitié de la hauteur totale de l'écran 
    # (c'est le centre vertical)
    # - On soustrait 100 pixels pour placer le texte légèrement au-dessus 
    # du centre vertical de l'écran
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
    
    
    
    # Affiche le score final juste en dessous du message "GAME OVER !"
    # "screen.blit(score_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))" 
    # positionne le texte du score par rapport au centre :
    # - "WIDTH // 2 - 200" centre horizontalement le texte en soustrayant 200 pixels 
    # pour que le texte soit bien aligné
    # - "HEIGHT // 2 - 30" place le score légèrement sous le texte "GAME OVER !", 
    # 30 pixels plus bas que le centre
    screen.blit(score_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))
    
    
    
    # Affiche le niveau atteint sous le score pour garder une structure verticale
    # "screen.blit(level_text, (WIDTH // 2 - 200, HEIGHT // 2 + 30))" 
    # positionne le texte du niveau :
    # - "WIDTH // 2 - 200" centre horizontalement le texte de la même manière 
    # que les autres lignes
    # - "HEIGHT // 2 + 30" place le texte du niveau 30 pixels plus bas que le centre, 
    # sous le score
    screen.blit(level_text, (WIDTH // 2 - 200, HEIGHT // 2 + 30))
    
    
    
    # Affiche le nombre de bonus collectés sous le niveau pour respecter l'alignement vertical
    # "screen.blit(bonus_text, (WIDTH // 2 - 200, HEIGHT // 2 + 90))" 
    # positionne le texte des bonus :
    # - "WIDTH // 2 - 200" garde le texte centré horizontalement
    # - "HEIGHT // 2 + 90" place le texte des bonus 90 pixels sous le centre, sous le niveau, 
    # en gardant une certaine distance
    screen.blit(bonus_text, (WIDTH // 2 - 200, HEIGHT // 2 + 90))
    
    
    # Affiche le message pour rejouer ou quitter encore plus bas pour que tout soit bien organisé
    # "screen.blit(replay_text, (WIDTH // 2 - 200, HEIGHT // 2 + 150))" 
    # place le texte d'option en bas de la liste :
    # - "WIDTH // 2 - 200" continue d'aligner tout le texte horizontalement au centre
    # - "HEIGHT // 2 + 150" positionne ce dernier message à 150 pixels 
    # sous le centre pour indiquer les options
    screen.blit(replay_text, (WIDTH // 2 - 200, HEIGHT // 2 + 150))

    # Met à jour l'écran pour afficher tous les messages de fin de partie
    pygame.display.flip()

    # Attente de l'entrée de l'utilisateur pour rejouer ou quitter le jeu
    waiting = True

    # Boucle pour gérer les événements pendant l'attente de l'entrée du joueur
    # Cette boucle vérifie continuellement les actions de l'utilisateur 
    # (comme appuyer sur une touche ou fermer la fenêtre)
    # tant que "waiting" est True, c'est-à-dire tant que le jeu attend une réponse 
    # du joueur pour continuer ou quitter
    while waiting:
        
        # Parcourt tous les événements détectés par Pygame, 
        # comme les clics de souris ou les frappes de clavier
        # "pygame.event.get()" récupère une liste de tous les événements récents 
        # pour les traiter un par un
        for event in pygame.event.get():
            
            
            # Vérifie si l'événement est de type "QUIT", 
            # ce qui signifie que l'utilisateur veut fermer la fenêtre du jeu
            # "event.type == pygame.QUIT" 
            # détecte si l'utilisateur clique sur la croix pour fermer la fenêtre
            if event.type == pygame.QUIT:
                
                # Quitte Pygame et ferme proprement la fenêtre du jeu
                # "pygame.quit()" libère toutes les ressources utilisées par Pygame
                # "sys.exit()" termine le programme pour fermer complètement l'application
                pygame.quit()
                sys.exit()
                

            # Vérifie si l'événement est de type "KEYDOWN", 
            # ce qui signifie qu'une touche du clavier a été enfoncée
            elif event.type == pygame.KEYDOWN:
                
                # Si la touche "r" est pressée, le jeu redémarre
                # "event.key == pygame.K_r" vérifie si la touche pressée est la lettre "r" 
                # (pour redémarrer)
                if event.key == pygame.K_r:
                    
                    # Met la variable "waiting" sur False pour arrêter la boucle d'attente
                    # Cela signifie que le jeu peut continuer et que l'attente 
                    # de l'entrée du joueur est terminée
                    waiting = False 
                    
                    # Appelle la fonction principale "main()" pour recommencer 
                    # le jeu depuis le début
                    # En relançant "main()", le jeu se réinitialise et démarre une nouvelle partie 
                    main()  
                    

                # Si la touche "q" est pressée, quitte le jeu
                # "event.key == pygame.K_q" vérifie si la touche pressée est la lettre "q" 
                # (pour quitter)
                elif event.key == pygame.K_q:
                    
                    # Quitte Pygame et ferme proprement la fenêtre du jeu
                    # "pygame.quit()" libère toutes les ressources de Pygame
                    # "sys.exit()" termine le programme pour quitter l'application
                    pygame.quit()
                    sys.exit()

# Charge le son de victoire qui est joué lors de la fin du combat final
# "pygame.mixer.Sound()" charge le fichier audio "son_fin_jeu.wav" pour l'utiliser plus tard
victory_sound = pygame.mixer.Sound(resource_path("son_fin_jeu.mp3"))

# Définit le volume du son de victoire pour qu'il soit au maximum (1.0 est le volume maximal)
# Vous pouvez ajuster ce niveau de volume si nécessaire
victory_sound.set_volume(1.0)  # Définissez le volume si nécessaire


# Fonction pour afficher l'écran du niveau final
# Affiche un message de félicitations et le score final pour indiquer la fin du jeu
def display_final_level_screen():
    
    # Arrête la musique de fond pour faire place au son de victoire
    # "pygame.mixer.music.stop()" arrête toute musique qui est actuellement en cours de lecture en arrière-plan
    pygame.mixer.music.stop()

    # Joue le son de victoire en boucle pour célébrer l'accomplissement du niveau final
    # "victory_sound.play(-1)" fait jouer le son de victoire en répétition infinie 
    # (-1 signifie "en boucle")
    victory_sound.play(-1)
    
    # Remplit l'écran avec une couleur noire pour nettoyer l'affichage
    # "screen.fill(BLACK)" applique la couleur noire sur tout l'écran 
    # pour préparer l'affichage des messages
    screen.fill(BLACK)
    
    # Charge l'image de la coupe (trophée) pour la montrer à la fin du jeu
    # "pygame.image.load()" charge une image depuis un fichier (ici "cup.png")
    # "resource_path()" aide à localiser correctement le fichier image
    # "convert_alpha()" permet de gérer la transparence de l'image pour 
    # qu'elle s'affiche proprement
    cup_image = pygame.image.load(resource_path("cup.png")).convert_alpha()
    
    # Redimensionne l'image de la coupe pour qu'elle mesure 
    # 400 pixels de large et 300 pixels de haut
    # "pygame.transform.smoothscale()" ajuste la taille de l'image 
    # pour s'intégrer visuellement à l'écran
    cup_image = pygame.transform.smoothscale(cup_image, (400, 300))
    
    # Crée un rectangle autour de l'image de la coupe et centre ce rectangle sur l'écran
    # "get_rect()" génère un rectangle basé sur les dimensions de l'image de la coupe
    # "center=(WIDTH // 2, HEIGHT // 2 - 150)" 
    # place ce rectangle au centre horizontalement, légèrement vers le haut
    cup_rect = cup_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    # Création des polices pour les messages de félicitations
    # "pygame.font.Font(None, 48)" crée une police de taille 48 pour le texte affiché
    font = pygame.font.Font(None, 48)
    
    # Crée le texte de félicitations "Bravo, fin du combat final !" en couleur orange
    # "font.render()" génère une image de texte avec le contenu et la couleur spécifiés
    congrats_text = font.render("Bravo, vous avez gagné le combat final !", True, OR)
    
    # Crée le texte pour afficher le score final du joueur en blanc
    # "final_score_text" montrera la valeur de "score" à la fin du jeu
    final_score_text = font.render(f"Votre score final est de : {score}", True, WHITE)
    
    # Crée le texte pour afficher le niveau final atteint par le joueur en blanc
    # "final_level_text" montrera la valeur de "level" à la fin du jeu
    final_level_text = font.render(f"Vous avez atteint le niveau : {level}", True, WHITE)
    
    # Crée le texte pour afficher le nombre total de bonus collectés par le joueur en blanc
    # "final_bonus_text" montrera le nombre total de bonus ramassés par le joueur
    final_bonus_text = font.render(f"Nombre de bonus collectés : {bonus_collected_count}", True, WHITE)

    # Affiche les messages de félicitations et l'image de la coupe sur l'écran
    # "screen.blit()" place chaque élément (image ou texte) à des positions spécifiques
    
    # Affiche l'image de la coupe à sa position centrée définie par "cup_rect"
    screen.blit(cup_image, cup_rect)
    
    # Affiche le message de félicitations "Bravo, fin du combat final !" 
    # juste sous l'image de la coupe
    # "screen.blit(congrats_text, (WIDTH // 2 - 250, HEIGHT // 2 + 10))" 
    # positionne le texte de félicitations de cette manière :
    # - "WIDTH // 2" représente la moitié de la largeur de l'écran, 
    # ce qui nous donne le centre horizontal de l'écran
    # - "WIDTH // 2 - 250" permet de centrer le texte horizontalement 
    # en ajustant sa position de 250 pixels vers la gauche
    #   pour qu'il soit bien aligné au centre, adapté à la largeur du texte
    # - "HEIGHT // 2" représente la moitié de la hauteur de l'écran, donc le centre vertical
    # - "HEIGHT // 2 + 10" place le texte légèrement en dessous du centre 
    # (10 pixels sous la ligne centrale)
    screen.blit(congrats_text, (WIDTH // 2 - 250, HEIGHT // 2 + 10))
    
    
    
    # Affiche le texte du score final sous le message de félicitations
    # "screen.blit(final_score_text, (WIDTH // 2 - 250, HEIGHT // 2 + 60))" 
    # positionne le score de cette manière :
    # - "WIDTH // 2 - 250" garde le texte centré horizontalement, 
    # en utilisant le même ajustement de 250 pixels vers la gauche
    # - "HEIGHT // 2 + 60" place le texte du score 60 pixels 
    # plus bas que la ligne centrale, sous le texte de félicitations,
    #   pour créer un espace visuel entre les deux
    screen.blit(final_score_text, (WIDTH // 2 - 250, HEIGHT // 2 + 60))
    
    
    
    # Affiche le texte du niveau final sous le score pour garder une structure verticale organisée
    # "screen.blit(final_level_text, (WIDTH // 2 - 250, HEIGHT // 2 + 110))" 
    # positionne le texte du niveau :
    # - "WIDTH // 2 - 250" continue de centrer le texte horizontalement
    # - "HEIGHT // 2 + 110" place le texte du niveau 110 pixels sous la ligne centrale, 
    # juste en dessous du score
    #   et crée ainsi un espacement de 50 pixels avec le texte du score
    screen.blit(final_level_text, (WIDTH // 2 - 250, HEIGHT // 2 + 110))
    
    
    
    # Affiche le texte du nombre de bonus collectés sous le texte 
    # du niveau pour garder l'alignement vertical
    # "screen.blit(final_bonus_text, (WIDTH // 2 - 250, HEIGHT // 2 + 160))" 
    # place le texte des bonus :
    # - "WIDTH // 2 - 250" garde le texte centré horizontalement, 
    # pour un alignement uniforme avec les autres textes
    # - "HEIGHT // 2 + 160" place le texte des bonus 160 pixels sous la ligne centrale, 
    # sous le texte du niveau,
    # créant ainsi un espacement de 50 pixels supplémentaire avec le niveau 
    # pour une bonne lisibilité
    screen.blit(final_bonus_text, (WIDTH // 2 - 250, HEIGHT // 2 + 160))

    # Met à jour l'écran pour afficher tous les messages et l'image de la coupe
    pygame.display.flip()
    
    # Fait une pause de 3 secondes pour permettre au joueur 
    # de voir les messages de fin de partie
    pygame.time.delay(3000)

    # Prépare le texte de question pour demander au joueur s'il veut rejouer ou quitter
    # "font.render()" crée une surface de texte avec la question, en couleur orange
    replay_text = font.render("Voulez-vous rejouer (R) ou quitter (Q) ?", True, OR)
    
    # Définit la transparence initiale à 0 pour créer un effet de fondu
    alpha = 0
    
    # Boucle pour augmenter progressivement la transparence du texte de question
    while alpha <= 255:
        # Remplit l'écran de noir pour rafraîchir l'affichage
        screen.fill(BLACK)
        
        # Affiche à nouveau l'image de la coupe à sa position d'origine
        screen.blit(cup_image, cup_rect)
        
        # Affiche le message de félicitations "Bravo, fin du combat final !" 
        # légèrement sous le centre de l'écran
        # "screen.blit(congrats_text, (WIDTH // 2 - 250, HEIGHT // 2 + 10))" 
        # place le texte en fonction des dimensions de l'écran :
        # - "WIDTH // 2" est la moitié de la largeur de l'écran, 
        # représentant le centre horizontal
        # - "WIDTH // 2 - 250" ajuste la position de 250 pixels 
        # vers la gauche pour centrer le texte "Bravo, fin du combat final !"
        #   en tenant compte de sa largeur, afin qu’il soit bien aligné au centre de l'écran
        # - "HEIGHT // 2" est la moitié de la hauteur de l'écran, 
        #    représentant le centre vertical
        # - "HEIGHT // 2 + 10" place le texte légèrement sous le centre 
        # (10 pixels en dessous de la ligne centrale)
        screen.blit(congrats_text, (WIDTH // 2 - 250, HEIGHT // 2 + 10))
        
        
        # Affiche le texte du score final juste en dessous du message de félicitations
        # "screen.blit(final_score_text, (WIDTH // 2 - 250, HEIGHT // 2 + 60))" 
        # positionne le texte du score :
        # - "WIDTH // 2 - 250" continue de centrer horizontalement le texte 
        # du score en gardant le même décalage de 250 pixels
        # - "HEIGHT // 2 + 60" place le texte du score 60 pixels 
        # en dessous de la ligne centrale, soit 50 pixels sous le texte de félicitations
        #   pour maintenir une bonne lisibilité et un espacement visuel constant
        screen.blit(final_score_text, (WIDTH // 2 - 250, HEIGHT // 2 + 60))
        
        
        # Affiche le texte du niveau final en dessous du score, pour garder 
        # une organisation en colonne
        # "screen.blit(final_level_text, (WIDTH // 2 - 250, HEIGHT // 2 + 110))" 
        # positionne le texte du niveau :
        # - "WIDTH // 2 - 250" aligne toujours le texte horizontalement 
        # avec les autres, au centre
        # - "HEIGHT // 2 + 110" place le texte du niveau 110 pixels 
        # sous la ligne centrale, donc 50 pixels sous le texte du score
        #   pour un espacement visuel agréable et une présentation ordonnée
        screen.blit(final_level_text, (WIDTH // 2 - 250, HEIGHT // 2 + 110))
        
        
        # Affiche le texte du nombre de bonus collectés sous le texte du niveau, 
        # pour garder la présentation alignée
        # "screen.blit(final_bonus_text, (WIDTH // 2 - 250, HEIGHT // 2 + 160))" 
        # positionne le texte des bonus :
        # - "WIDTH // 2 - 250" aligne le texte des bonus avec les autres textes 
        # pour un centrage horizontal uniforme
        # - "HEIGHT // 2 + 160" place le texte des bonus 160 pixels sous la ligne centrale, 
        # c'est-à-dire 50 pixels sous le niveau
        #   pour maintenir l'espacement cohérent entre chaque ligne de texte
        screen.blit(final_bonus_text, (WIDTH // 2 - 250, HEIGHT // 2 + 160))
        
        # Applique la transparence actuelle au texte de question pour le fondu
        # "set_alpha(alpha)" change la transparence du texte, 
        # de complètement transparent (0) à opaque (255)
        replay_text.set_alpha(alpha)
        
        
        # Affiche le texte de question "Voulez-vous rejouer (R) ou quitter (Q) ?" 
        # sous les autres messages
        # "screen.blit(replay_text, (WIDTH // 2 - 250, HEIGHT // 2 + 210))" 
        # place ce texte de la manière suivante :
        # - "WIDTH // 2" est la moitié de la largeur totale de l'écran, 
        # ce qui représente le centre horizontal
        # - "WIDTH // 2 - 250" décale la position de 250 pixels 
        # vers la gauche pour centrer précisément le texte
        #   "Voulez-vous rejouer (R) ou quitter (Q) ?" en tenant compte de sa largeur
        # - "HEIGHT // 2" est la moitié de la hauteur de l'écran, donc le centre vertical
        # - "HEIGHT // 2 + 210" place le texte 210 pixels 
        # en dessous de la ligne centrale de l'écran, sous tous les autres messages affichés,
        #   créant ainsi un espacement uniforme avec les textes au-dessus 
        # set permettant de le lire en dernier
        screen.blit(replay_text, (WIDTH // 2 - 250, HEIGHT // 2 + 210))
        
        # Rafraîchit l'écran pour montrer le texte de question avec la transparence modifiée
        pygame.display.flip()
        
        # Augmente la transparence de 5 à chaque cycle pour créer un effet de fondu progressif
        alpha += 5
        
        # Fait une courte pause de 50 millisecondes avant 
        # la prochaine augmentation de transparence
        pygame.time.delay(50)

    # Initialise une variable pour gérer l'attente de l'entrée de l'utilisateur 
    # (rejouer ou quitter)
    waiting = True

    # Boucle pour vérifier les entrées de l'utilisateur pendant l'attente
    while waiting:
        # Parcourt tous les événements de Pygame pour détecter les interactions utilisateur
        for event in pygame.event.get():
            # Si l'utilisateur ferme la fenêtre, arrête le jeu correctement
            if event.type == pygame.QUIT:
                victory_sound.stop()  # Arrête le son de victoire
                pygame.quit()
                sys.exit()

            # Vérifie si une touche a été enfoncée
            elif event.type == pygame.KEYDOWN:
                
                # Si la touche "r" est pressée, le jeu redémarre
                if event.key == pygame.K_r:
                    # Arrête le son de victoire et relance la musique de fond
                    victory_sound.stop()
                    pygame.mixer.music.play(-1)  # Joue la musique de fond en boucle
                    waiting = False  # Arrête la boucle d'attente
                    main()  # Relance la fonction principale du jeu pour rejouer

                # Si la touche "q" est pressée, quitte le jeu
                elif event.key == pygame.K_q:
                    victory_sound.stop()  # Arrête le son de victoire
                    pygame.quit()
                    sys.exit()


# Tentative de faire défiler le texte, de lancer le décompte et le jeu principal
# La structure "try...except" permet de gérer les erreurs : 
# le code dans "try" est exécuté normalement,
# mais si une erreur survient, le programme passe dans "except" 
# pour gérer cette erreur sans planter le programme
try:
    
    # Appelle la fonction pour faire défiler le texte de l'histoire avant de démarrer le jeu
    # "scroll_text()" est une fonction qui affiche un texte défilant 
    # (ici, l'introduction de notre jeu)
    scroll_text()
    
    
    # Appelle la fonction de compte à rebours avant de lancer le jeu
    # "countdown()" affiche un décompte (5, 4, 3, 2, 1) 
    # pour donner le temps au joueur de se préparer avant le début du jeu
    countdown()
    
    
    # Appelle la fonction principale "main()" pour démarrer le jeu
    # "main()" est la fonction qui gère tout le gameplay, 
    # les interactions et les événements du jeu  
    main()
    
# Boucle pour garder la fenêtre ouverte après la fin du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

# En cas d'erreur dans les fonctions précédentes, l'exception est capturée ici
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    input("Appuyez sur Entrée pour fermer...")