import time
import threading
import subprocess
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, Listener, KeyCode
from itertools import cycle
from abc import ABC, abstractmethod
import os

NOMBRE_PIXEL_DEMI_TOUR_HORIZONTAL = 3600
NOMBRE_PIXEL_QUART_TOUR_VERTICAL = 1600
POS_BTN_REPARER_X = 860
POS_BTN_REPARER_Y = -245

class ActionHelper:
    def executer_action(action):
        if action is not None:
            action()

class CancelToken:
    @abstractmethod
    def is_stop_requested(self) -> bool:
        pass

class TimeSleepCancellable:
    def __init__(self, cancel_token: CancelToken):
        self.cancel_token = cancel_token
    
    def attendre(self, attente):
        step = 0.05

        if(attente > step):
            nb_steps = int(attente / step)
            for i in range(nb_steps):
                time.sleep(step)
                if self.cancel_token.is_stop_requested():
                    return
        else:
            time.sleep(attente)

class Event:
    def __init__(self):
        self._handlers = []

    def subscribe(self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)

    def unsubscribe(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)

    def trigger(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)

class Inputs:
    def __init__(self, keyboard, mouse, time: TimeSleepCancellable,vitesse_souris = 30):
        self.keyboard = keyboard
        self.mouse = mouse
        self.vitesse_souris = vitesse_souris
        self.time = time

    def deplacer_souris(self, dx, dy):
        self.deplacer_souris_x(dx)
        self.deplacer_souris_y(dy)

    def deplacer_souris_xdotool(self, dx, dy):
        try:
            subprocess.run(["xdotool", "mousemove_relative", "--", str(dx), str(dy)])
        except Exception as e:
            print(f"[-] Erreur xdotool: {e}")

    def deplacer_souris_x(self, d):
        reverse = 1 if d > 0 else -1
        nb_steps = int(abs(d) / self.vitesse_souris)
        
        for i in range(nb_steps):
            self.deplacer_souris_xdotool(self.vitesse_souris * reverse, 0)

        mod = abs(d) % self.vitesse_souris
        if(mod != 0):
            self.deplacer_souris_xdotool(mod * reverse, 0)
        
        self.time.attendre(0.1)

    def deplacer_souris_y(self, d): 
        reverse = 1 if d > 0 else -1
        nb_steps = int(abs(d) / self.vitesse_souris)
        
        for i in range(nb_steps):
            self.deplacer_souris_xdotool(0, self.vitesse_souris * reverse)

        mod = abs(d) % self.vitesse_souris
        if(mod != 0):
            self.deplacer_souris_xdotool(0, mod * reverse)

        self.time.attendre(0.1)

    def clavier_appuie(self, touche, attente=0.05):
        self.keyboard.press(str(touche))
        self.time.attendre(attente)
        self.keyboard.release(str(touche))

    def souris_clic_gauche(self, temp_attente = 0, release = True):
        self.mouse.press(Button.left)
        if release:
            self.time.attendre(temp_attente)
            self.mouse.release(Button.left)

    def souris_clic_droit(self, temp_attente = 0, release = True):
        self.mouse.press(Button.right)
        if release:
            self.time.attendre(temp_attente)
            self.mouse.release(Button.right)

