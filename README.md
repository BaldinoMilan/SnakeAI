# SnakeAI

This project has been created for the purpose of a test, as a consequence the code has been written to make the program work in a low amount of time. So be carefull while reading this code and especially if you want to learn deep learning or reinforced learning.
If you're still determined to check the code, here are the few baselines...

# Files & Content
First of all, if you didn't noticed, this project is written in python and with many warnings I gave you in introduction, I have to do add one about the types safety and class data responsabilities that are relegated to the user (here my 'main.py' file).
For the structure of the code, there are two files of dependencies that are 'snake.py' and 'neural_network.py'. There are defined classes and functions that will all be used in the main file.
Finally, the only package that the project use is pygame and use the standards modules like sys and random. Now, here is a list of the files and their contents: 

- snake.py : this file implements all the related snake game features. All these features are combined in the 'Snake' class that contain a list of 'Body' class that represent a cube on the map, a 'Snack' class that is basicly the apple and give the possiblity of generating its position randomly and all the sprites needed for the rendering. Each class has a 'draw' method that use the pygame interface to render things to a surface that give the flexibility of drawing to a part of the window (as showed in the example).

- neural_network.py : this file contains all the deep learning related stuff, it will be hard to explain concisely and may be hard to understand if not explained. So in the following, I will describe each class and explain what it does:

  Neural: represents a neural, but is only use for the calculations, they're not explicitly refered in the network. The 'bias' is a constant added to the input and the 'function' is the index of the function in the 'activate_functions' list (its done so that it's easy to apply randomness to it).

  Node: it is the way that the network reference a neural. It contains the type of the neural (eather "input", "hidden" or "output") and its unique id. The id is the index of the neural in the list for inputs and outputs, and an id for hidden ones (its not correlated with the position in the list in this case).

  Connexion: represents a connexion between two neurals, the weight is a float that has no maximum or minimum, it is the multiplier of the input data. The input and output members are nodes that the network will interact with.

  Network: references tree list of respectivly input neurals, hidden neurals, and output neurals. The node work as described with this lists. The network contains the connexions between the neurals. Before assigning data in inputs neurals out member, you have to make sure to use the 'reset' method. After that you can process the output neurals you want by passing a node to them as parameter. Then the majority of methods are helper ones for the network and the mutation ones. 

  Population: it is the way to apply reinforcement learning (it's not well implemented for the save of time but work kind of fine). It basicly find the best network for a number of tries.

- main.py : Now the main file, there is nothing really special happening here. It's pretty straight forward so you should have now problem understand what's in there after understanding what's before.

# Performance
So the main issue in this project is that I didn't wanted to use much time into this because it was a test(I wrote it in a week end), and now I can see the result. At the moment, the program work. But it doesn't seems like the AI is really learning much or even regressing and that's quite depressing but for me and what I intended to do, it's fine. I know there are many ways to optimise, but I feel confortable with this and the main problem is that it's unusual to me to code in python and quite frustrating to write classes (especially data classes like neurals/nodes or connexions). In the end, test this at your risk.

