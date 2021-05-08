import random
import math

from gamelib import *

class ZombieCharacter(ICharacter):
    # def __init__(self, obj_id, health, x, y, map_view):
    #     ICharacter.__init__(self, obj_id, health, x, y, map_view)

    # def selectBehavior(self):
        # prob = random.random()

        # # If health is less than 50%, then heal with a 10% probability
        # if prob < 0.1 and self.getHealth() < self.getInitHealth() * 0.5:
        #     return HealEvent(self)

        # # Pick a random direction to walk 1 unit (Manhattan distance)
        # x_off = random.randint(-1, 1)
        # y_off = random.randint(-1, 1)

        # # Check the bounds
        # map_view = self.getMapView()
        # size_x, size_y = map_view.getMapSize()
        # x, y = self.getPos()
        # if x + x_off < 0 or x + x_off >= size_x:
        #     x_off = 0
        # if y + y_off < 0 or y + y_off >= size_y:
        #     y_off = 0

        # return MoveEvent(self, x + x_off, y + y_off)
    
    
    
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)
        # You may add any instance attributes you find useful to save information between frames
        # self.ctr = self.RoundCounter()
        # self.ctr = self.Counter()
        # self.dam = self.Damage()
        self.hey = 0
        
        # Storing records of actions between turns
        
        # number of times we've performed each event
        self.num_of = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0} # number of times we've done event
        # rounds since the previous run of each event
        self.since_previous = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0} # rounds since event
        # if Player is allowed to [attack, heal, scan] (no: 0 or yes: 1)
        self.toggle = {'start': 0, 'attack': 1, 'heal': 1, 'move': 1, 'scan': 1} # toggle to allow event
        # next position for movement
        self.next_pos = (0, 0)         
        

    def selectBehavior(self):
        # Replace the body of this method with your character's behavior
        
        def add_round(self):
            '''
            Count that one round has passed
            Also note that it has been one round since each Event.
            The Character calls this at the beginning of each turn.
            '''
            for event in self.since_previous:
                self.since_previous[event] += 1
                
        def reset_round(self, event):
            '''
            Reset the number of rounds since the latest performed Event.
            Placed before calling an event.
                        
            Args:
                event: a string (lowercase) for the Event that is called in the current turn
            '''
            self.num_of[event] += 1 # show that we've executed this event
            self.since_previous[event] = 0 # reset the rounds since previous execution of event
        
        
        # Calculate the damage that the Character can inflict on the scanned opponents
        
        def calc(self, scan_results, obj_pos):
            '''
            Calculate the damage that the Character can do to each opponent.
            
            Args:
                scan_results: info taken from object Character's ScanData
                obj_pos: the object Character's current position on the board
            '''
            
            id_pos = [] # initialize
            for target in scan_results: # for each scanned zombie
                target_id = target.getID() # get target's ID
                # print('zombie_health:', target_id.getHealth())
                # print('fam look it\'s zombie', target)
                
                if target_id == 0:
                    target_pos = target.getPos() # get target's position
                    target_pos_x, target_pos_y = target_pos
                    obj_pos_x, obj_pos_y = obj_pos
                    dist = math.hypot(obj_pos_x - target_pos_x, obj_pos_y - target_pos_y) # get distance from attacker to target
                    scale_factor = 1.0 / math.exp(dist) # attack damage scale factor
                    id_pos.append([target_id, scale_factor, target_pos]) # append the current target ID and damage scale factor to the collection
                    print('We can see Player {}'.format(target_id))
                
            id_pos.sort(key = lambda x: x[1], reverse=True) # sort list from highest to lowest attack scale factor
            
            print(id_pos)
            
            return id_pos
        
        
        # Function to control Player movement
        def movement(self, map_view, obj_pos): # takes MapView and Pos objects from Player
            '''
            
            '''
            # print('MOVEMENT')
            
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
        
        def print_rounds(self):
            rows = [ '\nround {}',
                     '{} since attack, {} since heal, {} since move, {} since scan',
                     '{} attacks, {} heals, {} moves, {} scans' ]
        
            round_printout = '\n'.join(rows).format(
                       *self.since_previous.values(),
                        self.num_of['attack'], self.num_of['heal'], self.num_of['move'], self.num_of['scan'])
            
            print(round_printout)
            
            return
        
        
        # Count the current round number and rounds since each event
        # Game starts on round 1, with "0" rounds since each event
        add_round(self)
        print_rounds(self)
        
        # self.hey += 1
        # print('yo', self.hey)
        
        # Need to Scan for the first time
        # Otherwise the rest of the program, ScanEvent if we've just done a MoveEvent
        if (self.since_previous['start'] == 1) or (self.since_previous['move'] == 1):
            if self.getHealth() >= self.getInitHealth() * 0.1: # and if we're above 1/10 of original health
                # print('SCAN 53!')
                reset_round(self, 'scan') # note that we're doing a ScanEvent
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
        obj_id = self.getID()
        obj_pos = self.getPos()
        map_view = self.getMapView()
        
        # First priority event is healing if under a certain threshold
        # If health is less than 25%, then heal
        
        # Check if health is lower than the max damage the nearest zombie could inflict
        try:
            id_pos = calc(self, scan_results, obj_pos) # analyze scan data
            
            if obj_id == 0: # If we're the player
                opponent_max_health = 100 # show zombies' max health
                damage_threshold = id_pos[0][1]*opponent_max_health + self.getInitHealth() * 0.02
            else: # If we're a zombie
                opponent_max_health = 1000 # show player's max health
                damage_threshold = 0.05*self.getInitHealth()
            # find max factor of damage that a zombie could inflict given the positions, excluding factor of health
            # also account for health decrement of each round
            
        # If there are no scan results or no zombies nearby, set the user-defined safe health threshold to 0.25 of original health
        except (IndexError): # if no zombies are in range as of last scan
            # print('no zombies in range')
            damage_threshold = self.getInitHealth() * 0.06
        
        print('Damage threshold:', damage_threshold)
        
        # If health is below a safe level, given zombie proximity, then HealEvent
        if (self.getHealth() <= damage_threshold) and (self.num_of['heal'] < 5):
            # If player health is below the safe health threshold and has healed fewer than 5 times so far
            reset_round(self, 'heal')
            print('HEAL 99!')
            return HealEvent(self)
        
        
        # Else (if health is above the safe level), either AttackEvent or MoveEvent based on to scan data
        else:
            if self.since_previous['scan'] <= 4: # If it's been at most 2 rounds since ScanEvent
                id_pos = calc(self, scan_results, obj_pos)
                if len(id_pos) >= 1: # and if there is at least one zombie in the scan data
                    
                    print('Damage we can do', self.getHealth()*id_pos[0][1])
                    
                    if self.getHealth()*id_pos[0][1] > 0: # If the damage we'll inflict is higher than the user-defined threshold
                        reset_round(self, 'attack') # note that we're doing an AttackEvent
                        # print('ATTACK 111!')
                        return AttackEvent(self, id_pos[0][1]) # then AttackEvent
                    else: # Else, if our damage is not high enough
                    # (but it's still been at most 2 rounds since last ScanEvent and we saw a zombie)
                        # Then we do a MoveEvent
                        x, y = obj_pos
                        x_off, y_off = movement(self, map_view, obj_pos)
                        reset_round(self, 'move') # note that we're doing a MoveEvent
                        # print('MOVE 123!')
                        return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
                        
                        # # Then we do an AttackEvent
                        # reset_round(self, 'attack') # note that we're doing a AttackEvent
                        # return AttackEvent(id_pos[0][1])
                        
                else: # If it's been at most 2 rounds since ScanEvent, but we see no zombie
                    x, y = obj_pos
                    x_off, y_off = movement(self, map_view, obj_pos)
                    reset_round(self, 'move') # note that we're doing a MoveEvent
                    # print('MOVE 123!')
                    return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
            
            # Else, if it's been more than 2 rounds since last ScanEvent (but we see no zombie), then ScanEvent
            else:
                reset_round(self, 'scan') # note that we're doing a ScanEvent
                # print('SCAN 129!')
                return ScanEvent(self) # then ScanEvent
            
            
        print('hahaha')
    
        
    
        
    


class PlayerCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)
        # You may add any instance attributes you find useful to save information between frames
        # self.ctr = self.RoundCounter()
        # self.ctr = self.Counter()
        # self.dam = self.Damage()
        self.hey = 0
        
        # Storing records of actions between turns
        
        # number of times we've performed each event
        self.num_of = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0} # number of times we've done event
        # rounds since the previous run of each event
        self.since_previous = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0} # rounds since event
        # if Player is allowed to [attack, heal, scan] (no: 0 or yes: 1)
        self.toggle = {'start': 0, 'attack': 1, 'heal': 1, 'move': 1, 'scan': 1} # toggle to allow event
        # next position for movement
        self.next_pos = (0, 0)         
        

    def selectBehavior(self):
        # Replace the body of this method with your character's behavior
        
        def add_round(self):
            '''
            Count that one round has passed
            Also note that it has been one round since each Event.
            The Character calls this at the beginning of each turn.
            '''
            for event in self.since_previous:
                self.since_previous[event] += 1
                
        def reset_round(self, event):
            '''
            Reset the number of rounds since the latest performed Event.
            Placed before calling an event.
                        
            Args:
                event: a string (lowercase) for the Event that is called in the current turn
            '''
            self.num_of[event] += 1 # show that we've executed this event
            self.since_previous[event] = 0 # reset the rounds since previous execution of event
        
        
        # Calculate the damage that the Character can inflict on the scanned opponents
        
        def calc(self, scan_results, obj_pos):
            '''
            Calculate the damage that the Character can do to each opponent.
            
            Args:
                scan_results: info taken from object Character's ScanData
                obj_pos: the object Character's current position on the board
            '''
            
            id_pos = [] # initialize
            for target in scan_results: # for each scanned zombie
                
                target_id = target.getID() # get target's ID
                # print('zombie_health:', target_id.getHealth())
                # print('fam look it\'s zombie', target)
                target_pos = target.getPos() # get target's position
                target_pos_x, target_pos_y = target_pos
                obj_pos_x, obj_pos_y = obj_pos
                dist = math.hypot(obj_pos_x - target_pos_x, obj_pos_y - target_pos_y) # get distance from attacker to target
                scale_factor = 1.0 / math.exp(dist) # attack damage scale factor
                id_pos.append([target_id, scale_factor, target_pos]) # append the current target ID and damage scale factor to the collection
                print('We can see Zombie {}'.format(target_id))
                
            id_pos.sort(key = lambda x: x[1], reverse=True) # sort list from highest to lowest attack scale factor
            
            print(id_pos)
            
            return id_pos
        
        
        # Function to control Player movement
        def movement(self, map_view, obj_pos): # takes MapView and Pos objects from Player
            '''
            
            '''
            # print('MOVEMENT')
            
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
        
        def print_rounds(self):
            rows = [ '\nround {}',
                     '{} since attack, {} since heal, {} since move, {} since scan',
                     '{} attacks, {} heals, {} moves, {} scans' ]
        
            round_printout = '\n'.join(rows).format(
                       *self.since_previous.values(),
                        self.num_of['attack'], self.num_of['heal'], self.num_of['move'], self.num_of['scan'])
            
            print(round_printout)
            
            return
        
        
        # Count the current round number and rounds since each event
        # Game starts on round 1, with "0" rounds since each event
        add_round(self)
        print_rounds(self)
        
        # self.hey += 1
        # print('yo', self.hey)
        
        # Need to Scan for the first time
        # Otherwise the rest of the program, ScanEvent if we've just done a MoveEvent
        if (self.since_previous['start'] == 1) or (self.since_previous['move'] == 1):
            if self.getHealth() >= self.getInitHealth() * 0.1: # and if we're above 1/10 of original health
                # print('SCAN 53!')
                reset_round(self, 'scan') # note that we're doing a ScanEvent
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
        obj_id = self.getID()
        obj_pos = self.getPos()
        map_view = self.getMapView()
        
        # First priority event is healing if under a certain threshold
        # If health is less than 25%, then heal
        
        # Check if health is lower than the max damage the nearest zombie could inflict
        try:
            id_pos = calc(self, scan_results, obj_pos) # analyze scan data
            
            if obj_id == 0: # If we're the player
                opponent_max_health = 100 # show zombies' max health
            else: # If we're a zombie
                opponent_max_health = 1000 # show player's max health
            damage_threshold = id_pos[0][1]*opponent_max_health + self.getInitHealth() * 0.02
            # find max factor of damage that a zombie could inflict given the positions, excluding factor of health
            # also account for health decrement of each round
            
        # If there are no scan results or no zombies nearby, set the user-defined safe health threshold to 0.25 of original health
        except (IndexError): # if no zombies are in range as of last scan
            # print('no zombies in range')
            damage_threshold = self.getInitHealth() * 0.1
        
        print('Damage threshold:', damage_threshold)
        
        # If health is below a safe level, given zombie proximity, then HealEvent
        if (self.getHealth() <= damage_threshold) and (self.num_of['heal'] < 5):
            # If player health is below the safe health threshold and has healed fewer than 5 times so far
            reset_round(self, 'heal')
            print('HEAL 99!')
            return HealEvent(self)
        
        
        # Else (if health is above the safe level), either AttackEvent or MoveEvent based on to scan data
        else:
            if self.since_previous['scan'] <= 4: # If it's been at most 2 rounds since ScanEvent
                id_pos = calc(self, scan_results, obj_pos)
                if len(id_pos) >= 1: # and if there is at least one zombie in the scan data
                    
                    print('Damage we can do', self.getHealth()*id_pos[0][1])
                    
                    if self.getHealth()*id_pos[0][1] > 5: # If the damage we'll inflict is higher than the user-defined threshold
                        reset_round(self, 'attack') # note that we're doing an AttackEvent
                        # print('ATTACK 111!')
                        return AttackEvent(self, id_pos[0][1]) # then AttackEvent
                    else: # Else, if our damage is not high enough
                    # (but it's still been at most 2 rounds since last ScanEvent and we saw a zombie)
                        # Then we do a MoveEvent
                        x, y = obj_pos
                        x_off, y_off = movement(self, map_view, obj_pos)
                        reset_round(self, 'move') # note that we're doing a MoveEvent
                        # print('MOVE 123!')
                        return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
                        
                        # # Then we do an AttackEvent
                        # reset_round(self, 'attack') # note that we're doing a AttackEvent
                        # return AttackEvent(id_pos[0][1])
                        
                else: # If it's been at most 2 rounds since ScanEvent, but we see no zombie
                    x, y = obj_pos
                    x_off, y_off = movement(self, map_view, obj_pos)
                    reset_round(self, 'move') # note that we're doing a MoveEvent
                    # print('MOVE 123!')
                    return MoveEvent(self, x + x_off, y + y_off) # then MoveEvent
            
            # Else, if it's been more than 2 rounds since last ScanEvent (but we see no zombie), then ScanEvent
            else:
                reset_round(self, 'scan') # note that we're doing a ScanEvent
                # print('SCAN 129!')
                return ScanEvent(self) # then ScanEvent
            
            
        print('hahaha')
        
        
        

            

        
        
    
    ## Mind Palace
        
    # class Counter: # (obj_id):
        
    #     def __init__(self, num_of = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0}, # number of times we've done event
    #                        since_previous = {'start': 0, 'attack': 0, 'heal': 0, 'move': 0, 'scan': 0}, # rounds since event
    #                        toggle = [1, 1, 1, 1, 1], # toggle to allow event
    #                        next_pos = (0, 0)         # next position for movement
    #                        ):

        

            
                
        # def __str__(self):
        #     '''
        #     Print a message showing the round number, rounds since each event, and number runs of each Events
        #     '''            

        
    # class Damage:
        
    #     def __init__(self, scan_results=0, obj_pos=(0,0), map_view=(0,0)):
    #         self.scan_results = scan_results
    #         self.obj_pos = obj_pos
    #         self.map_view = map_view
            

        

            
            
            # Started an alternative movement controller here
            
            # x_off, y_off = 4, 4 # initialize offset in x- and y-coordinates
            # # start with invalid offsets to initialize while loop

            # # Check the bounds
            # # map_view = map_view # 
            # size_x, size_y = map_view.getMapSize() # get the dimensions of the map
            # x, y = obj_pos # get the player's current position
            
            # while abs(x_off) + abs(y_off) > 3: # while the sum of the offsets is invalid
            #     x_off = random.randint(-3, 3) # randomly select a valid x-offset
            #     y_off = random.randint(-3, 3) # randomly select a valid y-offset
            #     # print('hey:', abs(x_off)+abs(y_off))
            #     if (abs(x_off) + abs(y_off) <= 3) and (): # if the sum is valid
            #         continue # then leave the while loop and continue
    


            # if x + x_off < 0 or x + x_off >= size_x: # ff the 
            #     x_off = 0
            # if y + y_off < 0 or y + y_off >= size_y:
            #     y_off = 0
                
            # return (x_off, y_off)
        
        

        
        
                
        # def add_since_attack(self):
        #     self.round_counter += 1``
            
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
