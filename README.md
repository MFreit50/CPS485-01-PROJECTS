# CPS485 01 PROJECTS

A Python-based framework for **step-by-step visualization of neural network training**, designed with extensibility in mind for **multiple algorithms and data structures**.  
This project demonstrates a modular architecture separating **producers (algorithms)**, **event tracing**, **transport**, and **consumers (visualizations)**.  

## Features

- **Step-by-step execution tracing** for neural networks
- **Event-driven architecture**: each significant computation emits events that are recorded in a trace
- **Framework-ready design** for future support of multiple algorithms (sorting, graph traversal, state machines)
- **MVP demo**: simple feed-forward network with forward/backward pass and weight updates
- **Flexible transport layer**: in-memory, file-based, or streaming to frontend
- **Replay & visualization-ready**: frontend can reconstruct state from emitted events

### Key Concepts

- **Event**: Immutable object representing a meaningful algorithmic step  
- **Trace**: Collection of ordered events with logical timestamps  
- **Producer**: Algorithm that emits events (e.g., a neural network layer)  
- **Consumer**: Visualizer or analysis tool that interprets events  
- **Transport**: Mechanism for moving events from producers to consumers  

