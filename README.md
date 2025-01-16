# 3D Game Engine (3D Shooter with Raycasting)

## What I learned
- Raycasting: Implemented to simulate a 3D environment in a 2D space, rendering walls and objects based on the player's view.
- Texture mapping: Apply realistic textures to walls and objects, giving the environment a more immersive 3D appearance while maintaining performance in a 2D raycasted world.
- Rendering optimisations: Applied various techniques such as only rendering parts of the textures that are in frame. Render only objects that are in the players view cone.
- Collision Detection: Used to manage interactions between bullets, enemies, and objects in the environment.
- Game Physics: Applied basic principles of velocity, randomization, and object movement to control bullets and enemies.
- Sprite Handling and Animation: Managed the rendering of sprites, including dynamic elements like bullets and enemies.
- Sound Integration: Added immersive sound effects and background music using Pygame's sound module

## Overview
This game is a 3D-style shooter where the player navigates through a grid-based environment, shooting at enemies while avoiding obstacles. The game uses raycasting to simulate a 3D view and provide a first-person perspective. Players can pick up power-ups to increase health or accuracy and must fend off waves of enemies that shoot back. The goal is to defeat all enemies to win.


## Fun fact:
- There is a Minimap on the top-left indicating your direction and the position of enemies. The minimap contains all the information needed to create the players 3D point of view.

## Demo
🎥 Watch the program in action: [Demo Video](https://youtu.be/hmMD37zuFf0)
