# psi
playdate serial interface

## so what's this?
this is a tool i created to communicate with my playdate through the serial port, based on information documented by jaames and the rest of the playdate reverse engineering crew at [this repo](https://github.com/jaames/playdate-reverse-engineering/).

## requirements
- python 3.10 or newer
- pip
- pyserial

## quickstart
1. plug your playdate into your computer
2. open psi (`python psi.py`)
3. type `list` to see every open serial port
4. type the shown port to connect to your playdate

## commands
### while disconnected
`list` - lists all available serial ports

`connect <port>` - connects to the port specified. typing the port by itself will do the same as this command.

### while connected

`disconnect` - disconnects psi from your playdate

`script <script>` - executes a psi script. documentation below.

### works everywhere
quit, help

## psiscript
psiscript is psi's scripting language which you can use to automatically perform actions on your playdate.

nearly every line of psiscript is sent to your playdate as if you had typed the line in yourself. exceptions to this rule are documented below:

`wait <float/int>` - wait for the specified time

`*<number> <command>` - perform the command `number` amount of times

`~~ <comment>` - script comment

## other useful info
- psi automatically dumps all serial information retrieved from your playdate to `psi.log` in your current working directory.
- currently commands that cause playdate to constantly stream data are not supported (`buttons`, `stream`, etc.)
- i wrote this without any concern for code quality and there are probably quite a few bugs