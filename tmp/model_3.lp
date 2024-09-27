\* mastermind_problem *\
Minimize
Objective_Function: x_3_Colors.RED
Subject To
_C1: x_0_Colors.BLACK + x_0_Colors.BLUE + x_0_Colors.BROWN + x_0_Colors.GREEN
 + x_0_Colors.ORANGE + x_0_Colors.RED + x_0_Colors.WHITE + x_0_Colors.YELLOW
 = 1
_C10: x_0_Colors.GREEN + x_1_Colors.GREEN + x_2_Colors.GREEN
 + x_3_Colors.GREEN - 100000 y_Colors.GREEN <= 0
_C11: - x_0_Colors.YELLOW - x_1_Colors.YELLOW - x_2_Colors.YELLOW
 - x_3_Colors.YELLOW + y_Colors.YELLOW <= 0
_C12: x_0_Colors.YELLOW + x_1_Colors.YELLOW + x_2_Colors.YELLOW
 + x_3_Colors.YELLOW - 100000 y_Colors.YELLOW <= 0
_C13: - x_0_Colors.ORANGE - x_1_Colors.ORANGE - x_2_Colors.ORANGE
 - x_3_Colors.ORANGE + y_Colors.ORANGE <= 0
_C14: x_0_Colors.ORANGE + x_1_Colors.ORANGE + x_2_Colors.ORANGE
 + x_3_Colors.ORANGE - 100000 y_Colors.ORANGE <= 0
_C15: - x_0_Colors.BROWN - x_1_Colors.BROWN - x_2_Colors.BROWN
 - x_3_Colors.BROWN + y_Colors.BROWN <= 0
_C16: x_0_Colors.BROWN + x_1_Colors.BROWN + x_2_Colors.BROWN
 + x_3_Colors.BROWN - 100000 y_Colors.BROWN <= 0
_C17: - x_0_Colors.WHITE - x_1_Colors.WHITE - x_2_Colors.WHITE
 - x_3_Colors.WHITE + y_Colors.WHITE <= 0
_C18: x_0_Colors.WHITE + x_1_Colors.WHITE + x_2_Colors.WHITE
 + x_3_Colors.WHITE - 100000 y_Colors.WHITE <= 0
_C19: - x_0_Colors.BLACK - x_1_Colors.BLACK - x_2_Colors.BLACK
 - x_3_Colors.BLACK + y_Colors.BLACK <= 0
_C2: x_1_Colors.BLACK + x_1_Colors.BLUE + x_1_Colors.BROWN + x_1_Colors.GREEN
 + x_1_Colors.ORANGE + x_1_Colors.RED + x_1_Colors.WHITE + x_1_Colors.YELLOW
 = 1
_C20: x_0_Colors.BLACK + x_1_Colors.BLACK + x_2_Colors.BLACK
 + x_3_Colors.BLACK - 100000 y_Colors.BLACK <= 0
_C21: - y_Colors.BLACK - y_Colors.GREEN - y_Colors.RED - y_Colors.WHITE = -2
_C22: - x_0_Colors.WHITE - x_1_Colors.GREEN - x_2_Colors.RED
 - x_3_Colors.BLACK = -2
_C23: - y_Colors.BLACK - y_Colors.BROWN - y_Colors.ORANGE - y_Colors.WHITE = 0
_C24: - x_0_Colors.GREEN - x_1_Colors.GREEN - x_2_Colors.RED
 - x_3_Colors.GREEN = 0
_C3: x_2_Colors.BLACK + x_2_Colors.BLUE + x_2_Colors.BROWN + x_2_Colors.GREEN
 + x_2_Colors.ORANGE + x_2_Colors.RED + x_2_Colors.WHITE + x_2_Colors.YELLOW
 = 1
_C4: x_3_Colors.BLACK + x_3_Colors.BLUE + x_3_Colors.BROWN + x_3_Colors.GREEN
 + x_3_Colors.ORANGE + x_3_Colors.RED + x_3_Colors.WHITE + x_3_Colors.YELLOW
 = 1
_C5: - x_0_Colors.RED - x_1_Colors.RED - x_2_Colors.RED - x_3_Colors.RED
 + y_Colors.RED <= 0
_C6: x_0_Colors.RED + x_1_Colors.RED + x_2_Colors.RED + x_3_Colors.RED
 - 100000 y_Colors.RED <= 0
_C7: - x_0_Colors.BLUE - x_1_Colors.BLUE - x_2_Colors.BLUE - x_3_Colors.BLUE
 + y_Colors.BLUE <= 0
_C8: x_0_Colors.BLUE + x_1_Colors.BLUE + x_2_Colors.BLUE + x_3_Colors.BLUE
 - 100000 y_Colors.BLUE <= 0
_C9: - x_0_Colors.GREEN - x_1_Colors.GREEN - x_2_Colors.GREEN
 - x_3_Colors.GREEN + y_Colors.GREEN <= 0
Binaries
x_0_Colors.BLACK
x_0_Colors.BLUE
x_0_Colors.BROWN
x_0_Colors.GREEN
x_0_Colors.ORANGE
x_0_Colors.RED
x_0_Colors.WHITE
x_0_Colors.YELLOW
x_1_Colors.BLACK
x_1_Colors.BLUE
x_1_Colors.BROWN
x_1_Colors.GREEN
x_1_Colors.ORANGE
x_1_Colors.RED
x_1_Colors.WHITE
x_1_Colors.YELLOW
x_2_Colors.BLACK
x_2_Colors.BLUE
x_2_Colors.BROWN
x_2_Colors.GREEN
x_2_Colors.ORANGE
x_2_Colors.RED
x_2_Colors.WHITE
x_2_Colors.YELLOW
x_3_Colors.BLACK
x_3_Colors.BLUE
x_3_Colors.BROWN
x_3_Colors.GREEN
x_3_Colors.ORANGE
x_3_Colors.RED
x_3_Colors.WHITE
x_3_Colors.YELLOW
y_Colors.BLACK
y_Colors.BLUE
y_Colors.BROWN
y_Colors.GREEN
y_Colors.ORANGE
y_Colors.RED
y_Colors.WHITE
y_Colors.YELLOW
End
