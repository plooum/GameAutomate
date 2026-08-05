Ce sctipt permet d'automatiser des tâches dans Valheim sur Linux :
 - XP des armes face à un manequin
 - Jardinage (plantation et recolte)

 Dépendences : 
  - Nécessite un logiciel externe : xdotool sous Linux
  - python3-pynput
 
 Notes : pour un fonctionnement sous Windows ou Mac, il faudra adapter la méthode Inputs.deplacer_souris_xdotool
 
[Premier Lancement]
En haut de ce script :
 - Modifier la variable NOMBRE_PIXEL_DEMI_TOUR_HORIZONTAL : lors de 2 appuies sur F6 (2 demi-tours), le curseur doit revenir exactement au même point
 - Modifier la variable NOMBRE_PIXEL_QUART_TOUR_VERTICAL : lors d'un appui sur F10, le regard du personnage passe de l'horizon à ses pieds (à peu près)
 - Modifier les variables POS_BTN_REPARER_X et POS_BTN_REPARER_Y : utiliser une forge et appuyer sur F11, le curseur doit se positionner sur le bouton réparer

[Mode farming des armes]
 - Armes en 3 et 4
 - Pour les armes à une main, ne mettre qu'une arme dans 3 ou 4 et garder l'autre slot vide
 - Nourriture en 7 et 8
 - Sans nourriture, conserver les slots 7 et 8 vide
 Positionnement :
 - Se positionner dans le cadre de farm face au mannequin
 - Viser le sol devant soi
 - Appuyer sur F6 et s'assurer que la forge est visée après un demi-tour (le bouton "utiliser la forge" doit être visible)
 - Appuer sur F6 pour se retourner
 Equipement
 - S'équiper des armes en 3 et 4
 - Je conseille fortement l'utilisation de la broche de fer et de nourriture (miel / viande de sanglier par exemple)

[Mode farming du jardin]
 - S'équiper du cultivateur et sélectionner le type de plantation via le clic droit ou s'équiper de la faux
 - Utiliser les options F3 et F4 afin de configurer le nombre d'actions par rangée et le nombre d'actions total
 - Viser à peu près la fin de la permière rangée et, pour planter, appuyer sur F10 pour que le personnage regarde ses pieds

Liste des commandes :
 - Pilotage de l'automate
F8  : Démarrer / Arrêter l'automatisation
F7  : Changer d'automate
 - Changement des réglages
F3  : Jardin - Changer le nombre d'actions par rangée (défaut:{self.settings_jardin.jardin_taille_rangee})
F4  : Jardin - Changer le nombre d'actions total (défaut:{self.settings_jardin.jardin_nb_total})
 - Tests et positionnement
F6  : Demie tour
F10 : Lever / baisser le regard
F11 : Déplacer la souris sur le bouton réparer
