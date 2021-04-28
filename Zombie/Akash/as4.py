import random
import math

from gamelib import *

class ZombieCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)

    def selectBehavior(self):
        prob = random.random()

        # If health is less than 50%, then heal with a 10% probability
        if prob < 0.1 and self.getHealth() < self.getInitHealth() * 0.5:
            return HealEvent(self)

        # Pick a random direction to walk 1 unit (Manhattan distance)
        x_off = random.randint(-1, 1)
        y_off = random.randint(-1, 1)

        # Check the bounds
        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()
        x, y = self.getPos()
        if x + x_off < 0 or x + x_off >= size_x:
            x_off = 0
        if y + y_off < 0 or y + y_off >= size_y:
            y_off = 0

        return MoveEvent(self, x + x_off, y + y_off)

class PlayerCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)
        # You may add any instance attributes you find useful to save information between frames
        self.rc = self.RoundCounter()
        self.sc = self.SinceCounter()

    def selectBehavior(self):
        # Replace the body of this method with your character's behavior
        
        # self.
        
        import re
        
        # Count the current round number
        # Game starts on round 1
        self.rc.round_counter += 1
        
        # Note that it's been one additional round since each action
        self.sc.since_counter = [ since_action + 1
                                  for since_action in self.sc.since_counter ]
        
        print('round {}'.format(self.rc.round_counter))

        print('since attack: {}'.format(self.sc.since_counter[0]))
        print('since heal  : {}'.format(self.sc.since_counter[1]))
        print('since scan  : {}'.format(self.sc.since_counter[2]))
        
        # prob = random.random()
        # hi = ZombieHunter.heal_count() in main
        
        # self.getScanResults()
        # print(self.getScanResults())
        
        # print(ScanData().getPos())
        
        x, y = self.getPos()
        
        # try:
        print(type(self.getScanResults()))
        for res in self.getScanResults():
            print("Radical:", type(str(res)))
            print(len(self.getScanResults()))
            
        if len(self.getScanResults()) >= 1:
            
            # print('epic:', self.getScanResults()[0])
        # if len(self.getScanResults()) > 0:

            # Store the ID and position of each scanned zombie
            positions = [ re.findall('\d', str(res))
                          for res in self.getScanResults() ]
            
            # Append Manhattan distance to each row
            for row in positions:
                row[0] = int(row[0])
                row[1] = abs(int(row[1]) - x) # x-Manhattan displacement from Player to Zombie
                row[2] = abs(int(row[2]) - y) # y-Manhattan displacement from Player to Zombie
                row.append(sum(row[1:3])) # Add total Manhattan distance
            
            # Sorts positions from closest to furthest to Player
            # (default ascending down the list)
            positions.sort(key = lambda x: x[3])
            
            print('yo i can see zombie', positions[0][0])
            
            self.sc.since_counter[0] = -1 # note that this ended with an Attack
            return AttackEvent(self, positions[0][0])
            
            
            # print(self.getTargetID)
            
            # len(positions)
            
            # for i in positions:
            #     print('\n')
            #     print(i)
            #     print('\n') 
            
            # for res in self.getScanResults():
            #     print('\n')
            #     print(res)
            #     print('\n')
            
            # | (position: (| , | ))
            # print('\n')
            # print(positions)
            # print('\n')
        # for res in self.getScanResults():
        #     print(res)
        # print(positions==[])
        # if len(positions) > 0:
        #     for idx, row in positions:
        #         positions[idx].append(abs(x-positions[idx][1]) + abs(y-positions[idx][2]))
        #         print('hey', idx, row)
        # else:
        #     print('No scan data available')
        
            
        # positions.sort(key = lambda x: x[2])
        # if type(positions[0] == list): # if it's a list of multiple zombies
        #     targetID = positions[0][0] # then select the closest zombie's ID
        # elif type(positions[0] == int): # if it's just one zombie's info
        #     targetID = positions[0] # then select the closest zombie's ID
            
        # if self.rc.round_number()-1 % 2 == 0:
        #     return AttackEvent(self, targetID)
        
        # print("It worked!")
            
        # except (AttributeError, IndexError):
        #     pass
        

        
        # for res in self.getScanResults():
        #     print('get a load of "{}"'.format(str(res)))
        
        # Scanning every 10 rounds
        # if self.rc.round_number() % 5 == 0: # scan on every 5th round
        
        self.sc.since_counter[2] = -1 # note that this ended with a Scan
        return ScanEvent(self) # scan the area
        

        
        # try:
        # print(ScanData(self))
        # except \:
            
                
        
           
        # 
        # self.heal_counter = 0
        # self.heal_counter += 1
        # self.hehe = self.getHealth()
        # print('yowza', self.hehe)
        
        # if self.getHealth():
            
        # try:
        #     round_counter += 1
        # except NameError:
        #     round_counter = 0
        # print(self.mp.outie())
        
        # try:
        #     round_counter += 1
        #     print('hello', round_counter)
        # except NameError:
        #     round_counter = 0
        #     print('hey', round_counter)
        
        # if round_counter % 5 == 0:
        # return ScanEvent(self)
        
                
        # # If health is less than 25%, then heal
        # if self.getHealth() < self.getInitHealth() * 0.25:
        #     return HealEvent(self)
        
        # # Pick a random direction to walk 1 unit (Manhattan distance)
        # x_off, y_off = 4, 4
        
        # while abs(x_off) + abs(y_off) > 3:
        #     x_off = random.randint(-3, 3)
        #     y_off = random.randint(-3, 3)
        #     print('hey:', abs(x_off)+abs(y_off))
        #     if abs(x_off) + abs(y_off) <= 3:
        #         continue

        # Check the bounds
        # map_view = self.getMapView()
        # size_x, size_y = map_view.getMapSize()
        # x, y = self.getPos()
        # if x + x_off < 0 or x + x_off >= size_x:
        #     x_off = 0
        # if y + y_off < 0 or y + y_off >= size_y:
        #     y_off = 0

        # return MoveEvent(self, x + x_off, y + y_off)
        
        # print('loooool:', self.health)
        # pass
        
        heydar = 4
        
    # class MindPalace:
    #     def __init__(self):
    #         # super().__init__()
    #         # self.round_counter = 1
    #         try:
    #             self.round_counter += 1
    #         except AttributeError:
    #             self.round_counter = 1
    #     def outie(self):
    #         print('yowza: {}'.format(self.round_counter))
    
    
    class RoundCounter:
        def __init__(self, round_counter = 0):
            self.round_counter = round_counter
            # self.hiswins = hiswins
    
        # def add_round(self):
        #     self.round_counter += 1
            
        # def round_number(self):
        #     return self.round_counter
    
    class SinceCounter:
        def __init__(self, since_counter = [0, 0, 0], toggle = [0, 1, 1]):
            self.since_counter = since_counter # rounds since last [attack, heal, scan]
            self.toggle = toggle # if Player is allowed to [attack, heal, scan] (no: 0 or yes: 1)
            
        # def add_since_attack(self):
        #     self.round_counter += 1
            
        # def stab(self):
        #     self.attack_toggle = 0
    
        # def his_score(self):
        #     self.hiswins += 1
    
        # @property
        # def best (self):
        #     return max ( [self.mywins, self.hiswins] )
            
        # def __str__(self):
        #     return 'oh yeah dab on em {}'.format(self.round_counter)
        
    # def __str__(self):
        # return 'bruuuuh'+
        # pass
