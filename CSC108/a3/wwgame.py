import sys, pygame, random
from ww import *
pygame.init()

ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24.png", ww))
ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))
ww.add_actor(Wall("icons/wall.jpg", ww, 4, 4))
ww.add_actor(Wall("icons/wall.jpg", ww, 5, 4))
ww.add_actor(Wall("icons/wall.jpg", ww, 7, 9))
ww.add_actor(Wall("icons/wall.jpg", ww, 8, 9))
ww.add_actor(Wall("icons/wall.jpg", ww, 9, 9))
ww.add_actor(Wall("icons/wall.jpg", ww, 9, 10))
ww.add_actor(Wall("icons/wall.jpg", ww, 9, 11))
ww.add_actor(Wall("icons/wall.jpg", ww, 15, 15))
ww.add_actor(Wall("icons/wall.jpg", ww, 15, 16))
ww.add_actor(Wall("icons/wall.jpg", ww, 15, 17))
ww.add_actor(Wall("icons/wall.jpg", ww, 15, 18))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 0, 3, 1))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 7, 4, 5))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 4, 10, 3))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 5, 20, 2))

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
# This while loop is for adding random number of boxes into the stage.
'''

'''
num_boxes=0
while num_boxes<100:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
        num_boxes+=1

num_sticky = 0
while num_sticky < 5:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(StickyBox("icons/sticky_box.png", ww, x, y))
        num_sticky += 1


        
# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
#This while loop is for every 100 millisecond, it will receive and respond to a command.
while True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            ww.player_event(event.key)
    ww.step()
    ww.draw()
