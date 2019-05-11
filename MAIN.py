# Imports de librairies
#____________________________________________________

import pygame
import sys
from pygame.locals import *
import random
from BNP import *
#____________________________________________________

	# -> affichage en plein écran

pygame.display.set_caption('GAME')# définition du tytre de la fenetre -> plein écran (inutile) -> preview en bare des taches (ok)

gameDisplay.fill([255,0,255]) # remplissage de la couleur d'arrière-plan (magenta) pour verifier l'abscence de texture
# --------> (si il y a un bout magenta , c'est pas beau et ça se voit)

#pygame.draw.rect(gameDisplay,[20,30,12],(50,50,50,50)) #-> création d'un rectangle


player = TrayClass() # creation d'un objet Tray
player.player = True
computer= TrayClass()

class Player:
	def __init__(self):
		self.ennemy = computer
		self.tray =  player
	def showWhereIAaimed(self):
		xdim = self.tray.dim[0]
		ydim = self.tray.dim[1]
		ni = Lcase *mult * xdim + (Lcase-Lcase)  * (xdim-1)

		for y in range(0,ydim):
			for x in range(0,xdim):
				traycontent = SmallDebugFont.render(self.tray.ShowTray [x][y], True, pygame.Color("Magenta"))
				gameDisplay.blit(traycontent,(self.tray.Gposx + Lcase*x +25,self.tray.Gposy + Lcase*y +25))#


class IA:
	def __init__(self):
		self.checked = [[False]*10 for _ in range(10)]
		self.ennemy = player
		self.aim = (0,0)
		self.aimdir = (0,0)
		self.newshot = True
		self.directional = False
		self.backwards = False
		self.checked = 0
		self.pola = False
		self.ori = False
		self.inc = 0
		self.hit = 0
		self.rstflag = True
	def reset(self, Reshot = False):
		self.backwards = False
		self.directional = False
		self.newshot = True
		self.inc = 0
		self.hit = 0
		self.rstflag = False
		if Reshot :
			self.TURN()

	def reload(self):
		#print("reload")
		x = self.aim[0]
		y = self.aim[1]
		Ori = bool(random.getrandbits(1))
		Pola = bool(random.getrandbits(1))
		if Ori:
			if Pola:y = y+1
			else:y =y-1
		else:
			if Pola:x=x+1
			else:x=x-1
	def TURN(self):
		if self.newshot:
			#print ("newshot")
			x = random.randint(0,9)
			y = random.randint(0,9)

			if self.ennemy.tray [x][y] != "":
				#print ("touché")
				self.aim = (x,y)
				self.newshot = False

		elif self.directional:


			#print ("Directional  " + str(self.inc ))
			x = self.aim[0]
			y = self.aim[1]
			Xinc =  self.aimdir[0] - self.aim[0]
			Yinc =  self.aimdir[1] - self.aim[1]

