# Imports de librairies
#____________________________________________________

import pygame
import sys
from pygame.locals import *
import random
#____________________________________________________

global Edit_Mode
Edit_Mode = False
global PlayMode
PlayMode = False
DEBUGTRAY = False
global isSelection
isSelection = False

global TOUR
TOUR = True
#
#
# barque = 1 case
#
#
COUNTER = 0
def vanish():
	pass
def RefreshPl():
	pass
placeMode = False
traysize = 10
T = 16
Placeholder = [255,0,0] # couleur de remplacement (tableau) -> [Rouge , Vert , Bleu] 0-255
global buttons
buttons = []
global numberBoatsOnTheTray
numberBoatsOnTheTray = 0

pygame.font.init()#initialisation de l'objet pygame.font
pygame.init() #initialisation de l'objet pygame
BaseFont = pygame.font.SysFont("Comic Sans MS",16) #definition d'un objet font (police d'écriture) -> BaseFont
SmallDebugFont = pygame.font.SysFont("Arial",12)




infoObject = pygame.display.Info() # création d'un objet (pygame.display.Info)
fit = 25 # nb de cases a rentrer dans l'espace horizontal de l'écran
StopGame = False # variable verifiant l'etat du programe

CROSS  =  pygame.image.load("Assets/cross.png")
TRAY  =  pygame.image.load("Assets/tray.png")
LOGO =  pygame.image.load("Assets/LOGO.png")


def check(array,what,radius,y,x,YM,YP,XM,XP):

		for i in range(0,radius+1):
			if YM == True :
				if not ((y-i > 0 ) and array[y-i][x] == ""):YM = False
			if  YP == True:
				if not((y+i < traysize) and array[y+i][x]== "" ):YP = False
			if XP == True:
				if not((x+i < traysize) and array[y][x+i]== "" ) :XP = False
			if  XM == True :
				if not((x-i > 0) and array[y][x-i] == "") :XM = False

		return(YM,YP,XM,XP,what,y,x)

def RandomOrientation(flags):
	YM=flags[0]
	YP=flags[1]
	XM=flags[2]
	XP=flags[3]
	what = flags[4]
	y = flags[5]
	x = flags[6]

	Xinc = 0
	Yinc = 0
	ok = False
	orientation = bool(random.getrandbits(1)) #X or Y
	polarity = bool(random.getrandbits(1)) # + or -


	if YM:
		if YM and YP :
			if polarity:
				Yinc = 1
			else:
				Yinc = -1
	elif YP:
		Yinc = 1

	if XM:
		if XM and XP :
			if polarity:
				Xinc = 1
			else:
				Xinc = -1
	elif XP:
		Xinc = 1
	else :
		pass

	if Xinc != 0 and Yinc !=0 :
		if orientation:
			Yinc = 0
			ok = True
		elif not orientation:
			Xinc = 0
			ok = True
	elif Xinc == 0 and Yinc ==0:
		ok = False
	if ok:
		print ("placing a  " + str(what) + "  position : x = " + str(x) + "  ||  y = "  + str(y) )
		print ("XP = " + str(XP) + "   XM = " + str(XM) + "   YP = " + str(YP) + "   YM = " + str(YM))

	return(Xinc,Yinc,ok)

def ScribeBoat(id,size,posX,posY,Xinc,Yinc,tray,postray,angletray):
	angle = 0
	if Xinc >0:
		angle = 0
	elif Xinc <0:
		angle = 180
	elif Yinc <0:
		angle = 270
	elif Yinc >0:
		angle = 90
	for i in range(0,size):
		angletray[posY + Yinc*i][posX+ Xinc*i] = angle
		tray[posY + Yinc*i][posX+ Xinc*i] = id+str(i)
		postray.append(str(posX) + "," + str(posY)+',' + id +str(i))

def reveal(x,y):
	pass




