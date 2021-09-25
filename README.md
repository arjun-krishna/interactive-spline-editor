# Interactive Spline Editor

![Application Layout](demo/app-layout.png?raw=true "Application Layout")


### Launching the Application
```
> cd src
> # pip install -r requirements.txt
> python app.py
```

### Controls

There are three modes to the editor:
1. Insert mode: In this mode, clicking anywhere on the drawable grid inserts a control point
2. Delete mode: In this mode, clicking near a control point deletes it
3. Animation mode: In this mode, we show an animated movement of a sphere along the specified interpolation trajectory

<ins>Keyboard Shortcuts</ins>

|action|key|
|---|---|
|Quit| q|
|Toggle insert mode| i|
|Toggle delete mode| x|
|Toggle animation mode| Space|
|Exit from all modes| Esc|
|Clear all data (control points, modes) | d|
|speed up animation| RIGHT|
|slow down animation| LEFT|
|loop animation| o|
|toggle grids and axis| h|
|toggle control points and interpolating curve | SHIFT-h|

<ins>Selecting interpolater</ins>
|interpolater|key|
|---|---|
|Linear|l|
|Bezier|z|
|B-splines|b|
|Catmull-Rom splines|r|
|C2-interpolating|c|

_Note_: Currently interpolater selection does not have GUI clickable button.

<ins>GUI supported controls</ins>
1. Insert/Delete mode toggle supported
2. Animation start/stop, speed control, loop button
3. Movement of control points by holding down on LEFT-mouse button.
4. Movement of control points supported during animation of sphere on the interpolated path.


*Checkout the Demo!* 

https://user-images.githubusercontent.com/12149046/134757415-05e38f49-b86a-4e93-ac72-873349681449.mp4

PS: Code is not optimal in any way! It was hacked together in about 4-5 hours.
