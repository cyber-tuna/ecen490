# Note

This folder was used for vision development. You can use an IDE if you prefer (such as Eclipse), but we just used Sublime Text as an editor and g++ on the terminal for compiling and running the code.

To run this code

1. Install dependencies
 * ZeroMQ
  ```
  # This install was a little tricky, so Google errors you get as you install
  # We were successful with the following commands
  git clone --depth=1 https://github.com/imatix/zguide.git
  cd zguide/examples
  make && ./build && ./build all
  git clone https://github.com/zeromq/libzmq
  ./autogen.sh && ./configure && make -j 4
  cd usr/lib/local/include
  git clone https://github.com/zeromq/cppzmq.git\
  sudo nano zmq.hpp
  ``` 
 * OpenCV
2. `rm imagefifo && mkfifo imagefifo`
3. Open src/ComputerVision.cpp
4. Change the two instances of "http://192.168.1.78:8080/stream?topic=/image&dummy=param.mjpg" to the correct URI for the camera you are using
5. Compile with ```g++ -o output src/*.cpp -lpthread `pkg-config opencv --cflags --libs` -lzmq```
6. Run with `./output`
```
