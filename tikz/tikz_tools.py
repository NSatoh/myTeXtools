#!python
# -*- coding: utf-8 -*-

from tikz_line-fill import tikz_fill_lines

# indentation setting
tikz_indent = "  "

# unit vectors
unit_length = 0.3
unit_x = "ex"
unit_y = "ey"

# set global unit_length
def set_unit_length(ul=unit_length):
    global unit_length
    unit_length = ul

# set global unit_x, unit_y
def set_unit_vector_name(x_name, y_name):
    global unit_x
    global unit_y
    unit_x = x_name
    unit_y = y_name

# print unit vector setting
def unit_vectors():
    output = ""
    output += tikz_indent + r"\coordinate ({unit_x}) at ({ul}, 0);" + "\n"
    output += tikz_indent + r"\coordinate ({unit_y}) at (0, {ul});"
    print(output.format(ul=unit_length, unit_x=unit_x, unit_y=unit_y))


#-- functions for \draw -----------------------------------------------------------------------------

# print parabola y = ax^2 + bx + c, draw x in [start_x, terminal_x]
def parabola_abc(a, b, c, start_x, terminal_x):
    def f(x):
        return a*x*x + b*x + c
    bend_x = -b/(2*a)
    output =  tikz_indent + r"\draw "
    output += r"(${start_x}*({unit_x}){sgn_start_y}{start_y}*({unit_y})$) "
    output += r"parabola bend "
    output += r"(${bend_x}*({unit_x}){sgn_bend_y}{bend_y}*({unit_y})$) "
    output += r"(${terminal_x}*({unit_x}){sgn_terminal_y}{terminal_y}*({unit_y})$);"
    print(output.format(start_x = start_x,       start_y = f(start_x),
                         bend_x  = bend_x,        bend_y  = f(bend_x),
                         terminal_x = terminal_x, terminal_y = f(terminal_x),
                         unit_x=unit_x, unit_y=unit_y,
                         sgn_start_y = sgn(f(start_x)),
                         sgn_bend_y = sgn(f(bend_x)),
                         sgn_terminal_y = sgn(f(terminal_x)))
    )

# parabola y = a(x-p)^2 + q, draw x in [start_x, terminal_x]
def parabola_apq(a, p, q, start_x, terminal_x):
    def f(x):
        return a*(x*x - p) + q
    bend_x = p
    output =  tikz_indent + r"\draw "
    output += r"(${start_x}*({unit_x}){sgn_start_y}{start_y}*({unit_y})$) "
    output += r"parabola bend "
    output += r"(${bend_x}*({unit_x}){sgn_bend_y}{bend_y}*({unit_y})$) "
    output += r"(${terminal_x}*({unit_x}){sgn_terminal_y}{terminal_y}*({unit_y})$);"
    print(output.format(start_x = start_x,       start_y = f(start_x),
                         bend_x  = bend_x,        bend_y  = f(bend_x),
                         terminal_x = terminal_x, terminal_y = f(terminal_x),
                         unit_x=unit_x, unit_y=unit_y,
                         sgn_start_y = sgn(f(start_x)),
                         sgn_bend_y = sgn(f(bend_x)),
                         sgn_terminal_y = sgn(f(terminal_x)))
    )

# x --> signature of x
def sgn(x):
    if x < 0:
        return "" # not return "-" because it is included in x.
    else:
        return "+"


# y --> tapple(x where y = ax^2+bx+c)
def abcy_to_x(a,b,c,y):
    x1 = (-b - (b*b-4*a*(c-y))**0.5)/(2*a)
    x2 = (-b + (b*b-4*a*(c-y))**0.5)/(2*a)
    return (x1,x2)