class Bouton:
	def __init__(self):
		self.arg = ""
		self.posX = 0
		self.posY = 0
		self.w = 30
		self.h = 30
		self.color = [0,255,128]
		self.ucolor = [200,255,10]
		self.Scale = 1
		self.autoScale = False
		self.angle = 0
		self.active = False
		self.ID = "#"
		self.imageset = "/"
		self.intent = 0
		self.base = "/Base.png"
		self.basehover = "/BaseHover.png"
		self.istext = False;
		self.image = pygame.image.load("Assets/NOTEXT.png")
		self.imagesrc = pygame.image.load("Assets/NOTEXT.png")
		self.arg = ""
		# -> TEXT ??????????????????
		# |>	FONT ??????????????

	def initimages(self):

		self.imagesrc = pygame.image.load(self.imageset + self.base)
		self.hoverimagesrc = pygame.image.load(self.imageset + self.basehover)

		if self.autoScale:
			self.Scale = int(self.w / self.imagesrc.get_rect().size[0])

		self.image = pygame.transform.rotate(self.imagesrc,self.angle)
		self.image = pygame.transform.scale(self.image,(self.Scale * self.imagesrc.get_rect().size[0],self.Scale * self.imagesrc.get_rect().size[1]))

		self.hoverimage = pygame.transform.rotate(self.hoverimagesrc,self.angle)
		self.hoverimage = pygame.transform.scale(self.hoverimage,(self.Scale * self.hoverimagesrc.get_rect().size[0],self.Scale * self.hoverimagesrc.get_rect().size[1]))

		if self.istext :
			self.textimagesrc = pygame.image.load(self.imageset + "/" + self.text + ".png")
			self.textimage =pygame.transform.scale(self.textimagesrc,(self.Scale * self.textimagesrc.get_rect().size[0],self.Scale * self.textimagesrc.get_rect().size[1]))


	def show(self):

		########################

		if self.imageset == "/":
			self.burface = pygame.draw.rect(gameDisplay,self.color,(self.posX,self.posY,self.w,self.h))
		else :
			self.initimages()
			self.burface = gameDisplay.blit(self.image,(self.posX,self.posY))
			if self.istext :
				self.burface = gameDisplay.blit(self.textimage,(self.posX,self.posY))

	def hover(self):
		if self.imageset == "/":
			self.burface = pygame.draw.rect(gameDisplay,self.ucolor,(self.posX,self.posY,self.w,self.h))
		else :
			self.burface = gameDisplay.blit(self.hoverimage,(self.posX,self.posY))
			if self.istext :
				self.burface = gameDisplay.blit(self.textimage,(self.posX,self.posY))

	def unhover(self):
		if self.imageset == "/":
			self.burface = pygame.draw.rect(gameDisplay,self.color,(self.posX,self.posY,self.w,self.h))

		else :
			self.burface = gameDisplay.blit(self.image,(self.posX,self.posY))
			if self.istext :
				self.burface = gameDisplay.blit(self.textimage,(self.posX,self.posY))

	def center(self,type):
		if type == "x":
			self.posX =   infoObject.current_w /2 - self.image.get_rect().size[0] / 2
		elif type == "y":
			self.posY =  infoObject.current_h /2 -  self.image.get_rect().size[1] / 2
		else :
			print ("error centering button  : unknown argument : " + type)

	def DoIntent(self):
		#print("nice !! ! !! " + str(self.ID))
		global DEBUGTRAY
		if self.intent == 1:
			unloadts()
			Showpl()
			global Edit_Mode
			Edit_Mode = True
		elif self.intent == 2:
			pass
		elif self.intent == 5:
			global TOUR
			TOUR = False
			reveal(self.ID[0],self.ID[1])
			RefreshPl()
			IA.TURN()
			if DEBUGTRAY:
				Player.showWhereIAaimed()
		elif self.intent == 9:
			unloadts()
			Showts()
		elif self.intent == 10:
			unloadts()
			ShowOPT()
		elif self.intent == 11:
			DEBUGTRAY = True
			unloadts()
			Showts()
		else :
			print ("error doing intent  : unknown intent :  id = " + str(self.intent))