#self.inc = self.inc+1

			if  (x * Xinc+2*self.inc)> 9 or (x * Xinc+2*self.inc)<0 or (y * Yinc+2*self.inc)>9 or(y * Yinc+2*self.inc)<0:
				if self.backwards :
					self.reset(True)
				self.backwards = True

				#print("directional ovf Fcheck")
			if self.backwards:
				#print("backwards")
				if self.rstflag :
					#print("no rst flag")
					if (x * -Xinc*self.inc)> 9 or (x * -Xinc*self.inc)<0 or (y * -Yinc*self.inc)>9 or(y * -Yinc*self.inc)<0:
						#print("directional ovf")
						self.reset(True)
					if self.ennemy.ShowTray [x * -Xinc*self.inc][y * -Yinc*self.inc] != "":
						#print("directional end")
						self.reset()

					elif self.ennemy.tray [x * -Xinc*self.inc][y * -Yinc*self.inc] != "":
						self.ennemy.ShowTray [x * -Xinc*self.inc][y * -Yinc*self.inc] = "Y"
						#print("touché")
						self.hit = self.hit+1
						self.inc = self.inc +1
					else:
						#print("reset")
						self.reset()
				else:
					#print("rst flag detected")
					self.rstflag = True
			else:
				#print("forwards")
				if self.rstflag :

					if self.ennemy.tray [x * Xinc+2*self.inc][y * Yinc+2*self.inc] != "":
						self.ennemy.ShowTray [x * Xinc+2*self.inc][y * Yinc+2*self.inc] = "Y"
						self.inc = self.inc + 1
						self.hit = self.hit + 1
					else:
						self.backwards = True
						#print("reset inc")
						self.inc = 0
				else :
					#print(self.rstflag)
					self.rstflag = True

		else :
			#print ("cherck surroundings")
			x = self.aim[0]
			y = self.aim[1]
			checked = False
			while not checked:
				Ori = bool(random.getrandbits(1))
				Pola = bool(random.getrandbits(1))
				if Ori:
					if Pola:y = y+1
					else:y =y-1
				else:
					if Pola:x=x+1
					else:x=x-1
				if x> 9 or x<0 or y>9 or y<0:
					self.checked = self.checked+1
					self.reload()
				else:
					while self.ennemy.ShowTray [x][y] != "":
						#print("already checked")
						self.checked = self.checked+1
						self.reload()
						if self.checked >=3:
							break
							self.reset(True)

				if self.checked >=3:
					checked = True
					self.newshot = True
					self.checked = 0
				elif self.ennemy.tray [x][y] != "":
					self.ennemy.ShowTray [x][y] = "Y"
					checked = True
					self.newshot = False
					self.ori = Ori
					self.pola = Pola
					self.directional = True
					self.aimdir = (x,y)
					self.checked = 0
				else : self.checked = self.checked+1
			checked = False


		global COUNTER
		global TOUR
		self.ennemy.ShowTray [x][y] = "Y"
		#print(self.ennemy.ShowTray)
		TOUR = True
		COUNTER = COUNTER +1
		#print("TOUR no",COUNTER)

IA = IA()
Player = Player()

def DoIntent(BOUTON):
		#print("nice !! ! !! " + str(BOUTON.ID))
	if BOUTON.intent == 1:
		unloadts()
		Showpl()

		GLOBAL.S = True
	elif BOUTON.intent == 2:
		pass
	elif BOUTON.intent == 5:
		global TOUR
		TOUR = False
		Player.ennemy.CheckTray("Ia :  ")
		reveal(BOUTON.ID[0],BOUTON.ID[1])
		RefreshPl(True)
		IA.TURN()
		Player.tray.CheckTray("PLayer : ")
		if GLOBAL.DEBUGTRAY:
			Player.showWhereIAaimed()
	elif BOUTON.intent == 9:
		unloadts()
		Showts()
	elif BOUTON.intent == 10:
		unloadts()
		ShowOPT()
	elif BOUTON.intent == 11:
		GLOBAL.DEBUGTRAY = True
		unloadts()
		Showts()
	else :
		print ("error doing intent  : unknown intent :  id = " + str(BOUTON.intent))


def showFPS(): # afficher le taux de raffraichissement de l'écran
	fps = BaseFont.render(str(int(clock.get_fps())), True, pygame.Color("white"))
	pygame.draw.rect(gameDisplay,Placeholder,(90,90,90,90))
	gameDisplay.blit(fps,(90,90))#


def ArrayDisplay(Which):
	Max_X = len(Which) #taille X du tableau -> [¤,¤,¤,...,¤] -> ¤ est ["","","",...,""]
	Max_Y = len(Which[0]) # taille Y du tableau  -> taille de ¤
	dimss = BaseFont.render("width = " + str(Max_X) + " height = " + str(Max_Y),1,[0,0,0])# créer une image a partir des dimensions du tableau dans la police BaseFont
	gameDisplay.blit(dimss,(500,180))# affichage des dimensions
	for x in range(0,Max_X):#pour tous les items (scan horizontal)
		for y in range(0,Max_Y):#pour tous les items (scan vertical)
			display = BaseFont.render(str(Which[x][y]),1,[0,0,0])# creer une image de la viariable dans la police BaseFont
			gameDisplay.blit(display,(20*x+500,20*y+200))# dessin de la variable  sur gameDisplay


# enmplacements des panneaux (Side Pannel -> Span)(Top Pannel ->TNan)
#____________________________________________________
UI_SPan_h= 220
UI_SPan_w = 215

UI_TPan_h= 80
UI_TPan_w = 570

GLOBAL.Message = "Placez votre Flotte !"
#____________________________________________________

