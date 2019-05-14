import pygame
import random
import sys
from pygame.locals import *


global isSelection
isSelection = False

global TOUR
TOUR = True

COUNTER = 0
def vanish():
	pass
def RefreshPl(Redraw = False):
	pass
placeMode = False
traysize = 10
T = 16
Placeholder = [255,0,0] # couleur de remplacement (tableau) -> [Rouge , Vert , Bleu] 0-255
global buttons
buttons = []
global numberBoatsOnTheTray
numberBoatsOnTheTray = 0


fit = 25 # nb de cases a rentrer dans l'espace horizontal de l'écran
StopGame = False # variable verifiant l'etat du programe



TOP  =  pygame.image.load("Assets/TOP.png")
SIDE  =  pygame.image.load("Assets/SIDE.png")
CROSS  =  pygame.image.load("Assets/cross.png")
TRAY  =  pygame.image.load("Assets/tray.png")
LOGO =  pygame.image.load("Assets/LOGO.png")

pygame.font.init()#initialisation de l'objet pygame.font
pygame.init() #initialisation de l'objet pygame

ecran = pygame.display.Info() # création d'un objet (pygame.display.Info)

if ecran.current_w < 1900: mult = 1.5
else: mult = 2
Lcase = int(32*mult)
offset = Lcase


BaseFont = pygame.font.SysFont("Comic Sans MS",16) #definition d'un objet font (police d'écriture) -> BaseFont
SmallDebugFont = pygame.font.SysFont("Arial Bold",25)
STATEfont = pygame.font.Font("Assets/Pieces of Eight.ttf",55)
STATfont = pygame.font.Font("Assets/Pieces of Eight.ttf",28)
TITLEfont = pygame.font.Font("Assets/Pieces of Eight.ttf",40)
SelectedFont = pygame.font.Font("Assets/Pieces of Eight.ttf",30)
SelectedFont.set_underline(True)





class GLOBAL:
	def __init__(self):
		self.S = False
		self.FONT1 = SelectedFont
		self.FONT2 =STATfont
		self.FONT3 =STATfont
		self.PlayMode = False
		self.Message = "Placez votre Flotte !"
		self.DEBUGTRAY = False
		self.TOTALBOATSIA = 0
		self.TOTALBOATSPLAYER = 0

GLOBAL = GLOBAL()

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
		#print ("placing a  " + str(what) + "  position : x = " + str(x) + "  ||  y = "  + str(y) )
		#print ("XP = " + str(XP) + "   XM = " + str(XM) + "   YP = " + str(YP) + "   YM = " + str(YM))
		pass

	return(Xinc,Yinc,ok)

def ScribeBoat(id,size,posX,posY,Xinc,Yinc,tray,postray,angletray,TotalBoats):

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
		postray[TotalBoats][i] = ((posY + Yinc*i),(posX+ Xinc*i))
	#print ("added  " +  str(postray[TotalBoats]))

	return TotalBoats + 1
if ecran.current_w > 1920 :
	gameDisplay = pygame.display.set_mode((1920,1080))# definition de la taille de la fenetre ( -> taille de l'écran)
	ScreenW  = 1920
	ScreenH = 1080

else:
	gameDisplay = pygame.display.set_mode((ecran.current_w,ecran.current_h),FULLSCREEN)
	ScreenW  = ecran.current_w
	ScreenH = ecran.current_h



class display:
	def __init__(self):
		self.Display = pygame.display.set_mode()
		self.mult = 2

