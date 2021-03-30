def main():
	import pygame
	n=input('Ingrese "i" para leer instrucciones antes de jugar, cualquier otro ingreso para comenzar inmediatamente: ')
	if n=='i':
		inst = open('instrucciones.txt','r')
		for fil in inst:
			print(fil[:-1])
		inst.close()
	name=entername()
	cicle=True	
	while cicle:
		cicle=juego(name)
	pygame.quit()
def gethiscore():
	hiscores = open('PokeScore.txt','r')
	scores={}
	for fila in hiscores:	
		ind=fila.index('>')
		f=fila[:(ind-1)]
		s=int(fila[(ind+1):-1])
		scores[f]=s
	hs=0
	for x in scores:
		if scores[x]>hs:
			hs=scores[x]
			fhs=('HiScore: {0}->{1}'.format(x,scores[x]))
	hiscores.close()	
	return fhs	
#Esta funcion returna el puntaje maximo registrado en un archivo .txt
def purosBlancos(f):
	nv=0
	for x in range (len(f)):
		if f[x]!=" ":
			nv+=1
	if nv==0:
		return True
	else:
		return False
#Valida que el ingreso no sean solo espacios
def otraCosa(num):
	largo=len(num)
	cualquiera = False
	i=0
	while(not cualquiera and i<largo):
		if ((not(num[i]>="a" and num[i]<="z")) and (not(num[i]>="A" and num[i]<="Z"))):
			cualquiera = True
		i+=1
	return cualquiera
#Valida que el espacio sean solo letras
def entername():
	class Errores(Exception):
		pass
	class NoEsLetra(Errores):
		pass
	class SoloBlancos(Errores):
		pass
	class Vacia(Errores):
		pass
	sigue=True
	while(sigue):
		try:
			name = input("Ingrese nombre para esta sesion (solo letras): ")
			if(len(name)==0):
				raise Vacia
			elif(purosBlancos(name)):
				raise SoloBlancos
			else:
				if(otraCosa(name)):
					raise NoEsLetra
				else:
					sigue = False
					return name
		except(NoEsLetra):
			print("Error! Ingresaste algo que no es una letra!")
		except(SoloBlancos):
			print("Error! Ingreso solo espacios en blanco!")
		except(Vacia):
			print("Error! Nada ingreso!")
#Ingreso y validacion del nombre de usuario
def gameover(screen,myFont,RED,swidth,shigh,score):
	import pygame
	background_image=pygame.image.load("gameover.jpg").convert()
	background_image=pygame.transform.scale(background_image,(swidth,shigh))
	scor=('Your Score: {0}'.format(score))
	hiscor=gethiscore()
	Text0=myFont.render(hiscor,True,RED)	
	Text1=myFont.render(scor,True,RED)
	Text2=myFont.render('Press "r" to restar',True,RED)
	Text3=myFont.render('Press "q" to quit',True,RED)	
	done=False
	while(not done):
		for event in pygame.event.get():			
			if(event.type==pygame.QUIT):
				return False	
				done=True
			if(event.type == pygame.KEYDOWN):
				if(event.key==pygame.K_r):
					return True
					done=True				
				if(event.key==pygame.K_q):
					return False	
					done=True						
		screen.blit(background_image,[0,0])
		screen.blit(Text0,[swidth/2-200,10])
		screen.blit(Text1,[swidth/2-200,40])	
		screen.blit(Text2,[swidth/2-200,70])	
		screen.blit(Text3,[swidth/2-200,100])	
		pygame.display.flip()
#Genera pantalla de fin del juego, permite salir o reiniciar
def start(screen,swidth,shigh):
	import pygame
	background_image=pygame.image.load("start.jpeg").convert()
	background_image=pygame.transform.scale(background_image,(swidth,shigh))	
	done=False
	while(not done):
		for event in pygame.event.get():			
			if(event.type==pygame.QUIT):
				pygame.quit()
			if(event.type == pygame.KEYDOWN):
				if(event.key==pygame.K_1):
					return 1
					done=True				
				if(event.key==pygame.K_2):
					return 3
					done=True
				if(event.key==pygame.K_3):
					return 7
					done=True					
		
		screen.blit(background_image,[0,0])
		pygame.display.flip()
