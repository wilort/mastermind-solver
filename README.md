# mastermind-solver
<img src=images/mastermind.jpg alt="My Example Image" width="300" height="200">
The purpose of this project is to show how to solve the mastermind board game
by using linear programming.

# Game description rules
https://en.wikipedia.org/wiki/Mastermind_(board_game)

# Mathematical modelling
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

# Algorithm description
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.


Let 
$B$ be the set of ball IDs and
$C$ be the set of possible ball colors

Let $ x_{b,c} $ be a binary variable where:

$$
x_{b,c} =
\begin{cases}
1 & \text{if ball } b \text{ has color } c, \\
0 & \text{otherwise}.
\end{cases}
$$

Here:
- $ b \in B $, where $ B $ is the set of all ball IDs.
- $ c \in C $, where $ C $ is the set of all color IDs.

Let $ y_c $ be a binary variable where:

$$
y_c =
\begin{cases}
1 & \text{if color } c \text{ exists in the solution}, \\
0 & \text{otherwise}.
\end{cases}
$$

The constraints follow from the game rules

1. Each ball position has exactly one color
$$
\sum_{c \in C} x_{bc} = 1, \text{for all } b \in B
$$

2. Force binary $y_c$ to be $1$ if and only if the color is used in any ball position
$$
y_c \leq \sum_{b \in B} x_{bc}, \text{for all } c \in C
$$
$$
\sum_{b \in B} x_{bc} \leq 10000y_c, \text{for all } c \in C
$$


