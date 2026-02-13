# Robotic Arm Exhibit

An **interactive touchscreen-based puzzle game** designed for a **museum exposition about robotics and automation** with runtime sequence validation, safety checks, and recovery handling..
Visitors use drag-and-drop command blocks to **program an industrial robotic arm** and watch it execute their instructions.

The system connects a Python Tkinter-based UI to an industrial robot (BORUNTE Brtirus 1820A) via GPIO signals and RoboDK-generated motion programs.

##  Overview

This application allows a user to construct a sequence of robot actions and execute it on real hardware.
Before and during execution, the sequence is validated to prevent unsafe motion, detect logical errors, and assess result quality.

The robot itself does not manage execution order.
All sequencing, validation, and error handling are performed in the application layer.

## Requirements
***Hardware:***

* Raspberry Pi (GPIO control)

* BORUNTE industrial robot

* Robot controller configured for external digital inputs

***Software:***

* Python 3.10+

* RoboDK

Python dependancies:
```
sudo apt update
sudo apt install python3-pil python3-pil.imagetk
sudo apt install python3-opencv
sudo apt install python3-cairosvg
```

## Key Features
### Hardware-Aware Execution

* Every robot action includes hardware-tuned delays

* A dedicated robot output pin signals when an action is finished

* Prevents command stacking and timing drift

* Designed to work even when robot feedback is temporarily unavailable

### Structured Error System

The executor classifies outcomes into three distinct levels:

* __Hard errors__  -  unsafe or invalid actions (wrong position, illegal shake, hardware failure).
Execution stops immediately and the robot recovers safely.

* __Soft errors__ - execution completes, but quality is reduced
(e.g. weak shake, scanning without shaking).

* __Incomplete tasks__ - the sequence ran, but required stations were skipped.
This state overrides soft errors and prompts the user to acknowledge before the robot homes.

### Gamified Task Logic

Rather than free-form motion:

* The robot must visit required stations

* Certain actions only make sense in specific zones

* Users are subtly guided toward correct behavior through feedback instead of hard restrictions

This makes the system suitable for training, demonstrations, and evaluation scenarios.