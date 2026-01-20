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