class proto:
	def __init__(self):
		self.ButTray = []
		self.ShowTray = [["NN"]*10 for _ in range(10)]
class TrayClass:
	def __init__(self):
		# paramètres de l'objet

		self.nbFreg = 2
		self.nbCar = 3
		self.nbVais = 1
		self.Fplaced = 0
		self.Cplaced = 0
		self.Vplaced = 0
		self.dim = (1 , 1) # creation d'une variable double ->dimention du plateau
		self.tray = [[""]] #initialisation du paramètre Plateau (tableaux de X par Y contentant les batteaux)
		self.editTray = [[""]*10 for _ in range(10)]
		self.angle = [[0]*10 for _ in range(10)]
		self.ShowTray = [[""]*10 for _ in range(10)]
		self.checked = [[False]*10 for _ in range(10)]
		self.Gposx = 30
		self.Gposy = 30
		self.Lcase = 0
		self.toPlace =""
		self.placeposX =0
		self.placeposY =0
		self.placeMode = False
		self.surf = gameDisplay
		self.Xinc = 0
		self.Yinc = 0
		self.length = 0
		self.ennemy = proto()
		self.ButTray = []
		self.ok = True
		self.XincM = 0
		self.YincM = 0
		self.owner = ""

	def CreateTray(self,x,y):
		self.dim = (x,y)
		#print ("Created Tray")

		self.postray = []
		self.angle = [[0]*x for _ in range(y)]
		self.tray = [[""]*x for _ in range(y)] # parce que python c'est rigolo
	def placeBoats(self,nbBoats,size):
		xdim = self.dim[0]
		ydim = self.dim[1]
		bato = ["C","F","V"]

		numberBoatsOnTheTray = 0
		while (numberBoatsOnTheTray < nbBoats):
				#premierement l'ordi choisit une pos au hasard sur le plateau
			posX = random.randint(0,xdim-1)
			posY = random.randint(0,ydim-1)
			if self.tray[posY][posX] == "": #est-ce que on essaye de placer un bateau sur un bateau
				#player si les differentes orientations possibles sont autorisées
				incs = RandomOrientation(check(self.tray,bato[size - 2],size,posY,posX,True,True,True,True))
				Xinc = incs[0]
				Yinc = incs[1]
				ok = incs[2]

				if ok :
					ScribeBoat(bato[size - 2],size,posX,posY,Xinc,Yinc,self.tray,self.postray,self.angle)
					numberBoatsOnTheTray = numberBoatsOnTheTray +1

				else :
					#print("can'nt place boat")
					pass



	def FillTray(self):
		self.placeBoats(self.nbFreg,2)
		self.placeBoats(self.nbCar,3)
		self.placeBoats(self.nbVais,4)
		#print(self.tray)
	def vanish(self):
		for i in range (0,len(self.ennemy.ButTray)):
			del self.ennemy.ButTray[0]
		#print (self.ennemy.ButTray)
	def HideTray(self) :
		RefreshPl()

	def DisTray(self,surf,Visible,grid = True):
		if Visible :tray = self.tray
		else :tray = self.ShowTray

		xdim = self.dim[0]
		ydim = self.dim[1]
		ni = Lcase * xdim + (offset-Lcase)  * (xdim-1)
	#	#pygame.draw.rect(surf,[0,0,0],(self.Gposx,self.Gposy,ni,ni))
		######################################################################################################
		if grid:
			self.surf.blit(pygame.transform.scale(TRAY,(644,644)),(self.Gposx-2,self.Gposy-2))
		for y in range(0,ydim):
			for x in range(0,xdim):
				if not tray [x][y] == "":
					but = Bouton()
					but.posX = self.Gposx + offset*x
					but.posY = self.Gposy + offset*y
					but.h = but.w = Lcase
					but.ID = (x,y)
					but.autoScale = True
					but.intent = 5
					but.arg = self.ennemy
					if Visible:
						but.angle = self.angle[x][y]
					but.imageset = "Assets/Boats/"
					but.base = tray [x][y][0] + "/" + tray [x][y][1] + ".png"
					but.basehover = tray[x][y][0] + "/" + tray [x][y][1] + ".png"
					#buttons.append (but)
					self.ButTray.append(but)
					but.show()

					if DEBUGTRAY :
						traycontent = SmallDebugFont.render(tray [x][y], True, pygame.Color("white"))
						debugplayer = SmallDebugFont.render(str(x) + " , " + str(y), True, pygame.Color("white"))
						gameDisplay.blit(traycontent,(but.posX +5,but.posY +5))#
						gameDisplay.blit(debugplayer,(but.posX +5,but.posY +25))#

	def showTray (self,surf):
		self.surf.blit(pygame.transform.scale(TRAY,(644,644)),(self.Gposx-2,self.Gposy-2))
		for i in self.ButTray:
			i.show()


	def PlaceModeDisplay (self,what,Yinc ,Xinc ):
		print("draw")
		print(self.editTray)
		if what == "C": self.length = 2
		elif what == "F": self.length = 3
		elif what == "V": self.length = 4
		xdim = self.dim[0]
		ydim = self.dim[1]

		self.surf.blit(pygame.transform.scale(CROSS,(64,64)),(self.Gposx + offset*self.placeposX,self.Gposy + offset*self.placeposY))
		if isSelection:
			for i in range(0,self.length):
				self.surf.blit(pygame.transform.scale(CROSS,(64,64)),(self.Gposx + offset*self.placeposX + Xinc*i*Lcase,self.Gposy + offset*self.placeposY+Yinc*i*Lcase))
		self.ok = True
	def DisEdit (self,surf):

		#print("draw")
		#print(self.editTray)
		xdim = self.dim[0]
		ydim = self.dim[1]
		for y in range(0,ydim):
			for x in range(0,xdim):
				if self.editTray[y][x] != "" :
					pygame.draw.rect(surf,Placeholder,(self.Gposx + offset*x,self.Gposy + offset*y, Lcase,Lcase))

	def EDplace(self,place,MoveX,MoveY):
		self.placeposX = self.placeposX + MoveX
		self.placeposY = self.placeposY + MoveY
		if self.placeposY <= 0 : self.placeposY = 0
		if self.placeposX <= 0 : self.placeposX = 0
		if self.placeposY >= 10 : self.placeposY = 9
		if self.placeposX >= 10 : self.placeposX = 9

		if place == "C" :
			self.editTray[self.placeposY][self.placeposX] = "C"
		elif place == "F":
			self.editTray[self.placeposY][self.placeposX] = "F"
		elif place == "V":
			self.editTray[self.placeposY][self.placeposX] = "V"

		xdim = self.dim[0]
		ydim = self.dim[1]

		self.surf.blit(pygame.transform.scale(CROSS,(64,64)),(self.Gposx + offset*self.placeposX,self.Gposy + offset*self.placeposY))

	def UpdateTray(self,move):
		MoveX =0
		MoveY =0
		direction =0
		global isSelection

		if self.toPlace == "C":space = 2
		elif self.toPlace == "F":space = 3
		else :space = 4
		if move == pygame.K_LEFT :
			MoveX = -1
			self.Xinc = -1
			self.Yinc = 0
			isSelection = True
			if self.placeposX < space-1:self.ok = False
		if move == pygame.K_RIGHT:
			MoveX = 1
			self.Xinc = 1
			self.Yinc = 0
			isSelection = True
			if self.placeposX > 10- space:self.ok = False
		if move == pygame.K_UP:
			MoveY = -1
			self.Xinc = 0
			self.Yinc = -1
			isSelection = True
			if self.placeposY < space-1:self.ok = False
		if move == pygame.K_DOWN:
			MoveY = 1
			self.Xinc = 0
			self.Yinc = 1
			isSelection = True
			if self.placeposY> 10-space :self.ok = False

		if self.ok :
			X=self.Xinc
			Y=self.Yinc
		else:
			X=self.XincM
			Y=self.YincM
			isSelection = False
		if move == pygame.K_RETURN:

			if self.placeMode and  isSelection:

				self.placeMode = False

				ScribeBoat(self.toPlace ,self.length,self.placeposY,self.placeposX,Y,X,self.tray,self.postray,self.angle)
				#print ("angle :" + str(self.angle))
				if self.toPlace == "C":self.Cplaced = self.Cplaced +1
				elif self.toPlace == "F":self.Fplaced = self.Fplaced +1
				elif self.toPlace == "V":self.Vplaced = self.Vplaced +1

				print("Bateaux : " + str(self.Cplaced)+ " / " + str(self.nbCar) +"   Fplaced : " + str(self.Fplaced)+ " / " + str(self.nbFreg) + "   Vplaced :" +  str(self.Vplaced) + " / " + str(self.nbCar)    )
			else:
				self.placeMode = True
			isSelection = False


		if self.placeMode:
			self.PlaceModeDisplay(self.toPlace,Y,X)
			self.YincM = Y
			self.XincM = X
			self.ok = True


		else:
			global Edit_Mode
			global PlayMode
			if self.Cplaced  < self.nbCar:self.toPlace = "C"
			elif self.Fplaced < self.nbFreg:self.toPlace = "F"
			elif self.Vplaced < self.nbVais:self.toPlace = "V"
			else:
				Edit_Mode = False
				PlayMode = True
				self.HideTray()
			#print(MoveX,MoveY )
			self.EDplace(self.toPlace,MoveX,MoveY)


