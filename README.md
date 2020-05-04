# Assignment2: Local Search

## Search problem

We are helping **"Som Mobilitat"** guys to create a new service for their customers through a new platform. The final aim is to reduce CO_2 emissions and help save the planet. For this reason we want people to share their cars when commuting to work. The idea is that car owners register to our platform and some days they drive and take other owners to work and some other days they leave their cars at home and other drivers take them. We will organize shifts of drivers and passengers. That is, there will be days that a car owner will use her own car and will transport other people (registered in the platform) while other days she will leave her car at home and will commute to work with other owner's cars.

### Problem details

1. Assume there are *N* users registered in the platform and every month *M* users don't drive. Those driving users will adapt their route to collect and transport the non-driving users to their work places.
2. The city has 10 x 10 Km and streets form a chess where every block is a square of 100 x 100 m
3. Origins and ends of routes will correspond to a crossroad 
4. Distance between two points is measured using the *Manhattan distance*
5. Assume that every car has two free places to take passengers

### Problem solution
We want a solution for a given month. We want a plan where everybody gets to her workplace and cars have at most 3 people simultaneously (the driver and two passengers). Note that it may happen that we do not need all drivers of a month to drive. A solution should state the following:
* Who is driving during the current month
* The route of every driver indicating the people it takes (origin - destination) and in which order

### Solution criteria

* Car owners must get in time to work which limits the total length of the route they can do. Assume that they do not leave home earlier than 7h and they must be at work not later than 8h. Assume also that the average driving speed is 30 Km/h.
* Everybody must get to work on time (before 8h)
* None of the users that are in the *passenger* shift can drive. 
* There may be users that are in the *driver* shift that do not need to drive (will be passengers of other drivers)

### Scoring
See that we need to maximize the number of users that get to their destination while minimizing the total amount of driven distance
* Each non driving user earns the number of points equal to the distance between her origin and destination *distance(o,d)* + MAX_DISTANCE
* Each driving user with passengers earns the number of points equal to maximum distance she can drive minus the overhead distance she needs 
to drive in order to lift her passengers to their destination. That is MAX_DISTANCE - (actual driven distance - distance(o,d))
* Each driving user with no passengers earns zero points

## What you have
### Input files 
In directory 'i_o_files' you'll find text files that represent a set with a total of 9 problems for which you need to find the solution with the highest score (value): 
* 3 small problems with 5 drivers and 2, 7 and 15 users respectively
* 3 medium problems with 100 drivers and 50, 150 and 300 users respectively
* 3 big problems with 1000 drivers and 500, 1500 and 3000 users respectively

You'll find a file for each problem with the extension ".in". 
The format of the files is as follows:
* All values are separated with a space
* The first line is: N M D U where N and M is the city size (NxM), D the number of drivers and U the number of non driving users
* The rest of the D + U lines represent the users. The first D are drivers while the last U are users that cannot drive this month
* These lines are as follows: idx ox oy dx dy where idx is the user's identifier (from 0 to D+U-1) ox is the x of the origin, oy is the y of the origin
and dx, dy are the coordinates for the destination. Note that drivers have identifiers from 0 to D-1 while non driving users from D to D+U-1

For example input file small_5_2.in
```
100 100 5 2 
0 74 58 85 3 
1 78 59 27 81 
2 86 45 9 26 
3 57 39 56 18 
4 78 13 43 88 
5 30 95 94 58 
6 56 72 96 41 
```
### Output files
Output files represent a solution to the problem. Solutions should have the same name as the problem but with extenson ".out"
In directory 'i_o_files' there is an example of an output file "small_5_2.out" 
File format:
* Each line represents a driver's route. Each point in the route is a coordinate preceded by the user identifier: id x y
* A line begins with the driver's origin and ends with the driver's destination: id ox oy ... id dx dy
* In the middle you have the places where the driver should travel to pick and drop passengers. See that each passenger
appears twice, first for the origin and second for the destination
* Note that a driver can pick two passengers in a row and then drop one to pick another one to finally drop all and go to her destination. A driver
can have a maximum of 2 passengers at the same time.

Output file small_5_2.out (warning: this is not solution with high value!!!)
```
0 74 58 5 30 95 5 94 58 0 85 3
1 78 59 2 86 45 2 9 26 1 27 81
3 57 39 3 56 18
4 78 13 6 56 72 6 96 41 4 43 88
```
### Code
* read_in_file : functions to read the problem file
* read_answer_file.py : functions to read the answer file and to check whether is a "legal" solution
* answer_value.py : a function to calculate the value of a solution. A non-legal solution gets 0 points
* random_problem_generator.py : you don't need this
* utils.py (with two added functions for practica 2)
* search.py : the AIMA library with search algorithms

Feel free to use the above code. You are not obligated though

## What you should do
We are going to make a contest. The group that gets the highest overall value **WINS**.

You are going to solve this problem with local search and perform several experiments to compare different solutions and algorithms. 
You want to get the best scoring for the scenarios in the input files.

Once you have the best solution you could find for each problem, **create an output file** with the problem's name and with extension ".out". 
You should have 9 files. All files must be in the directory "i_o_files"

### Local search
You should solve this problem with local search algorithms since we are not interested in the path to the optimal solution. To do so you need to:
* Establish what is the search space and how to represent the different states (tentative solutions) so that algorithms are efficient in both memory space and computational time
* Think of several ways to initialize the search (generate the initial state). It will be useful to be able to (more or less) randomly generate initial states to run search algorithms several times and find the best solution. 
Note though that the initial state may not be a **solution** to the problem.
* Determine the transformation operators for a given state in order to *navigate* the solution space. Consider the branching factor and the ability of the operators in generating all possible solutions. 
* Think of value functions to evaluate tentative solutions and guide the search process to the optimal solution given the problem criteria. If you think of more than one possibility you may want to experimentally compare them.
* Run several times the Hill Climbing algorithm and experimentally determine its sensibility to the initial state. Compare the quality of the generated solutions 
* Try the Simulated Annealing algorithm. Determine the best parameters.

## Hand out
* The code:
  * Code used to use the searching algorithms
  * Code (probably scripts) used to run your set of experiments
* The results: an output file with the problem's name and with extension ".out". 
You should have 9 files. All files must be in the directory "i_o_files" 
* A report of your experiments
  * What are your operators to navigate the state space
  * Explain clever tricks you used
  * Is Hill-Climbing sensible to different initial solution
  * How you get best solutions (with Hill-Climbing or Simulated Annealing)
  
