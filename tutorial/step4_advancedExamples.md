# ThreadPlotter 
Thread plotter package is a toolkit that can
1. store and process trajectories (paths), which are list of points that are connected in certain order. 
    2. ThreadPlotter only accept points and connect them with straight lines. If you have a curve (e.g., cubic bezier), you will need to approximate them with straight lines. 
2. write svg and axidraw-controlling python scripts.
    1. We utilize [the axidraw api](https://axidraw.com/doc/py_api/#functions-interactive) to get access to fundamental controls such as pen_up and pen_down. 
    If you use a different plotter, the python scripts would not work on your plotter. However, you can use the same strategy we took and modify the library to author in your own syntax.   

##install 
We would recommend that you clone this repository so you have access to all of the sample projects. It also makes it easier for you to modify the threadPlotter, especially if you want to use it on plotters other than Axidraw. 

Here's a list of dependencies that you might need to install. 
```angular2html
1. 
```