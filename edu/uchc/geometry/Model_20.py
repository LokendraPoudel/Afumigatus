import numpy as np
import json
from scipy import *
import struct
import sys
from multiprocessing import Process, Array, Condition, Manager
import math
import time
import ctypes
import os
import queue
import random

# tissue type
AIRWAY = "airway"
BLOOD_VESSEL = "blood vessel"

# function type
QUADRIC = "quadric"
VECTOR = "vector"
PLANE = "plane"

# tissue number
AIR = 0
EPITHELIUM = 1
REGULAR_TISSUE = 2
BLOOD = 3

BLOOD_VESSEL_LAYER = 3

# construct code
CONSTRUCT_BASIC = 0
CONSTRUCT_EPI = 1
CONSTRUCT_VESSEL = 2

# process state
PROCESSING = 0
READY = 1


class Quadric():
    def __init__(self, json):
        self.set_coef(json["cx"], json["cy"], json["cz"], json["r"])
        self.set_shift(json["a"], json["b"], json["c"])
        self.set_range(json["x_min"], json["x_max"], json["y_min"], json["y_max"], json["z_min"], json["z_max"])
        self.tissue_type = json["tissue_type"]

    def set_coef(self, cx, cy, cz, r):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.r = r

    def set_shift(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def set_range(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.z_min = z_min
        self.z_max = z_max


class Vector():
    def __init__(self, json):
        self.xt = np.poly1d(json["xt"])
        self.yt = np.poly1d(json["yt"])
        self.zt = np.poly1d(json["zt"])
        self.r = json["r"]
        self.t_min = json["t_min"]
        self.t_max = json["t_max"]
        self.set_range(json["x_min"], json["x_max"], json["y_min"], json["y_max"], json["z_min"], json["z_max"])
        self.tissue_type = json["tissue_type"]
        # print(self.xt)

    def set_range(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.z_min = z_min
        self.z_max = z_max

    def get_val(self, t):
        return [self.xt(t), self.yt(t), self.zt(t)]


class Geometry():
    def __init__(self, xbin, ybin, zbin, grid, multi_process, vessel_layer_json):
        self.xbin = xbin
        self.ybin = ybin
        self.zbin = zbin
        self.grid = grid
        #self.geo = Array(ctypes.c_double, xbin * ybin * zbin)
        self.lock = Array(ctypes.c_double, multi_process)

        self.set_vessel_layer_params(vessel_layer_json)

        self.multi_process = multi_process

        # for i in range(len(self.geo)):
        #     self.geo[i] = REGULAR_TISSUE
        for x in range(xbin):
            for y in range(ybin):
                for z in range(zbin):
                    grid[x][y][z].tissue_type = REGULAR_TISSUE

        for i in range(len(self.lock)):
            self.lock[i] = PROCESSING

        # geo = np.full((xbin,ybin,zbin), 2)
        self.l = []  # function list
        self.plane = []

    def set_vessel_layer_params(self, json):
        self.vessel_xmin = json["x_min"]
        self.vessel_xmax = json["x_max"]

        self.vessel_ymin = json["y_min"]
        self.vessel_ymax = json["y_max"]

        self.vessel_zmin = json["z_min"]
        self.vessel_zmax = json["z_max"]

        self.interstitium = json["interstitium"]

    # check if a point is in function's domain
    def in_range(self, x, y, z, function):
        return x >= function.x_min and x <= function.x_max and y >= function.y_min and y < function.y_max and z >= function.z_min and z < function.z_max

    # check if a point is inside the geometry space
    def in_range_geo(self, x, y, z):
        return x >= 0 and x < self.xbin and y >= 0 and y < self.ybin and z >= 0 and z < self.zbin

    # return the distance between two points
    def distance(self, x1, x2, y1, y2, z1, z2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    def add(self, function):
        self.l.append(function)

    def add_plane(self, function):
        self.plane.append(function)

    def construct(self):
        section = math.floor(self.xbin / self.multi_process)
        current = 0
        processes = []

        manager = Manager()
        condition = manager.Condition()

        for i in range(self.multi_process):
            if i == self.multi_process - 1:  # last section
                processes.append(Process(target=self.construct_multi,
                                         args=(current, self.xbin, 0, self.ybin, 0, self.zbin, i, condition,)))

            else:
                processes.append(Process(target=self.construct_multi,
                                         args=(current, current + section, 0, self.ybin, 0, self.zbin, i, condition,)))

            current += section

        for process in processes:
            process.start()

        for process in processes:
            process.join()

    def test_and_wait(self, condition):
        lock = np.frombuffer(self.lock.get_obj())

        wait = False

        with condition:
            for i in lock:
                if i != READY:
                    wait = True
                    # print(str(os.getpid()) + " waiting")
                    # sys.stdout.flush()
                    condition.wait()
                    break

            if wait == False:
                for i in range(len(lock)):
                    lock[i] = PROCESSING

                # print(str(os.getpid()) + " notifying")
                condition.notify_all()

    def construct_multi(self, x_min, x_max, y_min, y_max, z_min, z_max, id, condition):
        start_time = time.time()
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                for z in range(z_min, z_max):
                    for function in self.l:
                        self.check_geometry_type(function, x, y, z, CONSTRUCT_BASIC)

        lock = np.frombuffer(self.lock.get_obj())
        lock[id] += 1
        self.test_and_wait(condition)

        for function in self.l:
            function.r += 1
            # print(function.r)

        print("constructing epi")
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                for z in range(z_min, z_max):
                    for function in self.l:
                        self.check_geometry_type(function, x, y, z, CONSTRUCT_EPI)

        lock = np.frombuffer(self.lock.get_obj())
        lock[id] += 1
        self.test_and_wait(condition)

        for function in self.l:
            function.r += self.interstitium + 1

        print("constructing vessel")

        section = math.ceil((self.vessel_xmin + self.vessel_xmax) / self.multi_process)
        vessel_xmin = self.vessel_xmin + section * id
        vessel_xmax = vessel_xmin + section

        for x in range(vessel_xmin, vessel_xmax):
            for y in range(self.vessel_ymin, self.vessel_ymax):
                for z in range(self.vessel_zmin, self.vessel_zmax):
                    for function in self.l:
                        self.check_geometry_type(function, x, y, z, CONSTRUCT_VESSEL)

        print("--- process: " + str(os.getpid()) + " ends in %s seconds ---" % (time.time() - start_time))

    def check_geometry_type(self, function, x, y, z, code):
        # print(type(function))
        if self.in_range(x, y, z, function):
            if (type(function) is Quadric):

                d = function.cx * (x + function.a) ** 2 + function.cy * (y + function.b) ** 2 + function.cz * (
                            z + function.c) ** 2

                if code == CONSTRUCT_VESSEL:
                    if d <= function.r ** 2 and d > (function.r - 1) ** 2:
                        self.change_tissue_type(function, x, y, z, code)

                else:
                    if d <= function.r ** 2:
                        self.change_tissue_type(function, x, y, z, code)

            elif (type(function) is Vector):
                xt = function.xt - np.poly1d([x])
                xt = xt * xt

                yt = function.yt - np.poly1d([y])
                yt = yt * yt

                zt = function.zt - np.poly1d([z])
                zt = zt * zt

                p = xt + yt + zt
                p = p.deriv()

                # root = queue.Queue()
                root = p.r[:]
                np.append(root, function.t_min)
                np.append(root, function.t_max)

                for r in root:
                    # print(r)
                    if r >= function.t_min and r <= function.t_max and self.distance(x, function.xt(r), y,
                                                                                     function.yt(r), z,
                                                                                     function.zt(r)) <= function.r:
                        self.change_tissue_type(function, x, y, z, code)
                        break

    def change_tissue_type(self, function, x, y, z, code):
        ## print("geo size")
        ## print (len(geo.get_obj()))
        #g = np.frombuffer(self.geo.get_obj())
        ## print("b size")
        ## print (b.size)
        #g = g.reshape(self.zbin, self.ybin, self.xbin).transpose()

        if code == CONSTRUCT_BASIC:
            if (function.tissue_type == AIRWAY):
                self.grid[x][y][z].tissue_type = AIR
            elif (function.tissue_type == BLOOD_VESSEL):
                self.grid[x][y][z].tissue_type = BLOOD
                # print("blood_vessel")
            else:
                raise Exception("unknown tissue type")

        elif code == CONSTRUCT_EPI:
            if (function.tissue_type == AIRWAY and self.grid[x][y][z].tissue_type == REGULAR_TISSUE):
                self.grid[x][y][z].tissue_type = EPITHELIUM
                # print (x,y,z)

        elif code == CONSTRUCT_VESSEL:
            if (function.tissue_type == AIRWAY and self.grid[x][y][z].tissue_type == REGULAR_TISSUE):
                self.grid[x][y][z].tissue_type = BLOOD

    def write_to_file(self, filename="geometry.vtk"):
        f = open(filename, "w")
        f.write("# vtk DataFile Version 4.2\n")
        f.write("Aspergillus simulation: Geometry\n")
        f.write("BINARY\n")
        f.write("DATASET STRUCTURED_POINTS\n")
        f.write("DIMENSIONS " + str(self.xbin) + " " + str(self.ybin) + " " + str(self.zbin) + "\n")
        f.write("ASPECT_RATIO 20 20 20\n")
        f.write("ORIGIN 0 0 0\n")
        f.write("POINT_DATA " + str(self.xbin * self.ybin * self.zbin) + "\n")
        f.write("SCALARS TissueType unsigned_char 1\n")
        f.write("LOOKUP_TABLE default\n")
        f.close()

        f = open(filename, "ab")
        array = np.frombuffer(self.geo.get_obj())
        array = array.astype(int)

        b = struct.pack(len(array) * 'B', *array)
        f.write(b)
        f.close()


def main(argv):
    start_time = time.time()

    if (len(argv) != 2):
        print("usage: geometry.yt <inputfile>")
    else:
        with open(argv[1]) as f:
            data = json.load(f)

        dimen = data["dimension"]
        g = Geometry(dimen["xbin"], dimen["ybin"], dimen["zbin"], data["multi_process"], data["vessel layer"])

        # pprint(data)
        for function in data["function"]:

            if (function["type"] == QUADRIC):
                f = Quadric(function)
                g.add(f)
            elif (function["type"] == VECTOR):
                f = Vector(function)
                g.add(f)

        g.construct()
        # g.add_epithelium()
        g.write_to_file(data["target"])

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main(sys.argv)