class Actions :
    def __init__(self, 
                 inputs: Inputs, 
                 time: TimeSleepCancellable, 
                 nb_px_demi_tour = NOMBRE_PIXEL_DEMI_TOUR_HORIZONTAL, 
                 nb_px_quart_tour_vertical = NOMBRE_PIXEL_QUART_TOUR_VERTICAL,
                 pos_btn_reparer_x = POS_BTN_REPARER_X,
                 pos_btn_reparer_y = POS_BTN_REPARER_Y):
        self.inputs = inputs
        self.direction_demie_tour = 1
        self.nb_px_demi_tour = nb_px_demi_tour
        self.nb_px_quart_tour_vertical = nb_px_quart_tour_vertical
        self.pos_btn_reparer_x = pos_btn_reparer_x
        self.pos_btn_reparer_y = pos_btn_reparer_y
        self.recolter = self.planter
        self.direction_baisser_monter_camera = 1
        self.time = time

    def attendre(self, attente):
        self.time.attendre(attente)

    def deplacer_curseur_btn_reparer(self):
        self.inputs.deplacer_souris(dx=self.pos_btn_reparer_x, dy=self.pos_btn_reparer_y)

    def reparer(self):
        self.proteger()
        self.reculer(4)
        self.relacher_proteger()
        self.demi_tour()
        self.attendre(0.2)
        self.utiliser()
        self.deplacer_curseur_btn_reparer()
        for i in range(4):
            self.cliquer(0.1)
        self.utiliser()
        self.demi_tour()
        self.equiper_desequiper_armes()
        self.proteger()
        self.avancer(4)

    def utiliser(self):
        self.inputs.clavier_appuie('e')

    def equiper_desequiper_armes(self):
        self.inputs.clavier_appuie("'")
        self.inputs.clavier_appuie('"')

    def proteger(self, attente = 0):
        if(attente > 0):
            self.inputs.souris_clic_droit(attente)
        else:
            self.inputs.souris_clic_droit(release=False)

    def relacher_proteger(self):
        self.inputs.souris_clic_droit()

    def attaquer(self, attente):
        self.inputs.souris_clic_gauche(attente)
    cliquer = attaquer

    def manger(self):
        self.inputs.clavier_appuie('è')
        self.inputs.clavier_appuie('_')

    def ulti(self):
        self.inputs.clavier_appuie('f')

    def avancer(self, attente):
        self.inputs.clavier_appuie('z',attente)

    def reculer(self, attente):
        self.inputs.clavier_appuie('s',attente)

    def activer_desactiver_marcher_lentement(self):
        self.inputs.clavier_appuie('c')

    def planter(self):
        self.inputs.souris_clic_gauche(0.1)

    def initialiser_sens_demie_tour(self):
        self.direction_demie_tour = 1

    def quart_de_tour(self):
        self.inputs.deplacer_souris(dx=int(self.nb_px_demi_tour/2)*self.direction_demie_tour, dy=0)

    def demi_tour(self):
        self.inputs.deplacer_souris(dx=int(self.nb_px_demi_tour)*self.direction_demie_tour, dy=0)

    def demi_tour_sens_alterne(self, avance_sens_horaire = 1, avance_sens_antihoraire = 0.3):
        self.time.attendre(0.5)
        self.quart_de_tour()
        self.avancer(avance_sens_horaire if self.direction_demie_tour > 0 else avance_sens_antihoraire)
        self.quart_de_tour()
        self.direction_demie_tour = self.direction_demie_tour * -1

    def baisser_monter_camera(self):
        self.inputs.deplacer_souris(dx = 0, dy = self.nb_px_quart_tour_vertical * self.direction_baisser_monter_camera)
        self.direction_baisser_monter_camera = self.direction_baisser_monter_camera * -1

class Automate:
    def __init__(self, name, actions_pre = [], actions_loop = [], actions_post = []):
        self.name = name
        self.actions_pre = actions_pre
        self.actions_loop = actions_loop
        self.actions_post = actions_post

class LooperControler(CancelToken):
    def __init__(self):
        self.running = False
        self.stop_requested = False
        self.num_boucle = 0
        self.on_stop = Event()

    def is_stop_requested(self) -> bool:
        return self.stop_requested

    def action_autorise(self,n, autoriser_premiere_boucle = False):
        if(self.num_boucle == 0 and not autoriser_premiere_boucle):
            return False
        else:
            return self.num_boucle % n == 0

    def arreter_boucles(self):
        self.on_stop.trigger()

    def action_toutes_les_n_boucles(self, n, action, autoriser_premiere_boucle = False, action_sinon = None, action_pre = None, action_post = None):
        if(self.action_autorise(n,autoriser_premiere_boucle)):
            ActionHelper.executer_action(action_pre)
            ActionHelper.executer_action(action)
            ActionHelper.executer_action(action_post)
        else:
            ActionHelper.executer_action(action_sinon)

class Looper:
    def __init__(self, looper_controler: LooperControler, cycleur_automate: cycle):
        self.looper_controler = looper_controler
        self.cycleur_automate = cycleur_automate
        self.automate_en_cours = next(cycleur_automate)
        self.thread_loop = None
        self.looper_controler.num_boucle = 0
        self.looper_controler.on_stop.subscribe(self.arreter_boucles)

    def farm_loop(self):
        print("[+] Boucle d'actions ACTIVÉE")
        self.looper_controler.num_boucle = 0

        print("[*] Actions Pre Boucles")
        for action in self.automate_en_cours.actions_pre:
            action()

        while self.looper_controler.running:
            self.looper_controler.num_boucle += 1
            print("[*] Actions Boucles")
            for action in self.automate_en_cours.actions_loop:
                action()
                if not self.looper_controler.running:
                    break

        self.looper_controler.stop_requested = False

        print("[*] Actions Post Boucles")
        for action in self.automate_en_cours.actions_post:
            action()
        
        print("[-] Boucle d'actions DÉSACTIVÉE")

    def arreter_boucles(self):
        self.looper_controler.running = not self.looper_controler.running
        
        if not self.looper_controler.running:
            self.looper_controler.stop_requested = True

        if (self.thread_loop is not None 
            and self.thread_loop.is_alive() 
            and threading.current_thread() != self.thread_loop):
                self.thread_loop.join()

        if self.looper_controler.running:
            self.looper_controler.stop_requested = False
            self.thread_loop = threading.Thread(target=self.farm_loop)
            self.thread_loop.start()

    def changer_automate(self):
        if not self.looper_controler.running:
            old = self.automate_en_cours
            self.automate_en_cours = next(self.cycleur_automate)
            if(old.name == self.automate_en_cours.name):
                self.automate_en_cours = next(self.cycleur_automate)
            print(f"[+] Changement de mode : {self.automate_en_cours.name}")