#Pantalla inicio juego, permite elegir que pokemon usar
def non0rand(n):
	import random	
	r=0
	while r==0:
		r=random.randint(-n,n)
	return r
#Genera un nomero aleatorio no nulo
def listas(num_obj,swidth,pwidth,minspeed,maxspeed):
	import random
	lista=[]
	for x in range(num_obj):
		lista.append([random.randint(0,swidth-pwidth),0,non0rand(maxspeed),random.randint(minspeed,maxspeed)])
		#(x,y,chx,chy)
	return lista
#Genera lista de proyectiles totales
def movnpc(lista,index,swidth,shigh,pwidth):
	import random
	lista[index][0]+=lista[index][2]
	lista[index][1]+=lista[index][3]
	if (lista[index][0]<=0 or lista[index][0]>=swidth-pwidth):
		lista[index][2]=-lista[index][2]
	return lista
#Mueve los proyectiles
def onoff(pool,pantalla):
	if len(pool)>len(pantalla):
		sigue=True
		cont=0
		while sigue:
			if (pool[cont] not in pantalla):
				pantalla.append(pool[cont])
				cont=len(pool)-1
			if cont==len(pool)-1:
				sigue=False
			cont+=1			  			
	return pantalla
#Agrega proyectiles de la lista de proyectiles totales a la lista proyectiles en pantalla
def renew(lista,shigh):
	lista2=[]
	for y in range(len(lista)):
		if (lista[y][1]>=shigh):
			lista[y][1]=0
		else:
			lista2.append(lista[y])
	return lista2
