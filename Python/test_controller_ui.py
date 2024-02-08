import pygame

class Robot_UI:
    def __init__(self):
        pygame.display.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        print(self.joysticks)
    
    def _compensate_drift(self):
        pass

    def detect_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(event)
                if event.type == pygame.JOYBUTTONUP:
                    print(event)
                if (event.type == pygame.JOYAXISMOTION and self.joysticks[0].get_axis(5) > -1.0) :
                    print(event)
                if event.type == pygame.JOYHATMOTION:
                    print(event) 

if __name__ == "__main__":
    r = Robot_UI()
    r.detect_key()