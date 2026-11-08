# Birdo — Flappy Bird AI

A Pytorch based Deep Reinforcement Learning environment and agent which is designed to learn to play Flappy Bird directly on the GPU.

## Features

- Custom Flappy Bird environment: built from scratch in Python for fast state vector extraction and simulation.
- Deep Q-Learning / PPO agent: learns the optimal time to jump based on the spatial vectors (distance to next pipe, gap height, velocity).
- GPU acceleration: Optimised for local training (e.g. NVIDIA RTX cards).

## Requirements

- Python 3.11+
- PyTorch
- NumPy
- Pygame (for visualization)


 **Run Training / Simulation:**
 Insert in command line (; + ctrl):
 Install pygame: py -3.11 -m pip install pygame
 Run: python main.py