# print coordinate axis (arrow setting imitated for Tpic)
def axis(x1,x2,y1,y2):
    output  = tikz_indent + r"{p} axis" + "\n"
    output += tikz_indent + r"\draw [thick, arrows = {{{p}" + "\n"
    output += tikz_indent + r"  -Stealth[round, length=6.45pt, width=3.9pt, inset=1.35pt]{p}" + "\n"
    output += tikz_indent + r"}}] ({x1},0) -- ({x2},0) node(xAxis)[right] {{$x$}};" + "\n"
    output += tikz_indent + r"\draw [thick, arrows = {{{p}" + "\n"
    output += tikz_indent + r"  -Stealth[round, length=6.45pt, width=3.9pt, inset=1.35pt]{p}" + "\n"
    output += tikz_indent + r"}}] (0,{y1}) -- (0,{y2}) node(yAxis)[above] {{$y$}};" + "\n"
    output += tikz_indent + r"\node at (0,0) [below left] {{O}};"
    print(output.format(x1=x1, x2=x2, y1=y1, y2=y2, p="%"))


# print lattice (virtual coordinate x1 to x2, y1 to y2, expected int)
def lattice(x1,x2,y1,y2, axis_ignore=True, setting_print_flag=False):
    """
    print lattice (virtual coordinate x1 to x2, y1 to y2, expected int)

    axis_ignore=False         --> draw at coor=0
                True(default) --> not draw (easy to change the tex source by delete some indices)

    setting_print_flag=True           --> print interval-width and scale setting example
                       False(default) --> not print
    """

    # real coordinate from virtual
    [r_x1, r_x2, r_y1, r_y2] = map(lambda x: x * unit_length, [x1, x2, y1, y2])

    output = ""
    if setting_print_flag:
        output += r"{p}{p} require tikzsetting2015m2a" + "\n"
        output += r"{p}\setmyintervalwidth{{1.5}}" + "\n"
        output += r"{p}\begin{{tikzpicture}}[scale=1.5]" + "\n"

    x_index_max = x2 - x1 - 1
    x_indices = "1,2,..."
    if axis_ignore and (x1 < 0):
        i = -x1 # =abs(x1)
        x_indices += ",{0},{1},{2},...".format(i-1, i+1, i+2)
    x_indices += ",{0}".format(x_index_max)

    y_index_max = y2 - y1 - 1
    y_indices = "1,2,..."
    if axis_ignore and (y1 < 0):
        i = -y1 # =abs(y1)
        y_indices += ",{0},{1},{2},...".format(i-1, i+1, i+2)
    y_indices += ",{0}".format(y_index_max)

    output += tikz_indent + r"{p} lattice" + "\n"
    output += tikz_indent + r"\foreach \k in {{{x_indices}}}" + "\n"
    output += tikz_indent + r"    \draw[dash pattern=on \pgflinewidth off \myintervalwidth, dash phase=.5\pgflinewidth]%" + "\n"
    output += tikz_indent + r"      ($({r_x1},{r_y1})+ \k*({unit_x})$) -- ($({r_x1},{r_y2})+ \k*({unit_x})$);" + "\n"
    output += tikz_indent + r"\foreach \k in {{{y_indices}}}" + "\n"
    output += tikz_indent + r"    \draw[dash pattern=on \pgflinewidth off \myintervalwidth, dash phase=.5\pgflinewidth]%" + "\n"
    output += tikz_indent + r"      ($({r_x1},{r_y1})+ \k*({unit_y})$) -- ($({r_x2},{r_y1})+ \k*({unit_y})$);"
    print(output.format(x_indices=x_indices, y_indices=y_indices,
                        r_x1=r_x1, r_x2=r_x2, r_y1=r_y1, r_y2=r_y2,
                        unit_x = unit_x, unit_y = unit_y, p = "%")
    )

def perp_mark(A, B, C, angle=90, size=5):
    """
    print perpendicular mark into angle ABC
      A, B, C (str): name or coordinate without ()
      angle: default=90 (ABC: anticlockwise rotation (?))
                    270 (ABC: clockwise rotation (?))
      size: default=5 (pt)
    """

    output = tikz_indent + r"\draw ($({B})!{size}pt!({A})$)--($({B})!{size}pt!({A})!{size}pt!{angle}:({B})$)--($({B})!{size}pt!({C})$;"
    print(output.format(A=A, B=B, C=C, angle=angle, size=size))


