# Spickey The Game - End of term project assignment

Platform game consisting in going through level studded with deadly traps as quick as possible. 

![Screenshot](http://eros.vlo.gda.pl/~spiroz/projekt/screen.png)


## Installation

The project is written in Python using pyglet library.
Requires Python interpreter, version 2.7.3. Under the 3.x branch, the game has not been tested.

### Linux (dystrybucje oparte na debianie)

1. Install Python 2.7.x branch
    
    	$ sudo apt-get install python
    
2. Install the pyglet library 
    
    	$ sudo apt-get install python-pyglet
    
3. [Download] and unpack the project
4. Give the launch permissions for the file game/main.py
    
    	$ chmod +x project_path/game/main.py

5. Run the application
		
		$ cd project_path/game/
		$ ./main.py
    
[Pobierz]: https://github.com/jmietki/Projekt/archive/master.zip

### Windows 

Windows is not supported. This is a Python so there's a chance that it will works.

## Known Issues

Apart from a number of problems associated with the early version, there may be a problem with a very low performance in windowed mode under Ubuntu Unity.
In this case, switch the game in full screen mode.. 

In the game/game.xml need to change the line
	
		<fullscreen value="false" />

to 

		<fullscreen value="true" />
