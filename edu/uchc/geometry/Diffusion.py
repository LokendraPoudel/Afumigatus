class Diffuse():
    """
    DIFFUSION IN CLOSED BOUNDARY CONDITIONS
    """
    def __init__(self, f, pde_factor, delta_t):
        self.f = f
        self.pde_factor = pde_factor
        self.delta_t = delta_t

    def solver(self, space, molecule, index):
        xbin = len(space)
        ybin = len(space[0])
        zbin = len(space[0][0])

        D = [[[0 for _ in range(zbin)] for _ in range(ybin)] for _ in range(xbin)]
        next = [[[0 for _ in range(zbin)] for _ in range(ybin)] for _ in range(xbin)]

        C_x = [0 for _ in range(xbin)]
        C_y = [0 for _ in range(ybin)]
        C_z = [0 for _ in range(zbin)]

        D_x = [0 for _ in range(xbin)]
        D_y = [0 for _ in range(ybin)]
        D_z = [0 for _ in range(zbin)]

        A  = -(3 - 2 * self.f)
        B  = self.pde_factor/self.delta_t + 2 * (3 - 2 * self.f)
        Bc = self.pde_factor/self.delta_t + (3 - 2 * self.f)
        C  = -(3 - 2 * self.f)
        E  = self.pde_factor/self.delta_t - 4 * self.f

        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    #print(space[x][y][z].molecules[molecule].get(index))
                    D[x][y][z] = E * space[x][y][z].molecules[molecule].get(index)
                    if y == 0 and z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y + 1][z].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index) + 2 * space[x][y][z].molecules[molecule].get(index))
                    elif y == 0 and z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y + 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + 2 * space[x][y][z].molecules[molecule].get(index))
                    elif y == ybin - 1 and z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y - 1][z].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index) + 2 * space[x][y][z].molecules[molecule].get(index))
                    elif y == ybin - 1 and z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y - 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + 2 * space[x][y][z].molecules[molecule].get(index))
                    elif y == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y + 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index) + space[x][y][z].molecules[molecule].get(index))
                    elif y == ybin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y - 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index) + space[x][y][z].molecules[molecule].get(index))
                    elif z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y - 1][z].molecules[molecule].get(index) + space[x][y + 1][z].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index) + space[x][y][z].molecules[molecule].get(index))
                    elif z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y + 1][z].molecules[molecule].get(index) + space[x][y - 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + space[x][y][z].molecules[molecule].get(index))
                    else:
                        D[x][y][z] = D[x][y][z] + self.f * (space[x][y - 1][z].molecules[molecule].get(index) + space[x][y + 1][z].molecules[molecule].get(index) + space[x][y][z - 1].molecules[molecule].get(index) + space[x][y][z + 1].molecules[molecule].get(index))


        for y in range(ybin):
            for z in range(zbin):
                for x in range(xbin):
                    if x == 0:
                        C_x[x] = C / Bc
                    #elif x == (xbin - 1):
                    #    C_x[x] = C / (Bc - A * C_x[x - 1])
                    else:
                        C_x[x] = C / (B - A * C_x[x - 1])
                for x in range(xbin):
                    if x == 0:
                        D_x[x] = D[x][y][z] / Bc
                    elif x == xbin - 1:
                        D_x[x] = (D[x][y][z] - A * D_x[x - 1]) / (Bc - A * C_x[x - 1])
                    else:
                        D_x[x] = (D[x][y][z] - A * D_x[x - 1]) / (B - A * C_x[x - 1])
                for x in reversed(range(xbin)):
                    if x == xbin - 1:
                        next[x][y][z] = D_x[x]
                    else:
                        next[x][y][z] = D_x[x] - C_x[x] * next[x + 1][y][z]


        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    D[x][y][z] = E * next[x][y][z];
                    if x == 0 and z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x+1][y][z] + next[x][y][z+1] + 2 * next[x][y][z])
                    elif x == 0 and z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x+1][y][z] + next[x][y][z-1] + 2 * next[x][y][z])
                    elif x == xbin - 1 and z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x][y][z+1] + 2 * next[x][y][z])
                    elif x == xbin - 1 and z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x][y][z-1] + 2 * next[x][y][z])
                    elif x == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x+1][y][z] + next[x][y][z-1] + next[x][y][z+1] + next[x][y][z])
                    elif x == xbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x][y][z-1] + next[x][y][z+1] + next[x][y][z])
                    elif z == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x+1][y][z] + next[x][y][z+1] + next[x][y][z])
                    elif z == zbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x+1][y][z] + next[x][y][z-1] + next[x][y][z])
                    else:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x-1][y][z] + next[x+1][y][z] + next[x][y][z-1] + next[x][y][z+1]);


        for x in range(xbin):
            for z in range(zbin):
                for y in range(ybin):
                    if y == 0:
                        C_y[y] = C / Bc
                    #elif y == ybin:
                    #    C_y[y] = C / (Bc - A * C_y[y - 1])
                    else:
                        C_y[y] = C / (B - A * C_y[y - 1])
                for y in range(ybin):
                    if y == 0:
                        D_y[y] = D[x][y][z] / Bc
                    elif y == ybin - 1:
                        D_y[y] = (D[x][y][z] - A * D_y[y - 1]) / (Bc - A * C_y[y - 1])
                    else:
                        D_y[y] = (D[x][y][z] - A * D_y[y - 1]) / (B - A * C_y[y - 1])

                for y in reversed(range(ybin)):
                    if y == ybin - 1:
                        next[x][y][z] = D_y[y]
                    else:
                        next[x][y][z] = D_y[y] - C_y[y] * next[x][y + 1][z]

        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    D[x][y][z] = E * next[x][y][z]
                    if y == 0 and x == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y+1][z] + next[x+1][y][z] + 2 * next[x][y][z])
                    elif y == 0 and x == xbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y+1][z] + next[x-1][y][z] + 2 * next[x][y][z])
                    elif y == ybin - 1 and x == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x+1][y][z] + 2 * next[x][y][z])
                    elif y == ybin - 1 and x == xbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x-1][y][z] + 2 * next[x][y][z])
                    elif y == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y+1][z] + next[x-1][y][z] + next[x+1][y][z] + next[x][y][z])
                    elif y == ybin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x-1][y][z] + next[x+1][y][z] + next[x][y][z])
                    elif x == 0:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x][y+1][z] + next[x+1][y][z] + next[x][y][z])
                    elif x == xbin - 1:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x][y+1][z] + next[x-1][y][z] + next[x][y][z])
                    else:
                        D[x][y][z] = D[x][y][z] + self.f * (next[x][y-1][z] + next[x][y+1][z] + next[x-1][y][z] + next[x+1][y][z])

        for y in range(ybin):
            for x in range(xbin):
                for z in range(zbin):
                    if z == 0:
                        C_z[z] = C / Bc
                    #elif z == zbin:
                    #    C_z[z] = C / (Bc - A * C_z[z - 1])
                    else:
                        C_z[z] = C / (B - A * C_z[z - 1])
                for z in range(zbin):
                    if z == 0:
                        D_z[z] = D[x][y][z] / Bc
                    elif z == zbin - 1:
                        D_z[z] = (D[x][y][z] - A * D_z[z - 1]) / (Bc - A * C_z[z - 1])
                    else:
                        D_z[z] = (D[x][y][z] - A * D_z[z - 1]) / (B - A * C_z[z - 1])

                for z in reversed(range(zbin)):
                    if z == zbin - 1:
                        next[x][y][z] = D_z[z]
                    else:
                        next[x][y][z] = D_z[z] - C_z[z] * next[x][y][z + 1]

        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    space[x][y][z].set_molecule_qtty(molecule, index, next[x][y][z])
                    #print(space[x][y][z].molecules[molecule].get(index))