display = display()


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
		# |>	GLOBAL.FONT ??????????????

	def initimages(self):



		self.imagesrc = pygame.image.load(self.imageset + self.base)
		self.hoverimagesrc = pygame.image.load(self.imageset + self.basehover)

		if self.autoScale:
			self.Scale = int(self.w / self.imagesrc.get_rect().size[0])

		self.image = pygame.transform.rotate(self.imagesrc,self.angle)
		self.image = pygame.transform.scale(self.image,(int(self.Scale * self.imagesrc.get_rect().size[0]),int(self.Scale * self.imagesrc.get_rect().size[1])))

		self.hoverimage = pygame.transform.rotate(self.hoverimagesrc,self.angle)
		self.hoverimage = pygame.transform.scale(self.hoverimage,(int(self.Scale * self.hoverimagesrc.get_rect().size[0]),int(self.Scale * self.hoverimagesrc.get_rect().size[1])))

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
			self.posX =   ScreenW /2 - self.image.get_rect().size[0] / 2
		elif type == "y":
			self.posY =  ScreenH /2 -  self.image.get_rect().size[1] / 2
		else :
			print ("error centering button  : unknown argument : " + type)


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
		self.dim = (1 , 1) # creation d'une variable nb]double ->dimention du plateau
		self.tray = [[""]] #initialisation du paramètre Plateau (tableaux de X par Y contentant les batteaux)
		self.editTray = [[""]*10 for _ in range(10)]
		self.angle = [[0]*10 for _ in range(10)]
		self.ShowTray = [[""]*10 for _ in range(10)]
		self.checked = [[False]*10 for _ in range(10)]
		self.postray = []
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
		self.TotalBoats = 0
		self.player = False
	def CreateTray(self,x,y):
		self.dim = (x,y)
		#print ("Created Tray")

		self.postray = [[(255,255)]*4 for _ in range(self.nbFreg + self.nbCar + self.nbVais)]
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

					self.TotalBoats = ScribeBoat(bato[size - 2],size,posX,posY,Xinc,Yinc,self.tray,self.postray,self.angle,self.TotalBoats)
					numberBoatsOnTheTray = numberBoatsOnTheTray +1

				else :
					#print("can'nt place boat")
					pass


	def CheckTray (self,test = ""):
		nb = 0
		#print (self.postray)
		for Boat in self.postray:
			delboat = 0
			act = 0
			for i in range(0,4):
				if Boat[i][0] > 100:
					delboat = delboat +1
					if Boat[i][0] < 220:
						act = act+1
					#print ("delboat")

				elif self.ShowTray[Boat[i][0]][Boat[i][1]] != "":
					if self.ShowTray[Boat[i][0]][Boat[i][1]] != "NN" :
						self.postray[nb][i] = (200,200)


			if delboat == 4:
				#print(delboat , Boat)
				self.postray.remove(Boat)
				#print("delboat")
				if act == 2: self.Cplaced = self.Cplaced -1
				elif act == 3 : self.Fplaced = self.Fplaced -1
				elif act == 4 :self.Vplaced = self.Vplaced -1
				else: print ("delboat = "+str(act))
			nb = nb +1



			#print(Boat[1][1])
	def FillTray(self):

		self.placeBoats(self.nbCar,2)
		self.Cplaced = self.nbCar
		self.placeBoats(self.nbFreg,3)
		self.Fplaced = self.nbFreg
		self.placeBoats(self.nbVais,4)
		self.Vplaced = self.nbVais
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
		ni = Lcase *display.mult * xdim + (offset-Lcase)  * (xdim-1)
	#	#pygame.draw.rect(surf,[0,0,0],(self.Gposx,self.Gposy,ni,ni))
		######################################################################################################
		if grid:
			n = int(((32 * 10) + 2 )* display.mult)
			self.surf.blit(pygame.transform.scale(TRAY,(n,n)),(self.Gposx-2,self.Gposy-2))
		for y in range(0,ydim):
			for x in range(0,xdim):
				if not tray [x][y] == "":
					but = Bouton()
					but.posX = self.Gposx + offset*x
					but.posY = self.Gposy + offset*y
					but.h = but.w = Lcase
					but.ID = (x,y)
					but.autoScale = False
					but.Scale = display.mult
					but.intent = 5
					but.arg = self.ennemy
					but.imageset = "Assets/Boats/"
					if Visible:
						but.angle = self.angle[x][y]
						if self.ShowTray[x][y] != "" :
							but.imageset = "Assets/DeadBoats/"

					but.base = tray [x][y][0] + "/" + tray [x][y][1] + ".png"
					but.basehover = tray[x][y][0] + "/" + tray [x][y][1] + ".png"
					#buttons.append (but)
					self.ButTray.append(but)
					but.show()

					if GLOBAL.DEBUGTRAY :
						traycontent = SmallDebugFont.render(self.tray [x][y], True, pygame.Color("white"))
						debugplayer = SmallDebugFont.render(str(x) + " , " + str(y), True, pygame.Color("white"))
						gameDisplay.blit(traycontent,(but.posX +5,but.posY +5))#
						gameDisplay.blit(debugplayer,(but.posX +5,but.posY +25))#		self. debugShow()


	def showTray (self,surf):
		n = int(((32 * 10) + 2 )* display.mult)
		self.surf.blit(pygame.transform.scale(TRAY,(n,n)),(self.Gposx-2,self.Gposy-2))
		for i in self.ButTray:
			i.show()

	def PlaceModeDisplay (self,what,Yinc ,Xinc ):
		#print("draw")
		#print(self.editTray)
		if what == "C": self.length = 2
		elif what == "F": self.length = 3
		elif what == "V": self.length = 4
		xdim = self.dim[0]
		ydim = self.dim[1]

		self.surf.blit(pygame.transform.scale(CROSS,(Lcase,Lcase)),(self.Gposx + offset*self.placeposX,self.Gposy + offset*self.placeposY))
		if isSelection:
			for i in range(0,self.length):
				self.surf.blit(pygame.transform.scale(CROSS,(Lcase,Lcase)),(self.Gposx + offset*self.placeposX + Xinc*i*Lcase,self.Gposy + offset*self.placeposY+Yinc*i*Lcase))
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

		self.surf.blit(pygame.transform.scale(CROSS,(Lcase,Lcase)),(self.Gposx + offset*self.placeposX,self.Gposy + offset*self.placeposY))

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

				self.TotalBoats = ScribeBoat(self.toPlace ,self.length,self.placeposY,self.placeposX,Y,X,self.tray,self.postray,self.angle,self.TotalBoats)
				#print ("angle :" + str(self.angle))
				if self.toPlace == "C":self.Cplaced = self.Cplaced +1
				elif self.toPlace == "F":self.Fplaced = self.Fplaced +1
				elif self.toPlace == "V":self.Vplaced = self.Vplaced +1

				#print("Bateaux : " + str(self.Cplaced)+ " / " + str(self.nbCar) +"   Fplaced : " + str(self.Fplaced)+ " / " + str(self.nbFreg) + "   Vplaced :" +  str(self.Vplaced) + " / " + str(self.nbCar)    )
			else:
				self.placeMode = True
			isSelection = False


		if self.placeMode:
			self.PlaceModeDisplay(self.toPlace,Y,X)
			self.YincM = Y
			self.XincM = X
			self.ok = True


		else:
			if self.Cplaced  < self.nbCar:
				self.toPlace = "C"
				GLOBAL.FONT1 =SelectedFont
				GLOBAL.FONT2 =STATfont
				GLOBAL.FONT3 =STATfont
			elif self.Fplaced < self.nbFreg:
				self.toPlace = "F"
				GLOBAL.FONT1 = STATfont
				GLOBAL.FONT2 =SelectedFont
				GLOBAL.FONT3 =STATfont
			elif self.Vplaced < self.nbVais:
				self.toPlace = "V"
				GLOBAL.FONT1 = STATfont
				GLOBAL.FONT2 =STATfont
				GLOBAL.FONT3 =SelectedFont
			else:
				GLOBAL.FONT1 = STATfont
				GLOBAL.FONT2 =STATfont
				GLOBAL.FONT3 =STATfont

				GLOBAL.S = False
				GLOBAL.Message = "Que la bataille commence !"
				GLOBAL.PlayMode = True
				self.HideTray()
			#print(MoveX,MoveY )
			self.EDplace(self.toPlace,MoveX,MoveY)