Lcase = 64
offset= Lcase



gameDisplay = pygame.display.set_mode((infoObject.current_w,infoObject.current_h),FULLSCREEN)# definition de la taille de la fenetre ( -> taille de l'écran)
# -> affichage en plein écran
pygame.display.set_caption('GAME')# définition du tytre de la fenetre -> plein écran (inutile) -> preview en bare des taches (ok)

gameDisplay.fill([255,0,255]) # remplissage de la couleur d'arrière-plan (magenta) pour verifier l'abscence de texture
# --------> (si il y a un bout magenta , c'est pas beau et ça se voit)

#pygame.draw.rect(gameDisplay,[20,30,12],(50,50,50,50)) #-> création d'un rectangle


player = TrayClass() # creation d'un objet Tray
computer= TrayClass()

class Player:
	def __init__(self):
		self.ennemy = computer
		self.tray =  player
	def showWhereIAaimed(self):
		xdim = self.tray.dim[0]
		ydim = self.tray.dim[1]
		ni = Lcase * xdim + (offset-Lcase)  * (xdim-1)

		for y in range(0,ydim):
			for x in range(0,xdim):
				traycontent = SmallDebugFont.render(self.tray.ShowTray [x][y], True, pygame.Color("Black"))
				gameDisplay.blit(traycontent,(self.tray.Gposx + offset*x +25,self.tray.Gposy + offset*y +25))#


