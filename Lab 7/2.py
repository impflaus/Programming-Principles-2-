import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
black = (0, 0, 0)
screen.fill(black)
isDone = True
index = 0
sounds = ["Lab 7/Sounds /Akon_Eminem_-_Smack_That_64767700.mp3", "Lab 7/Sounds /Eurythmics_-_Sweet_Dreams_Are_Made_of_This_48046023.mp3", "Lab 7/Sounds /Twenty_One_Pilots_-_Stressed_Out_47828699.mp3"]
isPaused = False
isPlayed = True

while isDone:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = False
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if index == len(sounds) - 1:
                index = 0
            else: index += 1

            isPaused = False
            isPlayed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if index == 0:
                index = len(sounds) - 1
            else:
                index -= 1
            isPaused = False
            isPlayed = True

        if event.type == pygame.KEYDOWN and isPlayed:
            if isPaused:
                pygame.mixer.music.unpause()
                isPaused = not isPaused
            else:
                pygame.mixer.music.load(sounds[index])
                pygame.mixer.music.play(0)
            isPlayed = not isPlayed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not isPlayed:
            pygame.mixer.music.pause()
            isPlayed = not isPlayed
            isPaused = not isPaused

    pygame.display.flip()