#Remueve proyectiles de la lista de proyectiles en pantalla cuando sale de la pantalla
def juego(name):
	pokemon=7
	import pygame
	pygame.init()
	BLACK = (0,0,0)
	WHITE = (255,255,255)
	GREEN = (0,255,0)
	RED = (255,0,0)
	BLUE = (0,0,255)
	width=700
	high=500
	screen=pygame.display.set_mode((width,high))
	pygame.display.set_caption('Pokemon Litio')
	myFont=pygame.font.SysFont('Calibri',50,False,False)
	clock=pygame.time.Clock()
	tmsl=0
	tmsl2=0
	tmsl3=0
	tmsl4=0
	###Setup pygame###
	pokemon=start(screen,width,high)
	###Inicio###
	pc_width=50
	pc_high=50	
	pc_x=int((width+pc_width)/2)
	pc_y=int(high-pc_high)
	pc_chx=0
	pc_chy=0
	ball_width=25
	ball_high=25
	ballpool=listas(7,width,ball_width,1,7)
	balls=[]
	berry_width=25
	berry_high=25
	berrypool=listas(7,width,berry_width,5,10)
	berries=[]
	ball_image=pygame.image.load("pokeball.png").convert_alpha()
	ball_image=pygame.transform.scale(ball_image,(ball_width,ball_high))
	berry_image=pygame.image.load("pinap.png").convert_alpha()
	berry_image=pygame.transform.scale(berry_image,(berry_width,berry_high))
	background_image=pygame.image.load("backgroundpokemon.jpg").convert()
	background_image=pygame.transform.scale(background_image,(width,high))
	if(pokemon==1):
		player_image=pygame.image.load("slowpokenew.png").convert_alpha()
		pc_speed=1
		max_life=9
	elif(pokemon==3):
		player_image=pygame.image.load("psyducknew.png").convert_alpha()
		pc_speed=3
		max_life=6
	elif(pokemon==7):
		player_image=pygame.image.load("caterpienew.png").convert_alpha()
		pc_speed=7
		max_life=3
	player_image=pygame.transform.scale(player_image,(pc_width,pc_high))
	lives=max_life
	score=0
	pygame.mixer.music.load('theme.mp3')
	pygame.mixer.music.play(-1)
	###Parametros del juego###
	done=False
	while(not done):
		for event in pygame.event.get():			
			if(event.type==pygame.QUIT):
				pygame.quit()
			if(event.type == pygame.KEYDOWN):
				if(event.key==pygame.K_RIGHT):
					pc_chx=pc_speed					
				if(event.key==pygame.K_LEFT):
					pc_chx=-pc_speed	
				if(event.key==pygame.K_UP):
					pc_chy=-pc_speed					
				if(event.key==pygame.K_DOWN):
					pc_chy=pc_speed					
			if(event.type == pygame.KEYUP):
				if(event.key==pygame.K_RIGHT and pc_chx==pc_speed ):
					pc_chx=0
				if(event.key==pygame.K_LEFT and pc_chx==-pc_speed):
					pc_chx=0
				if(event.key==pygame.K_UP and pc_chy==-pc_speed ):
					pc_chy=0
				if(event.key==pygame.K_DOWN and pc_chy==pc_speed):
					pc_chy=0
		if pc_x<=0 and pc_chx==-pc_speed:
				pc_chx=0
		if pc_x>=width-pc_width and pc_chx==pc_speed:
				pc_chx=0
		if pc_y<=int(high/2) and pc_chy==-pc_speed:
				pc_chy=0
		if pc_y>=high-pc_high and pc_chy==pc_speed:
				pc_chy=0
		pc_x += pc_chx
		pc_y += pc_chy	
		########Lo de arriba controla el movimiento del jugador########
		screen.blit(background_image,[0,0])			
		screen.blit(player_image,(pc_x,pc_y))
		###Esta parte dibuja al jugador###
		tms=pygame.time.get_ticks()//500
		if tmsl!=tms:
			balls=onoff(ballpool,balls)
			tmsl=pygame.time.get_ticks()//500
		###Esta parte define que pelotas estan en pantalla
		for x in range(len(balls)):
			balls=movnpc(balls,x,width,high,ball_width)
			screen.blit(ball_image,(balls[x][0],balls[x][1]))
			if (balls[x][0]+ball_width>=pc_x and balls[x][0]<=pc_x+pc_width) and (balls[x][1]+ball_high>=pc_y and balls[x][1]<=pc_y+pc_high):
				balls[x][1]=9999
				lives-=1
		###Esta parte mueve las pelotas y las dibuja y colisiona###
		tms=pygame.time.get_ticks()//(1000*(pc_speed))
		if tmsl2!=tms:
			berries=onoff(berrypool,berries)
			tmsl2=pygame.time.get_ticks()//(1000*(pc_speed))
		###Esta parte define que bayas estan en pantalla###
		for x in range(len(berries)):
			berries=movnpc(berries,x,width,high,berry_width)
			screen.blit(berry_image,(berries[x][0],berries[x][1]))
			if (berries[x][0]+berry_width>=pc_x and berries[x][0]<=pc_x+pc_width) and (berries[x][1]+berry_high>=pc_y and berries[x][1]<=pc_y+pc_high):
				berries[x][1]=9999
				if lives<max_life:				
					lives+=1
		###movimiento bayas###		
		balls=renew(balls,high)
		berries=renew(berries,high)
		###Esta parte remueve las pelotas y bayas que salgan de la pantalla###				
		tms=pygame.time.get_ticks()//7000
		if tmsl3!=tms:
			ballpool=listas(7,width,ball_width,1,7)			
			berrypool=listas(7,width,berry_width,5,10)
			tmsl3=pygame.time.get_ticks()//7000
		###Renueva las listas cada cierto tiempo para que haya variedad en su movimiento###
		tms=pygame.time.get_ticks()//1000
		if tmsl4!=tms:
			score+=lives
			tmsl4=pygame.time.get_ticks()//1000
		###actualiza puntaje###				
		f1=('Lives: {0}'.format(lives))		
		myText1=myFont.render(f1,True,RED)
		screen.blit(myText1,[0,0])
		f2=('Score: {0}'.format(score))
		myText2=myFont.render(f2,True,BLUE)
		screen.blit(myText2,[0,30])
		###Muestra vida y puntaje###
		pygame.display.flip()
		clock.tick(60)
		if lives==0:
			done=True
		###Termina el juego cuando se acaban las vidas###
	scores = open('PokeScore.txt','a')	
	scores.write('{0}->{1}'.format(name,score)+'\n')
	scores.close()
	pygame.mixer.music.stop()
	reset=gameover(screen,myFont,RED,width,high,score)
	###Terminan la partida###
	return reset
					
main()