class IA:
	def __init__(self):
		self.checked = [[False]*10 for _ in range(10)]
		self.ennemy = player
		self.aim = (0,0)
		self.newshot = True
		self.directionnal = False
		self.checked = 0
		self.pola = False
		self.ori = False
	def TURN(self):
		if self.newshot:
			x = random.randint(0,9)
			y = random.randint(0,9)

			if self.ennemy.tray [x][y] != "":
				self.aim = (x,y)
				self.newshot = False
		elif self.directional:
			pass
			self.directionnal = False
			self.newshot = True

		else :
			x = self.aim[0]
			y = self.aim[1]
			checked = False
			while not checked:
				Ori = bool(random.getrandbits(1))
				Pola = random.getrandbits(1)
				if Ori:
					if Pola:y = y+1
					else:y =y-1
				else:
					if Pola:x=x+1
					else:x=x-1

				if self.ennemy.ShowTray [x][y] != "Y":
					self.ennemy.ShowTray [x][y] = "Y"
					checked = True
					self.newshot = False
					self.ori = Ori
					self.pola = Pola
					self.directionnal = True
					self.checked = 0

				elif self.checked >=3:
					checked = True
					self.newshot = False
					self.checked = 0
				else : self.checked = self.checked+1


		global COUNTER
		global TOUR
		self.ennemy.ShowTray [x][y] = "Y"
		#print(self.ennemy.ShowTray)
		TOUR = True
		COUNTER = COUNTER +1
		#print("TOUR no",COUNTER)

