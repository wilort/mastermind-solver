# Mastermind-solver
<img src=images/mastermind.png alt="My Example Image" width="250" height="200" class=center>

The purpose of this project is to showcase an algorithm that solves the mastermind board game
with linear programming.

# Game description
https://en.wikipedia.org/wiki/Mastermind_(board_game)

# Algorithm description
The game can be solved by setting up a linear optimization model with binary variables.

1. Make a randomized guess at the solution and get a set of key pegs.
2. Set up the optimization model.
3. If all key pegs are red go to step 7, else go to step 4
4. Convert the guess and key pegs into constraints and append them to the model.
5. Solve the optimization model. The solution represents a new guess.
6. Generate a new set of key pegs and go to step 2.
7. solution found!

# Linear optimization model

## General optimization model.
Let 
$B$ be the set of ball IDs and
$C$ be the set of possible ball colors.

Let $ x_{b,c} $ be a binary variable where $ b \in B, c \in C $.
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$
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
Hence, the following constraint is required.
$$
\sum_{c \in C} x_{bc} = 1, \text{for all } b \in B
$$

There can be a maximum of four ball colors in a guess.
Hence, the following constraint is required.
$$
\sum_{b \in B} \sum_{c \in C} x_{bc} \leq 4
$$

The variables x and y are related.
To force binary $y_c$ to be $1$ if and only if the color is used in any ball position
Hence, the following constraints are required.
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
\sum_{b,c \in G} x_{bc} = r
$$

Let $n$ be the number of none key pegs.
$$
\sum_{c \in G} 1 - y_c = n
$$

Let $w$ be the number of white colored key pegs.
$$
\sum_{b,c \in G} 1 - x_{bc} \geq w
$$


# TODO:
1. Allow duplicates
2. Could the binary variable $y$ be removed?
3. only create the optimization model once. not once per solve call

# experiments
x_00, x01, x02, x03
x_10, x11, x12, x13
x_20, x21, x22, x23
x_30, x31, x32, x33
x_40, x41, x42, x43
x_50, x51, x52, x53
x_60, x61, x62, x63
x_70, x71, x72, x73

solution is (1,2,3,4)
guess is (5,2,7,1)
then key pegs:
white, none, none, red

constraints:
white: 1-x0g + 1-x1g + 1-x2g + 1-x3g <= num white

#notes
this constraint will count the make sure that 
colors not in the solution are removed from the guess
and it will also remove the need of the variable y
constraint = pulp.lpSum(1 - x[b][c] for b in ball_ids for c in guess) == len(ball_ids) * hint.count(PegColors.NONE), ""


