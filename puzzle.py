import pygame
from pygame.locals import *
import random
import time
import math
import numpy as np

from solver import Solver
def start_game(dimension,heuristic):
	assert heuristic in ["malplace","distance"]
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((598,598))
	screen.fill((0,0,0))
	pygame.display.set_caption("Arrange the Numbers!")
	font = pygame.font.Font('fonts/Adca.ttf', 35)
	clock = pygame.time.Clock()
	victory = pygame.mixer.Sound("sounds/TaDa.ogg")
	button = pygame.Rect(450, 450, 20, 20)
	empty_x = (dimension)*100
	empty_y = (dimension)*100

	RED = (255,0,0)
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	GREEN = (0,255,0)
	colors = [(134,142,150),(250,82,82),(230,73,128),(190,75,219),(121,80,242),(76,110,245),(34,138,230),(21,170,191),(18,184,134),(64,192,87),(130,201,30),(250,176,5),(253,126,20),(233,236,239),(255,236,153),(163,218,255),(255,154,51)] 
	
	class Tile(object):
	    def __init__(self, num, x, y):
	        self.number = num
	        self.x = x
	        self.y = y
	        self.width = 99
	        self.height = 99
	        
	    def draw(self):
	        pygame.draw.rect(screen, colors[self.number], (self.x, self.y, self.width, self.height), 0)
	        text = font.render(str(self.number), True, WHITE)
	        textRect = text.get_rect(center=((2*self.x+self.width)/2, (2*self.y+self.height)/2))
	        screen.blit(text, textRect)
	        
	    def moveIt(self, dist):
	        final_x = self.x + dist[0]
	        final_y = self.y + dist[1]
	        
	        while self.x != final_x or self.y != final_y:
	            screen.fill(WHITE, [self.x, self.y, 99, 99])
	            self.x += int(dist[0]/50)
	            self.y += int(dist[1]/50)
	            self.draw()
	            pygame.display.update()

	        clock.tick(60)
	    def mat_pos(self):
	    	return (self.y//100-1,self.x//100-1)

	def count_inversions(num_order):
	  inversions = 0
	  for i in range(len(num_order)-1):
	    for k in range(i+1, len(num_order)):
	      if num_order[i] > num_order[k]:
	        inversions += 1
	  return inversions

	def moves_display(mytext):
	    txt = font.render(mytext, True, WHITE)
	    textRect = txt.get_rect(center=(299, 550))
	    screen.blit(txt, textRect)

	def show_congrats():
	    txt = font.render("Congratulations! You did it!", True, GREEN)
	    textRect = txt.get_rect(center=(299, 49))
	    screen.blit(txt, textRect)
	    finalTile = Tile(dimension*dimension, empty_x, empty_y)
	    finalTile.draw()
	    pygame.display.update()
	    print("\nYou solved it! Game window closing in 10 seconds....")

	def get_surrounding(listOfTiles):
		surronding={}
		xy_dists=[[-100, 0],[100, 0],[0, -100],[0, 100]]
		xy_keys=[K_LEFT,K_RIGHT,K_UP,K_DOWN]
		for tile in listOfTiles:
			for dist,key in zip(xy_dists,xy_keys):
				if tile.x + dist[0] == empty_x and tile.y + dist[1] == empty_y:
					surronding[tile.number]=key
		return surronding

	def tile_mat(listOfTiles,dimension):
		tiles=[[0 for i in range(dimension)] for i in range(dimension)]
		for tile in listOfTiles:
			tiles[tile.mat_pos()[0]][tile.mat_pos()[1]]=tile.number
		return tiles

	def tile_list(listOfTiles,dimension):
		result=[]
		mat=tile_mat(listOfTiles,dimension)
		for i in range(dimension):
			for j in range(dimension):
				result.append(mat[i][j])
		return result
	def solution(listOfTiles,dimension):
		start=tile_list(listOfTiles,dimension)
		astar=Solver(dimension,start,heuristic)
		solution=astar.solve()
		return solution[::-1]

	

	corret_matches=[]
	for i in range(1,dimension+1):
		for j in range(1,dimension+1):
			if(i!=dimension or j!=dimension ):
				corret_matches.append([j*100,i*100,(i-1)*dimension+j])

	print("matches : ",corret_matches)				
	def detectWin():
	    for tile in listOfTiles:
	        curr_arrangement = [tile.x, tile.y, tile.number]
	        if curr_arrangement not in corret_matches:
	            return False        
	    return True

	nums=list(range(1,dimension*dimension))
	random.shuffle(nums)
	while count_inversions(nums) % 2 != 0:
	  random.shuffle(nums)
	listOfTiles = []
	move_counter = 0
	index = 0
	
	pygame.draw.rect(screen, WHITE, (98, 98, (dimension)*100+3, (dimension)*100+3))
	for y in range(100, (dimension+1)*100, 100):
	    for x in range(100, (dimension+1)*100, 100):
	        if index < len(nums):
	            da_num = nums[index]
	            newTile = Tile(da_num, x, y)
	            listOfTiles.append(newTile)
	            newTile.draw()
	            index += 1
	pygame.display.update()

	def move(key,listOfTiles,empty_x,empty_y,move_counter):
		 
		if key == K_LEFT:
			xy_dist = [-100, 0]
		if key == K_RIGHT:
		 	xy_dist = [100, 0]
		if key == K_UP:
		 	xy_dist = [0, -100]
		if key == K_DOWN:
		 	xy_dist = [0, 100]

		for tile in listOfTiles:
		 	if tile.x + xy_dist[0] == empty_x and tile.y + xy_dist[1] == empty_y:
		 		move_counter += 1
		 		empty_x = tile.x
		 		empty_y = tile.y
		 		tile.moveIt(xy_dist)
		 		break
		return listOfTiles,empty_x,empty_y,move_counter

	running = True
	while running:

	    for event in pygame.event.get():
	        if event.type == QUIT:
	            running = False
	            
	        elif event.type == MOUSEBUTTONDOWN:
	            this_pos = pygame.mouse.get_pos()
	            
	            x = int(math.floor(this_pos[0] / 100.0)) * 100
	            y = int(math.floor(this_pos[1] / 100.0)) * 100
	            
	            li = [(empty_x - x), (empty_y - y)]
	            if 0 in li and (100 in li or -100 in li):
	                for tile in listOfTiles:
	                    if tile.x == x and tile.y == y:
	                        move_counter += 1
	                        empty_x = tile.x
	                        empty_y = tile.y
	                        tile.moveIt(li)
	    
	        elif event.type == KEYDOWN:
	            arrows = [K_LEFT, K_RIGHT, K_UP, K_DOWN]
	            
	            if event.key == K_ESCAPE:
	                running = False
	            
	            elif event.key in arrows:
	                xy_dist = [None, None]
	                
	                if event.key == K_LEFT:
	                    xy_dist = [-100, 0]
	                if event.key == K_RIGHT:
	                    xy_dist = [100, 0]
	                if event.key == K_UP:
	                    xy_dist = [0, -100]
	                if event.key == K_DOWN:
	                    xy_dist = [0, 100]

	                for tile in listOfTiles:
	                    if tile.x + xy_dist[0] == empty_x and tile.y + xy_dist[1] == empty_y:
	                        move_counter += 1
	                        empty_x = tile.x
	                        empty_y = tile.y
	                        tile.moveIt(xy_dist)
	                        break

	            elif event.key==K_SPACE:
	            	num=int(input("give permutation number here : "))
	            	surr=get_surrounding(listOfTiles)
	            	mat=tile_mat(listOfTiles,dimension)
	            	lis=tile_list(listOfTiles,dimension)
	            	print("surrounding : ",surr)
	            	print("tiles mat: ",mat)
	            	print("tiles list: ",lis)

	            	event=pygame.event.Event(KEYDOWN,{"key":surr[num]})
	            	pygame.event.post(event)

	            elif event.key==K_RETURN:
	            	sol=solution(listOfTiles,dimension)
	            	print("sol : ",sol)
	            	
	            	for number in sol:
	            		print("number : ",number)
	            		surr=get_surrounding(listOfTiles)	
	            		listOfTiles,empty_x,empty_y,move_counter=move(surr[number],listOfTiles,empty_x,empty_y,move_counter)
	            		time.sleep(1)
	            		


	    screen.fill(BLACK, [200, 515, 200, 85])
	    moves_display("Moves: " + str(move_counter))
	    pygame.display.update()
	    clock.tick(60)
	    
	    if detectWin() == True:
	        show_congrats()
	        victory.play()
	        running = False
	        time.sleep(3)
	pygame.quit()

if __name__ == '__main__':
	print("""Notes : 
	Le jeu de taquin admet les dimensions 2,3 et 4.
	Vous pouvez jouer avec les fleshes du clavier.
	A tout moment de la partie, vous pouvez clicker sur le button entree
	pour lancer l'assistance automatique avec l'algorithme A*
		

		""")
	dim=input("Entrer les dimensions du taquin : ")
	heuristic=input("Donner l'heuristic entre 'malplace' et 'distance' : ")
	start_game(int(dim),heuristic)