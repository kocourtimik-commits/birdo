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

## Installation & Setup

1. **Clone the repository:**
   git clone https://github.com/kocourtimik-commits/birdo.git
   cd birdo

2. **Install dependencies:**
   pip install -r requirements.txt

3. **Run Training / Simulation:**
   python main.py