import pygame
import time
import math

pygame.init()

clock_face = pygame.image.load("Lab 7/images /nohands.jpg")  
minute_hand = pygame.image.load("Lab 7/images /big_hand.png")
second_hand = pygame.image.load("Lab 7/images /small_hand.png")


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")


CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2


minute_hand_rect = minute_hand.get_rect(center=(CENTER_X, CENTER_Y))
second_hand_rect = second_hand.get_rect(center=(CENTER_X, CENTER_Y))

def rotate_hand(image, angle, offset_x=0, offset_y=0):
    """ Rotates a hand image and positions it correctly around the clock center. """
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=(CENTER_X + offset_x, CENTER_Y + offset_y))
    return rotated_image, rotated_rect

running = True
while running:
    screen.fill((255, 255, 255)) 
    screen.blit(clock_face, (0, 0)) 

     
    t = time.localtime()
    minutes = t.tm_min
    seconds = t.tm_sec

    minute_angle = -(minutes * 6)  
    second_angle = -(seconds * 6) 

    rotated_minute_hand, minute_rect = rotate_hand(minute_hand, minute_angle)
    rotated_second_hand, second_rect = rotate_hand(second_hand, second_angle)

    screen.blit(rotated_minute_hand, minute_rect.topleft)
    screen.blit(rotated_second_hand, second_rect.topleft)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(0.1) 

pygame.quit()