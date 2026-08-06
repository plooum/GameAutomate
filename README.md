# ⚔️ Valheim Automation Tools

Script Python d'automatisation des tâches répétitives pour **Valheim**.

---

## 📌 Fonctionnalités

- 🤺 **XP des armes :** Entraînement automatique face à un mannequin d'entraînement.
- 🌱 **Jardinage automatique :** Plantation et récolte des cultures.

---

## 🛠️ Prérequis & Dépendances

### 1. Outils système & Python
#### Linux (Testé sous Mint)
- **`xdotool`** : Gestion des interactions système sous Linux.
  ```bash
  sudo apt install xdotool
  ```
- Module python **`pynput`** : Emission d'événements clavier/souris (géré par uv).
#### Windows
- Module python **`pynput`** : Emission des événements clavier/souris (géré par uv).
- Module python **`pydirectinput`** : Emission des événements souris (géré par uv).

### 2. Gestionnaire de projet (`uv`)
Ce projet utilise **`uv`** pour la gestion de l'environnement virtuel et des dépendances.
- Pour installer `uv`, consultez la [Documentation officielle d'installation](https://docs.astral.sh/uv/getting-started/installation/).

---

## 🚀 Lancement de l'automate

Utilisez les scripts fournis à la racine du projet selon votre système d'exploitation :

- **Sous Linux :**
  ```bash
  ./start.sh
  ```
- **Sous Windows :**
  ```cmd
  start.cmd
  ```

*Alternativement, vous pouvez lancer le script directement via `uv` :*
```bash
uv run main.py
```

---

## ⚙️ Configuration & Réglages

> ⚠️ **Disposition du clavier :** Le script est préréglé pour un clavier **AZERTY**. Si vous utilisez une autre disposition (QWERTY, etc.), modifiez les constantes situées en haut du script.

### 🔑 Constantes Clavier (AZERTY)

```python
TOUCHE_UTILISER           = "e"
TOUCHE_AVANCER            = "z"
TOUCHE_RECULER            = "s"
TOUCHE_MARCHER_LENTEMENT  = "c"
TOUCHE_ITEM_1             = "&"
TOUCHE_ITEM_2             = "é"
TOUCHE_ITEM_3             = '"'
TOUCHE_ITEM_4             = "'"
TOUCHE_ITEM_5             = "("
TOUCHE_ITEM_6             = "-"
TOUCHE_ITEM_7             = "è"
TOUCHE_ITEM_8             = "_"
TOUCHE_ULTI               = "f"
```

---

## ⛏️ Mise en place du terrain
- Préparez un couloir d'environ 12m de long en terre (à l'aide de la houe) pour monter des murs indestructibles.
- Fermez une extrémité du couloir avec un mur en terre.
- Mettez un mannequin face au couloir et dos à ce mur.
![Couloir](docs/images/couloir.jpg)
- Du côté ouvert, faites un entonnoire avec 2 ou 3 poutres de bois et placez une forge (ou autre établi permettant de réparer vos armes).
![Couloir](docs/images/forge.jpg)

## 🎯 Premier Lancement (Calibrage)

Avant d'utiliser les automates, vous devez calibrer le déplacement de la souris et les coordonnées du bouton réparer de la forge en modifiant les variables en haut du script :

1. **Demi-tour horizontal :**  
   Ajustez `NOMBRE_PIXEL_DEMI_TOUR_HORIZONTAL`  
   *Test :* Appuyez 2 fois sur <kbd>F6</kbd> (2 demi-tours). Le curseur doit revenir exactement à son point d'origine.

2. **Ajustement vertical :**  
   Ajustez `NOMBRE_PIXEL_QUART_TOUR_VERTICAL`  
   *Test :* Appuyez sur <kbd>F10</kbd>. Le regard de votre personnage doit passer de l'horizon à ses pieds (approcximativement).

3. **Bouton de réparation :**  
   Ajustez `POS_BTN_REPARER_X` et `POS_BTN_REPARER_Y`  
   *Test :* Placez-vous sur une forge et appuyez sur <kbd>F11</kbd>. Le curseur doit se positionner précisément sur le bouton **Réparer**.

---

## 📖 Modes d'Utilisation

### 🗡️ Mode Farming des Armes
#### Préparation de l'inventaire :
- Placez vos **armes** dans les slots **`3`** et **`4`**.
  - *Arme à une main :* Mettez une seule arme en `3` ou `4` et laissez l'autre slot vide.
- Placez la **nourriture** dans les slots **`7`** et **`8`** (ex: Miel, Viande de sanglier).
  - *Sans nourriture :* Laissez les slots `7` et `8` vides.
- **Équipement recommandé :** Broche de fer + nourriture.

#### Positionnement :
1. Placez-vous dans le cadre de farm face au mannequin d'entraînement.
2. Visez le sol juste devant vous.
3. Appuyez sur <kbd>F6</kbd> pour faire un demi-tour : la forge doit être visée (le message *"Utiliser la forge"* doit apparaître).
4. Appuyez de nouveau sur <kbd>F6</kbd> pour vous retourner face au mannequin.
5. Équipez vos armes (slots `3` et `4`) et démarrez l'automate.

---

### 🌱 Mode Farming du Jardin

#### Préparation :
1. Équipez-vous du **Cultivateur** (et sélectionnez le type de culture via le clic droit) ou de la **Faux**.
2. Utilisez les touches de raccourci <kbd>F3</kbd> et <kbd>F4</kbd> pour régler :
   - Le nombre d'actions par rangée.
   - Le nombre total d'actions.
3. Positionnez-vous au début de la rangée, visez approximativement la fin de la première rangée.
4. Pour planter, appuyez sur <kbd>F10</kbd> afin que le personnage regarde à ses pieds.

---

## ⌨️ Commandes

| Touche | Action | Description |
| :---: | :--- | :--- |
| <kbd>F8</kbd> | **Démarrer / Arrêter** | Active ou désactive l'automatisation en cours. |
| <kbd>F7</kbd> | **Changer d'automate** | Bascule entre le mode Armes et le mode Jardin. |
| <kbd>F3</kbd> | **Réglage Jardin** | Modifie le nombre d'actions par rangée. |
| <kbd>F4</kbd> | **Réglage Jardin** | Modifie le nombre total d'actions. |
| <kbd>F6</kbd> | **Test Demi-tour** | Effectue un demi-tour à 180° (pour tester la calibration). |
| <kbd>F10</kbd> | **Test Regard** | Alterne le regard entre l'horizon et les pieds (pour tester la calibration). |
| <kbd>F11</kbd> | **Test Réparation** | Déplace la souris sur le bouton Réparer de la forge (pour tester la calibration). |