class SettingsJardin:
    def __init__(self):
        self.jardin_taille_rangee = 20
        self.jardin_nb_total = 200
        self.cycleur_jardin_rangee = cycle([3,5,10,15,20,30,50])
        self.cycleur_jardin_total = cycle([5,9,50,100,150,200,500,1000,1500,2000])

    def changer_taille_rangee(self):
        self.jardin_taille_rangee = next(self.cycleur_jardin_rangee)

    def changer_taille_totale(self):
        self.jardin_nb_total = next(self.cycleur_jardin_total)

    def __str__(self):
        return f"""Nombre d'actions par rangées : {self.jardin_taille_rangee}
Nombre d'actions totales : {self.jardin_nb_total}
"""

class Program:
    def __init__(self):
        self.looper_controler = LooperControler()
        self.time = TimeSleepCancellable(self.looper_controler)
        self.actions = Actions(Inputs(KeyboardController(), MouseController(), self.time), self.time)
        self.settings_jardin = SettingsJardin()
        self.looper = Looper(self.looper_controler, cycle(self.__build_cycleur_automates()))
        self.__print_prompt()

    def __build_cycleur_automates(self):
        return [
            Automate("Armes", 
                [
                    lambda: self.actions.manger(),
                    lambda: self.actions.attendre(2),
                    lambda: self.actions.proteger(),
                    lambda: self.actions.avancer(4),
                    lambda: self.actions.relacher_proteger(),
                ],
                [
                    lambda: self.actions.attaquer(2),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(5, 
                                                        action = self.actions.reparer),
                    lambda: self.actions.proteger(),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(10, 
                                                        action = self.actions.manger),
                    lambda: self.time.attendre(4),
                    lambda: self.actions.relacher_proteger(),
                ],
                [
                    lambda: self.actions.proteger(),
                    lambda: self.actions.reculer(4),
                    lambda: self.actions.relacher_proteger(),
                ]),
            Automate("Jardin - Plantation",
                [
                    lambda: self.actions.activer_desactiver_marcher_lentement(),
                    lambda: self.actions.initialiser_sens_demie_tour(),
                ],
                [
                    lambda: self.actions.planter(),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(self.settings_jardin.jardin_taille_rangee, 
                                                        action = self.actions.demi_tour_sens_alterne, 
                                                        action_sinon = lambda: self.actions.avancer(0.8)),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(10, 
                                                        action = lambda: self.time.attendre(5)),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(self.settings_jardin.jardin_nb_total, 
                                                        action = self.looper_controler.arreter_boucles)
                ],
                [
                    lambda: self.actions.activer_desactiver_marcher_lentement(),
                ]),
            Automate("Jardin - Recolte",
                [
                    lambda: self.actions.initialiser_sens_demie_tour(),
                ],
                [
                    lambda: self.actions.recolter(),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(self.settings_jardin.jardin_taille_rangee, 
                                                        action = lambda: self.actions.demi_tour_sens_alterne(1.8, 1.5), 
                                                        action_sinon = lambda: self.actions.avancer(1.1), 
                                                        action_pre = self.actions.activer_desactiver_marcher_lentement,  
                                                        action_post =  self.actions.activer_desactiver_marcher_lentement),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(10, 
                                                        action = lambda: self.time.attendre(5)),
                    lambda: self.looper_controler.action_toutes_les_n_boucles(self.settings_jardin.jardin_nb_total, 
                                                        action = self.looper_controler.arreter_boucles)
                ])
        ]

    def on_keyboard_press(self, key):
        if key == Key.f8 or key == KeyCode.from_vk(0x77):
            self.looper.arreter_boucles()

        elif key == Key.f7:
            self.looper.changer_automate()

        elif key == Key.f6:
            if not self.looper_controler.running:
                self.actions.demi_tour()

        elif key == Key.f3:
            self.settings_jardin.changer_taille_rangee()
            print(f"[i] Changer la taille des rangées : {self.settings_jardin.jardin_taille_rangee}")

        elif key == Key.f4:
            self.settings_jardin.changer_taille_totale()
            print(f"[i] Changer la taille totale du jardin : {self.settings_jardin.jardin_nb_total}")

        elif key == Key.f10:
            self.actions.baisser_monter_camera()

        elif key == Key.f11:
            self.actions.deplacer_curseur_btn_reparer()

    def __print_prompt(self):
        print(f"""Ce sctipt permet d'automatiser des tâches dans Valheim sur Linux :
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

""")
        print(f"[i] Automate en cours : {self.looper.automate_en_cours.name}")
        print(f"[i] Paramètrage Jardin : {os.linesep}{self.settings_jardin}")

program = Program()

with Listener(on_press=program.on_keyboard_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("[x] Fin")