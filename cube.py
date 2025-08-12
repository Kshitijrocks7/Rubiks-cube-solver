# cube.py

from vpython import *
import numpy as np
import random
from solve_rubiccs_cube import *

class Rubic_Cube():
    def __init__(self):
        self.running = True
        self.tiles = []
        self.dA = np.pi / 40
        
        # --- UI & Scene Enhancement ---
        scene.title = "Interactive Rubik's Cube"
        scene.width = 1000
        scene.height = 700
        scene.background = color.gray(0.2) # Dark background
        scene.lights = [] # Remove default lights
        distant_light(direction=vector(0.2, 0.5, 1), color=color.gray(0.8))
        distant_light(direction=vector(-0.8, -0.3, -0.5), color=color.gray(0.4))
        
        # Center sphere - smaller and shinier for a metallic look
        sphere(pos=vector(0,0,0), size=vector(2.9,2.9,2.9), color=color.gray(0.1), shininess=0.8)
        
        tile_pos = [[vector(-1, 1, 1.5),vector(0, 1, 1.5),vector(1, 1, 1.5),           #front
                     vector(-1, 0, 1.5),vector(0, 0, 1.5),vector(1, 0, 1.5),
                     vector(-1, -1, 1.5),vector(0, -1, 1.5),vector(1, -1, 1.5), ],
                    [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),         # right
                     vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
                     vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
                    [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),       # back
                     vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
                     vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),          # left
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),          # top
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
                    [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),          # bottom
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
                    ]
        colors = [vector(1,0,0),vector(1,1,0),vector(1,0.5,0),vector(1,1,1),vector(0,0,1),vector(0,1,0)]
        angle = [(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(np.pi/2,vector(1,0,0)),(np.pi/2,vector(1,0,0))]
        
        for rank,side in enumerate(tile_pos):
            for vec in side:
                tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[rank])
                tile.rotate(angle = angle[rank][0],axis=angle[rank][1])
                self.tiles.append(tile)

        self.positions = {'front':[],'right':[],'back':[],'left':[],'top':[],'bottom':[]}
        self.rotate = [None,0,0]
        self.moves = []
        self.solution_text = wtext(text='') # For displaying solution in UI

    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4: self.positions['front'].append(tile)
            if tile.pos.x > 0.4: self.positions['right'].append(tile)
            if tile.pos.z < -0.4: self.positions['back'].append(tile)
            if tile.pos.x < -0.4: self.positions['left'].append(tile)
            if tile.pos.y > 0.4: self.positions['top'].append(tile)
            if tile.pos.y < -0.4: self.positions['bottom'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])

    def animations(self):
        if self.rotate[0] is None: return
        
        rotations = {
            'front_counter': {'axis': vector(0,0,1), 'pieces': self.positions['front'], 'angle_mult': 1},
            'right_counter': {'axis': vector(1,0,0), 'pieces': self.positions['right'], 'angle_mult': 1},
            'back_counter': {'axis': vector(0,0,-1), 'pieces': self.positions['back'], 'angle_mult': 1},
            'left_counter': {'axis': vector(-1,0,0), 'pieces': self.positions['left'], 'angle_mult': 1},
            'top_counter': {'axis': vector(0,1,0), 'pieces': self.positions['top'], 'angle_mult': 1},
            'bottom_counter': {'axis': vector(0,-1,0), 'pieces': self.positions['bottom'], 'angle_mult': 1},
            'front_clock': {'axis': vector(0,0,1), 'pieces': self.positions['front'], 'angle_mult': -1},
            'right_clock': {'axis': vector(1,0,0), 'pieces': self.positions['right'], 'angle_mult': -1},
            'back_clock': {'axis': vector(0,0,-1), 'pieces': self.positions['back'], 'angle_mult': -1},
            'left_clock': {'axis': vector(-1,0,0), 'pieces': self.positions['left'], 'angle_mult': -1},
            'top_clock': {'axis': vector(0,1,0), 'pieces': self.positions['top'], 'angle_mult': -1},
            'bottom_clock': {'axis': vector(0,-1,0), 'pieces': self.positions['bottom'], 'angle_mult': -1},
        }

        current_move = rotations.get(self.rotate[0])
        if current_move:
            for tile in current_move['pieces']:
                tile.rotate(angle=(self.dA * current_move['angle_mult']), axis=current_move['axis'], origin=vector(0,0,0))
            self.rotate[1] += self.dA

        if self.rotate[1] + self.dA / 2 > self.rotate[2] and self.rotate[1] - self.dA / 2 < self.rotate[2]:
            self.rotate = [None, 0, 0]
            self.reset_positions()
            
    def set_rotation(self, move_name):
        if self.rotate[0] is None:
            self.rotate = [move_name, 0, np.pi / 2]

    def rotate_front_counter(self): self.set_rotation('front_counter')
    def rotate_right_counter(self): self.set_rotation('right_counter')
    def rotate_back_counter(self): self.set_rotation('back_counter')
    def rotate_left_counter(self): self.set_rotation('left_counter')
    def rotate_top_counter(self): self.set_rotation('top_counter')
    def rotate_bottom_counter(self): self.set_rotation('bottom_counter')
    def rotate_front_clock(self): self.set_rotation('front_clock')
    def rotate_right_clock(self): self.set_rotation('right_clock')
    def rotate_back_clock(self): self.set_rotation('back_clock')
    def rotate_left_clock(self): self.set_rotation('left_clock')
    def rotate_top_clock(self): self.set_rotation('top_clock')
    def rotate_bottom_clock(self): self.set_rotation('bottom_clock')

    def move(self):
        if self.rotate[0] is not None or not self.moves:
            return
            
        move_map = {
            "F": self.rotate_front_clock, "R": self.rotate_right_clock,
            "B": self.rotate_back_clock, "L": self.rotate_left_clock,
            "U": self.rotate_top_clock, "D": self.rotate_bottom_clock,
            "F'": self.rotate_front_counter, "R'": self.rotate_right_counter,
            "B'": self.rotate_back_counter, "L'": self.rotate_left_counter,
            "U'": self.rotate_top_counter, "D'": self.rotate_bottom_counter,
        }
        
        move_func = move_map.get(self.moves.pop(0))
        if move_func:
            move_func()
            
    def scramble(self):
        self.solution_text.text = "" # Clear previous solution
        possible_moves = ["F","R","B","L","U","D","F'","R'","B'","L'","U'","D'"]
        for _ in range(25):
            self.moves.append(random.choice(possible_moves))
            
    def solution(self):
        solution_string = solve(self.tiles)
        # Display the solution in the UI instead of printing to console
        self.solution_text.text = f"<b>Solution Path:</b>\n{solution_string}"
        
    def solve(self):
        self.solution_text.text = "" # Clear previous solution
        values = solve(self.tiles)
        values = list(values.split(" "))
        for value in values:
            if value.endswith('2'):
                move = value[:-1]
                self.moves.append(move)
                self.moves.append(move)
            else:
                self.moves.append(value)
                
    def control(self):
        scene.append_to_caption("<b>Rubik's Cube Simulator</b>\n\n")
        
        # --- Manual Controls Section ---
        scene.append_to_caption("<b>Manual Controls (Clockwise / Counter-Clockwise)</b>\n")
        
        # Row 1: Front and Back
        button(bind=self.rotate_front_clock, text='F')
        button(bind=self.rotate_front_counter,text="F'")
        scene.append_to_caption("  |  ")
        button(bind=self.rotate_back_clock, text='B')
        button(bind=self.rotate_back_counter, text="B'")
        scene.append_to_caption("\n")

        # Row 2: Right and Left
        button(bind=self.rotate_right_clock, text='R')
        button(bind=self.rotate_right_counter, text="R'")
        scene.append_to_caption("  |  ")
        button(bind=self.rotate_left_clock, text='L')
        button(bind=self.rotate_left_counter, text="L'")
        scene.append_to_caption("\n")

        # Row 3: Top (Up) and Bottom (Down)
        button(bind=self.rotate_top_clock, text='U')
        button(bind=self.rotate_top_counter, text="U'")
        scene.append_to_caption("  |  ")
        button(bind=self.rotate_bottom_clock, text='D')
        button(bind=self.rotate_bottom_counter, text="D'")
        scene.append_to_caption("\n\n")
        
        # --- Actions Section ---
        scene.append_to_caption("<b>Actions</b>\n")
        button(bind=self.scramble, text='Scramble Cube')
        button(bind=self.solution, text='Show Solution')
        button(bind=self.solve, text='Solve It!')
        scene.append_to_caption("\n\n")
        
        # --- Solution Display Area ---
        self.solution_text = wtext(text='') # Text object for the solution string

    def update(self):
        rate(60)
        self.animations()
        self.move()
        
    def start(self):
        self.reset_positions()
        self.control()
        while self.running:
            self.update()