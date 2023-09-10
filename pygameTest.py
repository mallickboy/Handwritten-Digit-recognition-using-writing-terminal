# importing pygame module
import pygame

# importing sys module
import sys

# initialising pygame
pygame.init()

# creating display
display = pygame.display.set_mode((300, 300))
count=0
# creating a running loop
while True:
	
	# creating a loop to check events that
	# are occurring
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		# checking if keydown event happened or not
		if event.type == pygame.KEYDOWN:
		
			# if keydown event happened
			# than printing a string to output
			print("A key has been pressed")
			if event.key == "K_ESCAPE":
				print("Esc")
				pygame.quit()
		if event.type==pygame.MOUSEBUTTONDOWN:
			count+=1
			print("Clicked",count)
