# PySlice

## Basic requirements:
1. Create a basic instruction set that lets users add and remove cubes/cubesets
2. Save the users' design in a file
3. Develop a slicer that converts the design file to G-code

Refer to the [Project Overview](https://docs.google.com/document/d/1ZvQXrVY3l2oUyY_0G_QL7AB2-BRr6pGMgmdDLN2GCs8/edit?usp=sharin)
for more detailed information.

Refer to the [repository](https://github.com/RohanK9/PySlice) to view the code.

## PySlice Installation and Setup (in WSL environment)
Run the following commands in a WSL terminal.
```
python3 setup.py sdist bdist_wheel
python3 setup.py develop
```

If on a Windows OS, ensure that X11 Server for Windows (VcXsrv) is installed and running. If installed 
but not running, run the XLaunch app from the start menu. 

## How to Run the App
```
pyslice
```

## Features
### Commands
A set of commands are provided to interact with the application. x, y, and z represents the 
coordinate and they must be of integer values.

#### 1. Add a Unit Cube 
The x, y, z position must be specified and must be of type integer.
```
addcube x y z
```
For example, the below command will add a unit cube with default color at position (1,2,3). The color
of the cube will be the default color if the user did not pick a different color.
```
addcube 1 2 3 
```

#### 2. Delete a Unit Cube
The x, y, z position must be specified when deleting a cube. If there is not a cube at this position,
a warning will be given.
```
delcube x y z
```

#### 3. Add a Cube Set 
The x, y, z position of the starting cube must be specified and must be of type integer.
Dimensions sx, sy, sz are also integers that represent the dimensions of the cube set. The top corner 
cube diagonally opposite of the starting cube will have position x + sx, y + sy, z + sz.

```
addcubeset x y z sx sy sz
```

#### 4. Delete a Cube Set 
Requires the same arguments as addcubeset.

```
delcubeset x y z sx sy sz
```

#### 5. Save model
Save the currently open file by passing in the filename (without the .slice extension) and optionally
the path to the directory where the file is located.

```
save filename [path_to_directory]
```
For example, the first command below command will save file "testfile1.slice" to the current working 
directory. The second command will save testfile2.slice to a given directory.
```
save testfile1
save testfile2 d:\Users\my_name\Documents\Projects
```

#### 6. Load
Loading a previously saved model with file extension .slice requires the path (relative or absolute) to 
the file. An optional second argument 'f' or 'false can be given to not clear the currently loaded model. 
This can be useful if you want to combine different models.

```
load pathtofile [f]
```

#### 7. Clear
Will clear current model from the display.

```
clear
```

#### 8. Add Model
Creates a copy of a model file at a specified position.

```
addmodel filename x y z
```

#### 9. Subtract Model
Subtracts a designfile from the current design at a specified position.
Could be used as a configurable eraser.

```
submodel filename x y z
```

#### 10. Slice
Generates a .gcode file for the specified designfile.
The gcode file can be used to print the model on a 3D printer.

```
slice filename
```

<br>

### Set Cube Color
A color picker is added to make it easy for users to pick a color that they want to use. The default
color is blue. The alpha value (transparency) can only be set on certain systems.

<br>

### Cycle through Commands Using Up/Down Arrow key
When pressing up/down arrow key with the command input box selected, one can cycle through
the past commands that were typed into it. The up key makes it go back to older commands and
the down key makes it go forward to newer commands.

<br>

### Use Tab to Autocomplete Commands
Pressing tab when typing a command will find the longest common prefix of possible commands based
on what is currently typed.

For example, typing
```
add [tab press]
```
will result in "addcube".

<br>

### Error Checking
All illegal inputs will cause the error to be displayed in a pop up window. 