def projection_to_axis(x,y,name=""):
    """
    print (if name != "") coordinate (name), (name+'x'), (name+'y')
          and dashed line (name+'x') -- (name) -- (name+'y')
    """
    if x * y == 0:
        print("% ignore: this point is on the axis.")
    else:
        if y > 0:
            pos_x = "below"
        else:
            pos_x = "above"

        if x > 0:
            pos_y = "left"
        else:
            pos_y = "right"

        output = ""
        if name == "":
            output += tikz_indent + r"\node at (${x}*({unit_x})$) [{pos_x}] {{${x}$}};" + "\n"
            output += tikz_indent + r"\node at (${y}*({unit_y})$) [{pos_y}] {{${y}$}};" + "\n"
            output += tikz_indent + r"\draw [dashed] (${x}*({unit_x})$) -- (${x}*({unit_x}){sgn_y}{y}*({unit_y})$) -- (${y}*({unit_y})$);"
            output += "{name}" # dummy
        else:
            output += tikz_indent + r"\coordinate ({name}) at (${x}*({unit_x}){sgn_y}{y}*({unit_y})$);" + "\n"
            output += tikz_indent + r"\coordinate ({name}x) at (${x}*({unit_x})$)" + "\n"
            output += tikz_indent*2 + r"node at ({name}x) [{pos_x}] {{${x}$}};" + "\n"
            output += tikz_indent + r"\coordinate ({name}y) at (${y}*({unit_y})$)" + "\n"
            output += tikz_indent*2 + r"node at ({name}y) [{pos_y}] {{${y}$}};" + "\n"
            output += tikz_indent + r"\draw [dashed] ({name}x) -- ({name}) -- ({name}y);"

        print(output.format(x = x, y = y, name = name,
                            unit_x = unit_x, unit_y = unit_y,
                            pos_x = pos_x, pos_y = pos_y,
                            sgn_y = sgn(y)))


#-- test ------------------------------------------------------
if __name__ == "__main__":
    import my_tikz_tools
    help(my_tikz_tools)

    print("---- test ----")
    p1 = abcy_to_x(1,-4,3,2/0.3)
    p2 = abcy_to_x(1,0,0,2/0.3)
    print("\n@-- parabola_abc(1,-4,3,p1[0],p1[1]) ----")
    parabola_abc(1,-4,3,p1[0],p1[1])
    print("\n@-- parabola_abc(1,0,0,p2[0],p2[1]) ----")
    parabola_abc(1,0,0,p2[0],p2[1])

    print("\n@-- parabola_apq(1,-2,1,-3,4) ----")
    parabola_apq(1,-2,1,-3,4)

    print("\n@-- axis(-1,2,-3,4) ----")
    axis(-1,2,-3,4)

    print("\n@-- lattice(-4,5,-3,2) ----")
    lattice(-4,5,-3,2)
    print("\n@-- lattice(2,5,-3,2) ----")
    lattice(2,5,-3,2)
    print("\n@-- lattice(-1,1,-1,1, axis_ignore=False) ----")
    lattice(-1,1,-1,1, axis_ignore=False)
    print("\n@-- lattice(-1,1,-1,1, setting_print_flag=True) ----")
    lattice(-1,1,-1,1, setting_print_flag=True)

    print("\n@-- perp_mark('A', 'P', 'B', angle=270, size=7) ----")
    perp_mark('A', 'P', 'B', angle=270, size=7)
    print("\n@-- perp_mark('C', 'Q', 'D') ----")
    perp_mark('C', 'Q', 'D')

    print("\n@-- projection_to_axis(1, 5, 'P') ----")
    projection_to_axis(1, 5, 'P')
    print("\n@-- projection_to_axis(-3, 5, 'Q') ----")
    projection_to_axis(-3, 5, 'Q')
    print("\n@-- projection_to_axis(4, -6,) ----")
    projection_to_axis(4, -6)

