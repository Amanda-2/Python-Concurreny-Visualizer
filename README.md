# Python Threading Concurrency Visualization

An threading module that logs information about the created threads, so that a 3D interactive graph can be made.


## Description

The threading_visualization works similarly to Python's threading module and calls the threading module. It has a few
additional arguements for the sake of readability. The information from threading_visualization is stored in a log
file, which can create a 3D visualization graph using index.html and vis_server.py.


## Getting Started


Dependencies (no installation necessary)

    threading
    three.js


## Executing program

    python {{file}}
    python vis_server.py  
          Optional: Takes argument -f {file} to load file and Concurrency.log and -p {port}
    ex. python many_workers.py
    python vis_server.py -f Workers.log

Please note that the file may be cached in the browser, so it may be necessary to disable the cache through inspect element to see live updates.

### Authors


Amanda Sparks

Luke Shannon

