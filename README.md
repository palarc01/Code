The purpose of this code was to be able to extract the images of different rocks captured in a photo. Of course, the photo can contain any objects (not necessarily rocks) which can be extracted manually.
Before running the code, you need to have the following. Some means of runnning the code. I used the freely available visual studio code (https://code.visualstudio.com/). You also need to download and install a few python libraries shown in the short code below
"pip install opencv-python numpy matplotlib pillow"
You also need to have the photo saved in the same folder as the code. Please name the photo "rocks" and it should be a jpeg file.
To run the code do the following:-
a) Type "python tracerocks.py"
b) A screen will open up showing your image. On the upper top left you will see the options of selecting the outline of an object and then presing c to confirm
c) select the outline of an object by selecting points on the outside of the object using your mouse and then once done press c (Warning, DO NOT press c twice as the program will crash)
d) Once you press c, switch to your visual studio code. You will see that the code has saved the first object as a png file and called it rock_0.png
e) To select another object, press "enter" else type "done" to finish
Now you can take all these individual images and use another code (which is also available in my github folder and is called "positionrocks.py") to move, and rotate these images and arrange them as per your wish. Once done, you can export the output as a png file.
