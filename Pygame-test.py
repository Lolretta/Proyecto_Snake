import pygame

pygame.init()
display = pygame.display.set_mode( (880, 600))
pygame.display.update()
open = True
while open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open = False
pygame.quit()
quit()