IA = IA()
Player = Player()


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
UI_SPan_h= 350
UI_SPan_w = 200

UI_TPan_h= 70
UI_TPan_w = 350
#____________________________________________________

def basicInterface():
	pygame.draw.rect(gameDisplay,Placeholder,(0,(infoObject.current_h/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h)) #endroit, couleur, taille

	pygame.draw.rect(gameDisplay,Placeholder,(infoObject.current_w-UI_SPan_w,(infoObject.current_h/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h))#endroit, couleur, taille

	pygame.draw.rect(gameDisplay,Placeholder,(infoObject.current_w/2 - UI_TPan_w/2,0,UI_TPan_w,UI_TPan_h)) #endroit, couleur, taille

def PrintScore():

	pygame.draw.rect(gameDisplay,Placeholder,(0,(infoObject.current_h/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h)) #endroit, couleur, taille

	pygame.draw.rect(gameDisplay,Placeholder,(infoObject.current_w-UI_SPan_w,(infoObject.current_h/2)-(UI_SPan_h/2),UI_SPan_w,UI_SPan_h))#endroit, couleur, taille

	pygame.draw.rect(gameDisplay,Placeholder,(infoObject.current_w/2 - UI_TPan_w/2,0,UI_TPan_w,UI_TPan_h)) #endroit, couleur, taille

def TitleScreen():

	gameDisplay.blit(pygame.transform.scale(LOGO,(485*2,176*2)),(infoObject.current_w/2 - 485,30))

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
	print (buttons)

def ShowBackGr():
	nombre = infoObject.current_w // fit + 1

	img = pygame.image.load("Assets/Mer.png")
	issou  = pygame.transform.scale(img, (nombre,nombre))
	yrange = infoObject.current_h // nombre + 1

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
	player.Gposy =infoObject.current_h/2 - (ydim*offset)/2
	#player.FillTray() # remplissage du tableau player



	xdim = computer.dim[0]
	ydim = computer.dim[1]

	computer.Gposx = infoObject.current_w - (xdim*offset) - 300
	computer.Gposy =infoObject.current_h/2  - (ydim*offset)/2
	computer.FillTray()
	print (computer.tray)
	ShowBackGr()
	player.DisTray(gameDisplay,True)
	player.ennemy = computer

	computer.ennemy = player
	computer.DisTray(gameDisplay,False)

	basicInterface()
	Edit_Mode = True

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

def RefreshPl():
	#print("refresh")
	ShowBackGr()
	basicInterface()
	player.showTray(gameDisplay)
	computer.showTray(gameDisplay)


def editor(key):
	if Edit_Mode :
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
					element.DoIntent()
			else:
				if event.type == MOUSEBUTTONDOWN:
					element.DoIntent()
		elif element.active :
			element.unhover()

while not StopGame:
	for event in pygame.event.get(): #Gestionaire d'evènements (souris clavier boutons ... )
		if event.type == pygame.QUIT: #Si la croix rouge (en haut a droite est cliquée) -> plein écran (inutile) -> preview en bare des taches (ok)
			quit() #quitter le prgm

		if event.type == pygame.KEYDOWN: #Si une touche est enfoncée
			if event.key == pygame.K_ESCAPE: #si la touche échap est enfoncée
				quit() #quitter le prgm


		if Edit_Mode :
			if event.type == pygame.KEYDOWN:
				editor(event.key)

		elif PlayMode :
			if TOUR:
				ButtonScan(computer.ButTray,False)

		ButtonScan(buttons)


	pygame.display.update()  # Rafrichir l'écran # identique à pygame.display.flip()
	#showFPS()
	clock.tick(100) # définir le rafraichissement de l'écran | -> clock.tick(200) -> 200 FPS m
