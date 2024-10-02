# mastermind-solver
<img src=images/mastermind.jpg alt="My Example Image" width="300" height="200" class=center>

The purpose of this project is to show how to solve the mastermind board game
by using linear programming.

# Game description rules
https://en.wikipedia.org/wiki/Mastermind_(board_game)

# Algorithm description
The game can be solved by setting up a linear optimization model with binary variables.

1. Make a randomized guess at the solution and get a set of key pegs.
2. Set up the optimization model.
3. If all key pegs are red go to step 8, else go to step 3
4. Convert the guess and key pegs into constraints and append them to the model.
5. Solve the optimization model. The solution represent the new guess.
6. Generate a new set of key pegs.
7. Go to step 2.
8. solution found!

# Linear optimization model

## General optimization model.
Let 
$B$ be the set of ball IDs and
$C$ be the set of possible ball colors

Let $ x_{b,c} $ be a binary variable where $ b \in B, c \in C $.
$$
x_{b,c} =
\begin{cases}
1 & \text{if ball } b \text{ has color } c, \\
0 & \text{otherwise}.
\end{cases}
$$

Let $ y_c $ be a binary variable where:
$$
y_c =
\begin{cases}
1 & \text{if color } c \text{ exists in the solution}, \\
0 & \text{otherwise}.
\end{cases}
$$

Each ball position has exactly one color.
Thus the following constraint is required.
$$
\sum_{c \in C} x_{bc} = 1, \text{for all } b \in B
$$

There can be a maximum of four ball colors in a guess.
Thus, the following constraint is required.
$$
\sum_{b \in B} \sum_{c \in C} x_{bc} \leq 4
$$

The variables x and y are related.
To force binary $y_c$ to be $1$ if and only if the color is used in any ball position
Then the following constraints are required.
$$
y_c \leq \sum_{b \in B} x_{bc}, \text{for all } c \in C
$$
$$
\sum_{b \in B} x_{bc} \leq 10000y_c, \text{for all } c \in C
$$


## Constraints from guess and key pegs

Let $G$ be the guess.

Let $r$ be the number of red colored key pegs.
$$
\sum_{b,c \in G} \sum_{x_{bc}} x_{bc} = r
$$

Let $n$ be the number of none key pegs.
$$
\sum_{c \in G} \sum_{1 - y_{c}} = n
$$

Let $w$ be the number of white colored key pegs.
$$
\sum_{b,c \in G} \sum_{1 - x_{bc}} \geq w
$$
