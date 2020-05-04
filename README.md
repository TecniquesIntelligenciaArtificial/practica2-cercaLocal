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
* There may be users that are in the *driver* shift that do not need to drive

### Scoring
See that we need to maximize the number of users that get to their destination while minimizing the total amount of driven distance
* Each non driving user earns the number of points equal to the distance between her origin and destination *distance(o,d)* plus MAX_DISTANCE
* Each driving user earns the number of points equal to maximum distance she can drive minus the overhead distance she needs 
to drive in order to lift other users to their destination. That is MAX_DISTANCE - (actual driven distance - distance(o,d))
* Note that a driver user that finally doesn't drive wins the most points 

## What you have
In directory 'i_o_files' you'll find a set of problems for which you need to find the solution with the highest score (value). There is a small problem (5 drivers) 

## What you should do
You are going to solve this problem with local search and perform several experiments to compare different solutions and algorithms. You want to get the best scoring for the scenarios in the input files.

### Local search
You should solve this problem with local search algorithms since we are not interested in the path to the optimal solution. To do so you need to:
* Establish what is the search space and how to represent the different states (tentative solutions) so that algorithms are efficient in both memory space and computational time
* Think of several ways to initialize the search (generate the initial state). It will be useful to be able to (more or less) randomly generate initial states to run search algorithms several times and find the best solution. Note though that the initial state may not be a **solution** to the problem.
* Determine the transformation operators for a given state in order to *navigate* the solution space. Consider the branching factor and the ability of the operators in generating all possible solutions. 
* Think of value functions to evaluate tentative solutions and guide the search process to the optimal solution given the problem criteria. If you think of more than one possibility you may want to experimentally compare them.
* Run several times the Hill Climbing algorithm and experimentally determine its sensibility to the initial state. Compare the quality of the generated solutions 
* Try the Simulated Annealing algorithm. Determine the best parameters.


## Input file format

## Output file format

## Hand out
* The code:
  * Code used to use the searching algorithms
  * Code (probably scripts) used to run your set of experiments
* A report of your experiments
  * Is Hill-Climbing sensible to different initial solution
  * How you get best solutions (with Hill-Climbing or Simulated Annealing)
  
