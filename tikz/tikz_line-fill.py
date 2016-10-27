# -*- coding: utf-8 -*-

import math

## confusion camel and snake...

def create_mask_lines(angle, d, y0, pSW, pNE):
    lines = []
    if angle % 90 != 0:
        dy = d/math.cos(math.radians(angle))
        def line_y(i, x):
            return math.tan(math.radians(angle))*x + y0 + dy*i
        def line_x(i, y):
            return (y - y0 - dy*i) / math.tan(math.radians(angle)) # Is " *cotan(angle)" better than this?

        xW = pSW[0]
        xE = pNE[0]
        yS = pSW[1]
        yN = pNE[1]

        i = 0
        line = [(0,0),(0,0)] # dummy
        while len(line) == 2:
            line = [] # represented by a pair of tupple: [init_pt, term_pt]
            yE = line_y(i, xE)
            yW = line_y(i, xW)
            xS = line_x(i, yS)
            xN = line_x(i, yN)
            # West
            if yS <= yW < yN:
                line += [(xW, yW)]
            # North
            if xW <= xN < xE:
                line += [(xN, yN)]
            # East
            if yS < yE <= yN:
                line += [(xE, yE)]
            # South
            if xW < xS <= xE:
                line += [(xS, yS)]
            if len(line) == 2:
                lines += [line]
            i += 1

        i = -1
        line = [(0,0),(0,0)] # dummy
        while len(line) == 2:
            line = [] # represented by a pair of tupple: [init_pt, term_pt]
            yE = line_y(i, xE)
            yW = line_y(i, xW)
            xS = line_x(i, yS)
            xN = line_x(i, yN)
            # West
            if yS <= yW < yN:
                line += [(xW, yW)]
            # North
            if xW <= xN < xE:
                line += [(xN, yN)]
            # East
            if yS < yE <= yN:
                line += [(xE, yE)]
            # South
            if xW < xS <= xE:
                line += [(xS, yS)]
            if len(line) == 2:
                lines += [line]
            i += -1

    return lines

def is_inside(pt, path):
    """
    Require: path is cyclic (i.e. path[0] == path[-1])
    """
    x = 0
    y = 1

    # winding number algorithm
    winding_num = 0
    for i in range(len(path)-1):
        sgn = 0 # flag

        # upward edge
        if (path[i][y] <= pt[y]) and (path[i+1][y] > pt[y]):
            sgn = 1
        # downward edge
        elif (path[i][y] > pt[y]) and (path[i+1][y] <= pt[y]):
            sgn = -1

        if sgn != 0:
            t = (pt[y] - path[i][y]) / (path[i+1][y] - path[i][y]) # y = (1-t)*y_i + t*y_{i+1}
            intersection_x = (1-t) * path[i][x] + t * path[i+1][x] # path[i][x] + t * (path[i+1][x] - path[i][x]) is lower cost ?
            if pt[x] < intersection_x:
                winding_num += sgn

    if winding_num == 0:
        return False
    else:
        return True

def binary_search(pIn, pOut, path):
    pNext = ((pIn[0]+pOut[0])/2, (pIn[1]+pOut[1])/2)
    if is_inside(pNext, path):
        return [pNext, pOut]
    else:
        return [pIn, pNext]

def cc_intersection_angle(O1, r1, O2, r2):
    """
    angle at intersection of circle O1 and circle O2
    -2pi <= angle < 4pi (connect if inner arc include angle 0)
    return ((pair of angles for O1), (pair of angles for O2))
    """

    x = 0
    y = 1
    # direction cosine of vector O1 -> O2
    dc = (O2[x] - O1[x])/math.sqrt((O2[x] - O1[x])**2 + (O2[y] - O1[y])**2)

    angle0 = math.acos(dc)

    angle1 = math.acos( (d*d + r1*r1 - r2*r2) / (2*d*r1) )
    angle2 = math.acos( (d*d + r2*r2 - r1*r1) / (2*d*r2) )

    return ( (angle0 - angle1, angle0 + angle1), (-angle0 - angle2, angle0 + angle2) )

# --- main ---
def tikz_fill_lines(path, margin=0, angle=45, d=0.2, y0=0.3, search_accuracy=16, margin_accuracy=10**(-5)):
    """
    Create tikz src for line filling inside the path.
    search_accuracy > 2 (as much as necessary).
    unmounted: clipping.
    """
    tikz_line = r"  \draw [ultra thin] ({p1x:.6f}, {p1y:.6f}) -- ({p2x:.6f}, {p2y:.6f});" + "\n"
    tikz_src = r"  % --- line filling: angle = {angle}, d = {d} ---".format(angle=angle, d=d)
    tikz_src += "\n"

    path_xs = [path[i][0] for i in range(len(path))]
    path_ys = [path[i][1] for i in range(len(path))]

    pSW = (min(path_xs) -1, min(path_ys) -1)
    pNE = (max(path_xs) +1, max(path_ys) +1)

    lines = create_mask_lines(angle, d, y0, pSW, pNE)
    if path[0] != path[-1]:
        path += [path[0]] # cyclic

    INSIDE = 1
    OUTSIDE = 0
    x = 0
    y = 1

    for line in lines:
        in_out_flag = OUTSIDE
        prev_pt = (line[0][x], line[0][y])
        for i in range(1, search_accuracy+1):
            found = False
            t = i/search_accuracy
            pt = ((1-t)*line[0][x] + t*line[1][x], (1-t)*line[0][y] + t*line[1][y])
            if is_inside(pt, path):
                if in_out_flag == OUTSIDE:
                    pIn = pt
                    pOut = prev_pt
                    found = True
            else:
                if in_out_flag == INSIDE:
                    pIn = prev_pt
                    pOut = pt
                    found = True
            if found:
                while (abs(pIn[x]-pOut[x]) > margin_accuracy) or (abs(pIn[y]-pOut[y]) > margin_accuracy):
                    [pIn, pOut] = binary_search(pIn, pOut, path)
                if in_out_flag == OUTSIDE:
                    p1 = pIn
                    in_out_flag = INSIDE
                else:
                    p2 = pIn
                    tikz_src += tikz_line.format(p1x=p1[x], p1y=p1[y], p2x=p2[x], p2y=p2[y])
                    in_out_flag = OUTSIDE
            prev_pt = pt

    return tikz_src


if __name__ == "__main__":
    #path = [(0,0), (5,0), (6,6), (2,5)]
    #print(tikz_fill_lines(path))

    #path = [(-4,0), (-3.6,1), (-1.5,1), (-1.5,0)]
    #print(tikz_fill_lines(path, d=0.08))
    #path = [(1,0), (1,1), (1.6,1), (2,0)]
    #print(tikz_fill_lines(path, d=0.08))

    #path = [(3.5,0), (3.5,2), (-2,2), (-2,-2), (3.5,-2), (3.5,0)]
    #for i in range(720):
    #    path += [(1.5*math.cos(math.radians(-i)), 1.5*math.sin(math.radians(-i))-0.2 )]

    path = [(3.5,2), (-2,2), (-2,-2), (3.5,-2)]
    print(tikz_fill_lines(path, d=0.08))
