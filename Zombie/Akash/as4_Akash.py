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
        # self.ctr = self.RoundCounter()
        self.ctr = self.Counter()
        self.dam = self.Damage()
        # self.ctr.rounds = self.ctr.rounds
        # self.ctr.since = self.ctr.since

    def selectBehavior(self):
        # Replace the body of this method with your character's behavior
        
        # Count the current round number and rounds since each event
        # Game starts on round 1, with "0" rounds since each event
        self.ctr.add_round()
        print(self.ctr)
        
        # Need to Scan for the first time
        # Otherwise the rest of the program, ScanEvent if we've just done a MoveEvent
        if (self.ctr.rounds[0] == 1) or (self.ctr.rounds[3] == 1):
            # print('SCAN 53!')
            self.ctr.reset_round('scan') # note that we're doing a ScanEvent
            return ScanEvent(self)
        
        
        ## Order of Priority
        # Perform initial ScanEvent (only round 1)
        # If we have just moved, ScanEvent again
        # Check scan results
            # HealEvent if in danger of low health
            # If zombies appear on scan
                # If we can inflict good damage
                    # AttackEvent the closest one
                # If we can't damage them much
                    # Move elsewhere
        # ScanEvent for zombies
        # 
        # Check health
            
            # 1-1. If health is below maximum possible attack damage, then heal
       
        scan_results = self.getScanResults()
        obj_pos = self.getPos()
        map_view = self.getMapView()
        
        # First priority event is healing if under a certain threshold
        # If health is less than 25%, then heal
        
        # Check if health is lower than the max damage the nearest zombie could inflict
        try:
            id_pos = self.dam.calc(scan_results, obj_pos) # analyze scan data
            damage_threshold = id_pos[0][1]*100 + self.getInitHealth() * 0.02
            # find max factor of damage that a zombie could inflict given the positions, excluding factor of health
            # also account for health decrement of each round
            
        # If there are no scan results or no zombies nearby, set the user-defined safe health threshold to 0.25 of original health
        except (NameError, IndexError): # if no zombies are in range as of last scan
            print('no zombies in range')
            damage_threshold = self.getInitHealth() * 0.1
        
        print('Damage threshold:', damage_threshold)
        
        # If health is below a safe level, given zombie proximity, then HealEvent
        if (self.getHealth() <= damage_threshold) and (self.ctr.events[2] <= 5): # If player health is below the safe threshold
            self.ctr.reset_round('heal')
            # print('HEAL 99!')
            return HealEvent(self)
        
        
        # Else (if health is above the safe level), either AttackEvent or MoveEvent based on to scan data
        else:
            if self.ctr.rounds[4] <= 2: # If it's been at most 2 rounds since ScanEvent
                if len(id_pos) >= 1: # and if there is at least one zombie in the scan data
                    
                    print('Damage we can do', self.getHealth()*id_pos[0][1])
                    
                    if self.getHealth()*id_pos[0][1] > 0.05: # If the damage we'll inflict is higher than the user-defined threshold
                        self.ctr.reset_round('attack') # note that we're doing an AttackEvent
                        # print('ATTACK 111!')
                        return AttackEvent(self, id_pos[0][1]) # then AttackEvent
                    # else: # Else, if our damage is not high enough
                    # # (but it's still been at most 2 rounds since last ScanEvent and we saw a zombie)
                        # # Then we do a MoveEvent
                        # x, y = obj_pos
                        # x_off, y_off = self.dam.movement(map_view, obj_pos)
                        # self.ctr.reset_round('move') # note that we're doing a MoveEvent
                        # print('MOVE 123!')
                        # return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
                        
                else: # If it's been at most 2 rounds since ScanEvent, but we see no zombie
                    x, y = obj_pos
                    x_off, y_off = self.dam.movement(map_view, obj_pos)
                    self.ctr.reset_round('move') # note that we're doing a MoveEvent
                    # print('MOVE 123!')
                    return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
            
            # Else, if it's been more than 2 rounds since last ScanEvent (but we see no zombie), then ScanEvent
            else:
                self.ctr.reset_round('scan') # note that we're doing a ScanEvent
                # print('SCAN 129!')
                return ScanEvent(self) # then ScanEvent
                
    
    ## Mind Palace
        
    class Counter:
        def __init__(self, rounds = [0, 0, 0, 0, 0], # rounds since event
                           events = [0, 0, 0, 0, 0], # number of times we've done event
                           toggle = [1, 1, 1, 1, 1], # toggle to allow event
                           next_pos = (0, 0)         # next position for movement
                           ):
            # rounds since beginning, attack, last heal, last scan
            self.rounds = rounds
            self.events = events
            self.toggle = toggle # if Player is allowed to [attack, heal, scan] (no: 0 or yes: 1)
        
        def add_round(self):
            self.rounds = [ rounds_since + 1 for rounds_since in self.rounds ]
            
        def select_round(self, event):
            if event == 'start':
                return self.rounds[0]
            if event == 'attack':
                return self.rounds[1]
            if event == 'heal':
                return self.rounds[2]
            if event == 'move':
                return self.rounds[3]
            if event == 'scan':
                return self.rounds[4]
            
        def reset_round(self, event):
            if event == 'attack':
                self.events[1] += 1
                self.rounds[1] = 0
            if event == 'heal':
                self.events[2] += 1
                self.rounds[2] = 0
                # print('UHHH')
            if event == 'move':
                self.events[3] += 1
                self.rounds[3] = 0
            if event == 'scan':
                self.events[4] += 1
                self.rounds[4] = 0
            
                
        def __str__(self):
            
            rows = [ 'round {}',
                     '{} since attack, {} since heal, {} since move, {} since scan',
                     '{} attacks, {} heals, {} moves, {} scans']
            
            printout = '\n'.join(rows).format(*self.rounds, *self.events[1:5])
            
            return printout
        
    class Damage:
        
        def __init__(self, scan_results=0, obj_pos=(0,0), map_view=(0,0)):
            self.scan_results = scan_results
            self.obj_pos = obj_pos
            self.map_view = map_view
            
        def calc(self, scan_results, obj_pos):
            
            id_pos = [] # initialize
            for target in scan_results: # for each scanned zombie
                
                target_id = target.getID() # get target's ID
                # print('zombie_health:', target_id.getHealth())
                # print('fam look it\'s zombie', target)
                target_pos_x, target_pos_y = target.getPos() # get target's position
                obj_pos_x, obj_pos_y = obj_pos
                dist = math.hypot(obj_pos_x - target_pos_x, obj_pos_y - target_pos_y) # get distance from attacker to target
                scale_factor = 1.0 / math.exp(dist) # attack damage scale factor
                id_pos.append([target_id, scale_factor]) # append the current target ID and damage scale factor to the collection
                print('We can see Zombie {}'.format(target_id))
                
            id_pos.sort(key = lambda x: x[1], reverse=True) # sort list from highest to lowest attack scale factor
            
            return id_pos
        
        # Function to control Player movement
        def movement(self, map_view, obj_pos): # takes MapView and Pos objects from Player
            print('MOVEMENT')
            
            x_off, y_off = 4, 4 # initialize offset in x- and y-coordinates
            # start with invalid offsets to initialize while loop
            
            while abs(x_off) + abs(y_off) > 3: # while the sum of the offsets is invalid
                x_off = random.randint(-3, 3) # randomly select a valid x-offset
                y_off = random.randint(-3, 3) # randomly select a valid y-offset
                # print('hey:', abs(x_off)+abs(y_off))
                if abs(x_off) + abs(y_off) <= 3: # if the sum is valid
                    continue # then leave the while loop and continue
    
            # Check the bounds
            # map_view = map_view # 
            size_x, size_y = map_view.getMapSize() # get the dimensions of the map
            x, y = obj_pos # get the player's current position
            if x + x_off < 0 or x + x_off >= size_x: # if the new x is invalid
                x_off = 0 # don't move in the x-direction
            if y + y_off < 0 or y + y_off >= size_y: # if the new y is invalid
                y_off = 0 # don't move in the Y-direction
                
            return (x_off, y_off) # return the x and y offsets