def basicInterface():
	pygame.draw.rect(gameDisplay,Placeholder,(0,(ScreenH/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h)) #endroit, couleur, taille
	pygame.draw.rect(gameDisplay,Placeholder,(ScreenW-UI_SPan_w,(ScreenH/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h))#endroit, couleur, taille
	pygame.draw.rect(gameDisplay,Placeholder,(ScreenW/2 - UI_TPan_w/2,0,UI_TPan_w,UI_TPan_h)) #endroit, couleur, taille



def PrintScore():

	MsgBox = STATEfont.render(GLOBAL.Message,1,[0,0,0])

	gameDisplay.blit(TITLEfont.render("Ordi",1,[0,0,0]),(ScreenW-UI_SPan_w + 65,(ScreenH/2)-(UI_SPan_h/2) + 5))#
	gameDisplay.blit(TITLEfont.render("Joueur",1,[0,0,0]),(50,(ScreenH/2)-(UI_SPan_h/2) + 5))
	gameDisplay.blit(MsgBox,(ScreenW/2  - MsgBox.get_rect().size[0]/2,15))


	gameDisplay.blit(GLOBAL.FONT1.render("Caravelles : " + str(player.Cplaced ) + "/" + str( player.nbCar),1,[0,0,0]),(10,(ScreenH/2)-(UI_SPan_h/2) + 70))
	gameDisplay.blit(GLOBAL.FONT2.render("Fregates : " + str(player.Fplaced) + "/" + str( player.nbFreg),1,[0,0,0]),(10,(ScreenH/2)-(UI_SPan_h/2) + 120))
	gameDisplay.blit(GLOBAL.FONT3.render("Vaisseau : " + str(player.Vplaced) + "/" + str( player.nbVais),1,[0,0,0]),(10,(ScreenH/2)-(UI_SPan_h/2) + 170))

	gameDisplay.blit(STATfont.render("Caravelles : " + str(computer.Cplaced ) + "/" + str( computer.nbCar),1,[0,0,0]),(ScreenW-UI_SPan_w + 10,(ScreenH/2)-(UI_SPan_h/2) + 70))
	gameDisplay.blit(STATfont.render("Fregates : " + str(computer.Fplaced) + "/" + str( computer.nbFreg),1,[0,0,0]),(ScreenW-UI_SPan_w + 10,(ScreenH/2)-(UI_SPan_h/2) + 120))
	gameDisplay.blit(STATfont.render("Vaisseau : " + str(computer.Vplaced) + "/" + str( computer.nbVais),1,[0,0,0]),(ScreenW-UI_SPan_w + 10,(ScreenH/2)-(UI_SPan_h/2) + 170))



def TitleScreen():
	gameDisplay.blit(pygame.transform.scale(LOGO,(485*2,176*2)),(ScreenW/2 - 485,30))

	Start = Bouton()
	Start.imageset = "Assets/UI/BigButton"
	Start.Scale = 8
	Start.posY = 500
	Start.istext = True
	Start.text = "Start"
	Start.intent = 1
	Start.initimages()
	Start.center("x")

	Options = Bouton()
	Options.imageset = "Assets/UI/BigButton"
	Options.Scale = 8
	Options.posY = 750
	Options.istext = True
	Options.text = "Options"
	Options.intent = 10
	Options.initimages()
	Options.center("x")
	global buttons
	buttons.append (Options)
	Options.show()
	buttons.append (Start)
	Start.show()

def vanish():
	for i in range (0,len(buttons)):
		del buttons[0]

def unloadts():
	for i in range (0,len(buttons)):
		del buttons[0]
	#print (buttons)

def ShowBackGr():
	nombre = ScreenW // fit + 1

	img = pygame.image.load("Assets/Mer.png")
	issou  = pygame.transform.scale(img, (nombre,nombre))
	yrange = ScreenH // nombre + 1

	for x in range(0,fit):
		for y in range(0,yrange):
			gameDisplay.blit(issou,(x * nombre,y*nombre))



clock = pygame.time.Clock()



def Showts():
	ShowBackGr ()
	TitleScreen()

def ShowOPT():
	ShowBackGr ()
	Debug = Bouton()
	Debug.imageset = "Assets/UI/BigButton"
	Debug.Scale = 8
	Debug.posY = 200
	Debug.istext = True
	Debug.text = "Enable Debug"
	Debug.intent = 11
	Debug.initimages()
	Debug.center("x")

	exit = Bouton()
	exit.imageset = "Assets/UI/BigButton"
	exit.Scale = 8
	exit.posY = 400
	exit.istext = True
	exit.text = "Done"
	exit.intent = 9
	exit.initimages()
	exit.center("x")
	global buttons

	buttons.append (Debug)
	Debug.show()
	buttons.append (exit)
	exit.show()


def Showpl():
 # Creation d'un plateau
	player.CreateTray(10,10)
	computer.CreateTray(10,10)
	player.ennemy = computer
	computer.ShowTray = [["NN"]*10 for _ in range(10)]
	computer.ennemy = player
	#player.nbCar = 3 # reféfénition du paramètre "nombre de Barques"
	player.owner = Player
	xdim = player.dim[0]
	ydim = player.dim[1]

	player.Gposx = 300
	player.Gposy =ScreenH/2 - (ydim*Lcase)/2
	#player.FillTray() # remplissage du tableau player



	xdim = computer.dim[0]
	ydim = computer.dim[1]

	computer.Gposx = ScreenW - (xdim*Lcase) - 300
	computer.Gposy =ScreenH/2  - (ydim*Lcase)/2
	computer.FillTray()
	#print (computer.tray)
	ShowBackGr()
	player.DisTray(gameDisplay,True)
	player.ennemy = computer

	computer.ennemy = player
	computer.DisTray(gameDisplay,False)

	basicInterface()
	PrintScore()
	__Mode = True

def reveal(x,y):
	if computer.tray[x][y] != "":
		computer.ShowTray[x][y] = "XX"
	else:
		computer.ShowTray[x][y] = ""
	player.vanish()
	computer.DisTray(gameDisplay,False)

def showtray():
	player.vanish()
	computer.vanish()
	player.DisTray(gameDisplay,True)
	computer.DisTray(gameDisplay,False)

def RefreshPl(Redraw = False):
	#print("refresh")

	ShowBackGr()
	basicInterface()
	PrintScore()
	if Redraw:
		computer.vanish()
		player.DisTray(gameDisplay,True)
	else:
		player.showTray(gameDisplay)
	computer.showTray(gameDisplay)


def editor(key):
	if GLOBAL.S :
		RefreshPl()
		player.surf = gameDisplay
		player.UpdateTray(key)
		#player.deltray(gameDisplay)
		computer.vanish()
		player.DisTray(gameDisplay,True,False)


RefreshPl()


def GAME():

	Player.TURN()
	pass

Showts()

def quit(): #quitter le prgm
	exit() #quiter le programe
	pygame.quit() # "désinitialise les modules pygame importés"

def ButtonScan(buttonArray,isup = True):
	for element in buttonArray :
		if element.burface.collidepoint(pygame.mouse.get_pos()):
			#print("element : " + str(element) + "	buttons =  " + str(buttons))
			element.hover()
			element.active = True
			if isup:
				if event.type == MOUSEBUTTONUP:
					DoIntent(element)
			else:
				if event.type == MOUSEBUTTONDOWN:
					DoIntent(element)

		elif element.active :
			element.unhover()

while not StopGame:
	for event in pygame.event.get(): #Gestionaire d'evènements (souris clavier boutons ... )
		if event.type == pygame.QUIT: #Si la croix rouge (en haut a droite est cliquée) -> plein écran (inutile) -> preview en bare des taches (ok)
			quit() #quitter le prgm

		if event.type == pygame.KEYDOWN: #Si une touche est enfoncée
			if event.key == pygame.K_ESCAPE: #si la touche échap est enfoncée
				quit() #quitter le prgm


		if GLOBAL.S :
			if event.type == pygame.KEYDOWN:
				editor(event.key)

		elif GLOBAL.PlayMode :
			if TOUR:
				ButtonScan(computer.ButTray,False)

		ButtonScan(buttons)


	pygame.display.update()  # Rafrichir l'écran # identique à pygame.display.flip()
	#showFPS()
	clock.tick(100) # définir le rafraichissement de l'écran | -> clock.tick(200) -> 200 FPS m
