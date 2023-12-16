Project Title

A threading module that logs information about the created threads, so that a 3D graph can be made.


Description

The threading_visualization works similarly to Python's threading module and calls the threading module. It has a few
additional arguements for the sake of readability. The information from threading_visualization is stored in a log
file, which can create a 3D visualization graph using index.html and vis_server.py.


Getting Started


Dependencies

    threading


Executing program

    python {{file}}
    python vis_server.py  
          Optional: Takes argument -f {file} if the log file is not the default Concurrency.log and -p {port}
    ex. python many_workers.py
    python vis_server.py -f Workers.log

Authors

Contributors names and contact info

Amanda Sparks
Luke Shannon

