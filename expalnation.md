## How the game woks
A quick explanation of how the fractals are generated.

# The base case
Given a set of vertices the fractal is created by iteratively creating a sequence of points,
starting with a random starting point (which is chosen by default, it's the grey point), in which each point in the sequence is the midpoint between the 
previous point and one of the vertices of the polygon; the vertex is chosen at random in each iteration.
Repeating this iterative process a large number of times, selecting the vertex at random on each iteration, will often (but not always) produce a fractal shape.

# The parameter alpha
Instead of chosing the midpoint we can chose a generic fraction alpha of the distance between the previous point and the randomly chosen vertex. 
In the program only positive values are accepted for alpha (it can be bigger than 1).

# The vertex excluder
The idea of the vertex excluder is easy but it's hard to explain, i'll try my best.

At each iteration we can decide to exclude some vertices from the set of the vertices that can be chosen, based on which vertices were chosen in the previous iterations.
To do it we use the circle of circles that is in the setting window (we call it "the vertex excluder"). In it, at each iteration, the top circle
(the one with a thin circle around it) represents the vertex chosen in the previous iteration, while the other circles represent the other vertices relative to it.
If a circle is selected (is red) then, at each iteration, the corresponding vertex cannot be chosen. 
This happens if Memory=1; if Memory=2 the vertex is excluded only if the vertex chosen in the previous iteration was chosen twice in a row.
