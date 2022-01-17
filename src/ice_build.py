import numpy as np
import os
import math
import random
from numpy import genfromtxt
from .qmgr import add_qsub_dir
import pandas as pd


def yz_rotate(geom, yz_angle=np.pi / 4):
    """This will take the original xyz geometry, rotate by radians and displace by x,y,z"""

    # builds new array with correct atom order
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k - 1 : k, 0] = i
        k += 1

    # rotates molecule by given yz-angle in radians

    Y = geom[:, 2]
    Z = geom[:, 3]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_y, atom_z in np.nditer([Y, Z]):

        if atom_y > 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_z))
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y < 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_z))
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y > 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_z)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y < 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_z)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y == 0 and atom_z == 0:
            theta_0[k - 1 : k] = 0
            hyp[k - 1 : k] = 0

        elif atom_y > 0 and atom_z == 0:
            theta_0[k - 1 : k] = math.degrees(np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y < 0 and atom_z == 0:
            theta_0[k - 1 : k] = math.degrees(3 * np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y == 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(0)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        elif atom_y == 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(np.pi)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_z ** 2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k - 1 : k] = theta + math.degrees(yz_angle)
        k += 1

    xs = geom[:, 1]
    ys = np.zeros(int(len(geom[:, 0])))
    zs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        ys[k - 1 : k] = round(hypot * math.sin(math.radians(theta)), 8)
        zs[k - 1 : k] = round(hypot * math.cos(math.radians(theta)), 8)
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k - 1 : k, 1] = x
        k += 1

    k = 1
    for y in ys[:]:
        new_geom[k - 1 : k, 2] = y
        k += 1

    k = 1
    for z in zs[:]:
        new_geom[k - 1 : k, 3] = z
        k += 1

    return new_geom


def xz_rotate(geom, xz_angle=np.pi / 4):
    """This will take the original xyz geometry, rotate by radians and displace by x,y,z"""

    # builds new array with correct atom order
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k - 1 : k, 0] = i
        k += 1

    # rotates molecule by given yz-angle in radians

    X = geom[:, 1]
    Z = geom[:, 3]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_x, atom_z in np.nditer([X, Z]):

        if atom_x > 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_x / atom_z))
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x < 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_x / atom_z))
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x > 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_x / atom_z)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x < 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_x / atom_z)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x == 0 and atom_z == 0:
            theta_0[k - 1 : k] = 0
            hyp[k - 1 : k] = 0

        elif atom_x > 0 and atom_z == 0:
            theta_0[k - 1 : k] = math.degrees(np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x < 0 and atom_z == 0:
            theta_0[k - 1 : k] = math.degrees(3 * np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x == 0 and atom_z > 0:
            theta_0[k - 1 : k] = math.degrees(0)
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        elif atom_x == 0 and atom_z < 0:
            theta_0[k - 1 : k] = math.degrees(np.pi)
            hyp[k - 1 : k] = math.sqrt(atom_x ** 2 + atom_z ** 2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k - 1 : k] = theta + math.degrees(xz_angle)
        k += 1

    xs = np.zeros(int(len(geom[:, 0])))
    ys = geom[:, 2]
    zs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        xs[k - 1 : k] = round(hypot * math.sin(math.radians(theta)), 8)
        zs[k - 1 : k] = round(hypot * math.cos(math.radians(theta)), 8)
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k - 1 : k, 1] = x
        k += 1

    k = 1
    for y in ys[:]:
        new_geom[k - 1 : k, 2] = y
        k += 1

    k = 1
    for z in zs[:]:
        new_geom[k - 1 : k, 3] = z
        k += 1

    return new_geom


def xy_rotate(geom, xy_angle=np.pi / 4):
    """First, must initialize a np.array to store new geometry based on input geometry's size"""
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k - 1 : k, 0] = i
        k += 1

    Y = geom[:, 2]
    X = geom[:, 1]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_y, atom_x in np.nditer([Y, X]):
        """Accounts for each quadrant that the inverse tangent function produces"""

        if atom_y > 0 and atom_x > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_x))
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y < 0 and atom_x > 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_x))
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y > 0 and atom_x < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_x)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y < 0 and atom_x < 0:
            theta_0[k - 1 : k] = math.degrees(math.atan(atom_y / atom_x)) + 180
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y == 0 and atom_x == 0:
            theta_0[k - 1 : k] = 0
            hyp[k - 1 : k] = 0

        elif atom_y > 0 and atom_x == 0:
            theta_0[k - 1 : k] = math.degrees(np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y < 0 and atom_x == 0:
            theta_0[k - 1 : k] = math.degrees(3 * np.pi / 2)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y == 0 and atom_x > 0:
            theta_0[k - 1 : k] = math.degrees(0)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        elif atom_y == 0 and atom_x < 0:
            theta_0[k - 1 : k] = math.degrees(np.pi)
            hyp[k - 1 : k] = math.sqrt(atom_y ** 2 + atom_x ** 2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k - 1 : k] = theta + math.degrees(xy_angle)
        k += 1

    zs = geom[:, 3]
    ys = np.zeros(int(len(geom[:, 0])))
    xs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        ys[k - 1 : k] = round(hypot * math.sin(math.radians(theta)), 8)
        xs[k - 1 : k] = round(hypot * math.cos(math.radians(theta)), 8)
        k += 1

    """ Saves the rotated x and y values to new array"""

    k = 1
    for y in ys[:]:
        new_geom[k - 1 : k, 2] = y
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k - 1 : k, 1] = x
        k += 1
    k = 1
    for z in zs[:]:
        new_geom[k - 1 : k, 3] = z
        k += 1

    return new_geom


def displacement(new_geom, x_dis=5, y_dis=0, z_dis=0):
    """displacements for x, y, z coordinates for the whole monomer"""

    cnt = 0
    for x in new_geom[:, 1]:
        new_geom[cnt : cnt + 1, 1] = x + x_dis
        cnt += 1

    cnt = 0
    for y in new_geom[:, 2]:
        new_geom[cnt : cnt + 1, 2] = y + y_dis
        cnt += 1

    cnt = 0
    for z in new_geom[:, 3]:
        new_geom[cnt : cnt + 1, 3] = z + z_dis
        cnt += 1

    return new_geom


def convertTuple(tup):
    str = "".join(tup)
    return str


def ran_angle():
    """Randomly selects a rotation from 0 to 2pi"""
    return np.random.random_sample() * 4 * np.pi - 2 * np.pi
    # uses the Mersenne twister sequence to generate psuedo-random numbers
    # Mersenne twister generates Mersenne primes which are M_n=2^n-1
    # Passes Diehard tests but not all TestU01 tests


def ran_dis(boxlength):
    """Change the coefficient and subtracted constant to build the rectangular box of your choosing"""

    # change for rectangular box size
    return np.random.random_sample() * boxlength - boxlength / 2


def ran_dis_growth(boxlength, removed):
    """
    this will remove points closest to zero, error current state
    """
    pos_neg = np.random.randint(2)
    if pos_neg == 1:
        return np.random.uniform(removed, boxlength / 2)
    else:
        return -np.random.uniform(removed, boxlength / 2)


def distance(geom1, geom2):
    """Three dimensional distance formula for evaluating the distance betweeen
    molecules"""
    return math.sqrt(
        (geom1[1] - geom2[1]) ** 2
        + (geom1[2] - geom2[2]) ** 2
        + (geom1[3] - geom2[3]) ** 2
    )


def sample_without_replacement(arr):
    random.shuffle(arr)
    return arr.pop()


def random_arrangement_3(
    filenames,
    geo_dict,
    geom_num,
    num_molecules,
    box_length,
    minimum_distance_between_molecules,
    boxGrowth,
):
    num = 0
    random_list = []
    for n, i in enumerate(num_molecules):
        num += i
        for j in range(i):
            random_list.append(n)
    print(filenames, random_list, num_molecules)
    choice = sample_without_replacement(random_list)
    sequence = [choice]

    geo_spacer = {}
    for key, val in geo_dict.items():
        geo_spacer[key] = len(val)
    geom = geo_dict[filenames[choice]]
    spacer = geo_spacer[filenames[choice]]

    arching = geom[:, :]
    attempts = 0
    cnt = 1
    molecule = [spacer]
    check_tf = False
    while cnt < num:
        if not check_tf:
            choice = sample_without_replacement(random_list)
            print(random_list)
            geom = geo_dict[filenames[choice]]
            spacer = geo_spacer[filenames[choice]]
            check_tf = True

        yz = yz_rotate(geom, ran_angle())
        xy = xy_rotate(yz, ran_angle())
        xz = xz_rotate(xy, ran_angle())

        dis = displacement(
            xz,
            ran_dis(box_length),
            ran_dis(box_length),
            ran_dis(box_length),
        )
        failed_distance = False

        for i in range(len(molecule)):
            if failed_distance:
                break
            length_check = 0
            for m in molecule:
                length_check += m
            for k in range(len(dis)):
                for j in range(length_check):
                    dist_atoms = distance(dis[k, :], arching[j, :])
                    if dist_atoms < minimum_distance_between_molecules:
                        failed_distance = True
                        break
                if failed_distance:
                    break
            if not failed_distance:
                check_tf = False
        if not failed_distance:
            molecule.append(spacer)
            arching = np.concatenate((arching, dis))
            cnt += 1
            attempts = 0
            sequence.append(choice)
        else:
            if boxGrowth["enable"]:
                if attempts > 100:
                    box_length += boxGrowth["increment"]
                    attempts = 0
                    print(box_length)
                else:
                    attempts += 1
    arching = np.round_(arching, decimals=16)
    print("XYZ molecule {0}".format(geom_num))
    if boxGrowth["enable"]:
        print("The final box_length was", box_length)
    return arching, len(molecule), spacer, sequence


def clean_many_txt():
    """This will replace the numerical forms of the elements as their letters numbered in order"""

    f = open("many.txt", "r")
    a = ["6.000000 ", "8.000000 ", "1.000000 ", "7.000000 "]
    table = {
        "6.000000 ": "C",
        "8.000000 ": "O",
        "1.000000 ": "H",
        "7.000000 ": "N",
    }

    lst = []
    cnt2 = 0
    for line in f:
        cnt2 += 1
        for word in a:
            if word in line:
                convert_wrd = table[word]
                line = line.replace(word, convert_wrd + str(cnt2) + " ")

        lst.append(line)
    f.close()
    f = open("many.txt", "w")
    for line in lst:
        f.write(line)
    f.close()


def bond_lengths_2(geom, name):

    lines = []
    for i in range(len(geom[:, 0])):
        for j in range(len(geom[:, 0])):

            distances = round(distance(geom[i, :], geom[j, :]), 3)

            if j > i and distances < 1.8:

                line = (
                    str(i + 1) + " ",
                    str(j + 1) + " ",
                    "=" + str(distances),
                    " B",
                    "\n",
                    str(i + 1) + " ",
                    str(j + 1) + " ",
                    "F\n",
                )
                line = convertTuple(line)
                lines.append(line)
            if j > i and distances < 1.8 and i == len(geom[:, 0]):

                line = (
                    str(i + 1) + " ",
                    str(j + 1) + " ",
                    "=" + str(distances),
                    " B",
                    "\n",
                    str(i + 1) + " ",
                    str(j + 1) + " ",
                    "F",
                )
                line = convertTuple(line)
                lines.append(line)
    lines = "".join(lines)
    with open(name, "w") as fp:
        fp.write(lines)


def bond_angles_2(geom, name):
    length = len(geom[:, 0])
    angles = []
    for i in range(length - 2):

        ab = distance(geom[i, :], geom[i + 1, :])
        ac = distance(geom[i, :], geom[i + 2, :])
        bc = distance(geom[i + 1, :], geom[i + 2, :])

        angle = math.degrees(
            math.acos((ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab * ac))
        )

        angle = round(angle, 3)
        if i < length:
            ang = (
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " ",
                "=" + str(angle),
                " B\n",
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " F\n",
            )
            ang = convertTuple(ang)
            angles.append(ang)
        if i == length:
            ang = (
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " ",
                "=" + str(angle),
                " B\n",
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " F",
            )
            ang = convertTuple(ang)
            angles.append(ang)
    angles = "".join(angles)
    with open(name, "w") as fp:
        fp.write(angles)


def dihedral_2(geom, name):
    """Praxeolitic formula
    1 sqrt, 1 cross product"""
    length = len(geom[:, 0])
    di_angles = []

    for i in range(length - 3):
        p0 = geom[i, 1:]  # in the form np.array[x,y,z]
        p1 = geom[i + 1, 1:]
        p2 = geom[i + 2, 1:]
        p3 = geom[i + 3, 1:]

        b0 = -1.0 * (p1 - p0)
        b1 = p2 - p1
        b2 = p3 - p2

        # normalize b1 so that it does not influence magnitude of vector
        # rejections that come next
        b1 /= np.linalg.norm(b1)

        # vector rejections
        # v = projection of b0 onto plane perpendicular to b1
        #   = b0 minus component that aligns with b1
        # w = projection of b2 onto plane perpendicular to b1
        #   = b2 minus component that aligns with b1
        v = b0 - np.dot(b0, b1) * b1
        w = b2 - np.dot(b2, b1) * b1

        # angle between v and w in a plane is the torsion angle
        # v and w may not be normalized but that's fine since tan is y/x
        x = np.dot(v, w)
        y = np.dot(np.cross(b1, v), w)
        di_ang = np.degrees(np.arctan2(y, x))
        di_angle = round(di_ang, 3)
        if i < length:
            di_ang = (
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " ",
                str(i + 4) + " ",
                "=" + str(di_angle),
                " B\n",
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " " + str(i + 4) + " ",
                " F\n",
            )
            di_ang = convertTuple(di_ang)
            di_angles.append(di_ang)
        if i == length:
            di_ang = (
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " ",
                str(i + 4) + " ",
                "=" + str(di_angle),
                " B\n",
                str(i + 1) + " ",
                str(i + 2) + " ",
                str(i + 3) + " " + str(i + 4) + " ",
                " F",
            )
            di_ang = convertTuple(di_ang)
            di_angles.append(di_ang)

    di_angles = "".join(di_angles)
    with open(name, "w") as fp:
        fp.write(di_angles)


def constraints_2(molecule_cnt, spacer, sequence, dihedral=False):
    """Must be called after random_arrangement() since it takes the value of len(molecule) from the function's output. Takes the bonds.txt and angles.txt of the monomer's geometry"""

    if sequence[0] == 0:
        bsas = pd.read_csv("bonds1.txt", sep=" ", header=None)
        df_bds = bsas.replace(np.nan, " ", regex=True)

        bsas = pd.read_csv("angles1.txt", sep=" ", header=None)
        df_ang = bsas.replace(np.nan, " ", regex=True)
        if dihedral == True:
            bsas = pd.read_csv("dihedral1.txt", sep=" ", header=None)
            dh_ang = bsas.replace(np.nan, " ", regex=True)

    else:
        bsas = pd.read_csv("bonds2.txt", sep=" ", header=None)
        df_bds = bsas.replace(np.nan, " ", regex=True)

        bsas = pd.read_csv("angles2.txt", sep=" ", header=None)
        df_ang = bsas.replace(np.nan, " ", regex=True)
        if dihedral == True:
            bsas = pd.read_csv("dihedral2.txt", sep=" ", header=None)
            dh_ang = bsas.replace(np.nan, " ", regex=True)

    for row in df_bds.itertuples():
        if df_bds.columns[0] == int:
            df_bds.at[row.Index, 0]
        if df_bds.columns[1] == int:
            df_bds.at[row.Index, 1]

        df_bds.loc[row.Index, 0]
        df_bds.loc[row.Index, 1]

    for row in df_ang.itertuples():
        if df_ang.columns[0] == int:
            df_ang.at[row.Index, 0]
        if df_ang.columns[1] == int:
            df_ang.at[row.Index, 1]
        if df_ang.columns[2] == int:
            df_ang.at[row.Index, 2]

        df_ang.loc[row.Index, 0]
        df_ang.loc[row.Index, 1]
        df_ang.loc[row.Index, 2]

    if dihedral == True:
        for row in dh_ang.itertuples():
            if dh_ang.columns[0] == int:
                dh_ang.at[row.Index, 0]
            if dh_ang.columns[1] == int:
                dh_ang.at[row.Index, 1]
            if dh_ang.columns[2] == int:
                dh_ang.at[row.Index, 2]
            if dh_ang.columns[3] == int:
                dh_ang.at[row.Index, 3]
            dh_ang.loc[row.Index, 0]
            dh_ang.loc[row.Index, 1]
            dh_ang.loc[row.Index, 2]
            dh_ang.loc[row.Index, 3]

    num = molecule_cnt - 1
    if dihedral == True:
        fnames = [df_ang, df_bds, dh_ang]
    else:
        fnames = [df_ang, df_bds]

    df = pd.concat(fnames, ignore_index=True)

    for i in range(num):

        if sequence[i + 1] == 0:
            bsas = pd.read_csv("bonds1.txt", sep=" ", header=None)
            df_bds = bsas.replace(np.nan, " ", regex=True)

            bsas = pd.read_csv("angles1.txt", sep=" ", header=None)
            df_ang = bsas.replace(np.nan, " ", regex=True)
            if dihedral == True:
                bsas = pd.read_csv("dihedral1.txt", sep=" ", header=None)
                dh_ang = bsas.replace(np.nan, " ", regex=True)

        else:
            bsas = pd.read_csv("bonds2.txt", sep=" ", header=None)
            df_bds = bsas.replace(np.nan, " ", regex=True)

            bsas = pd.read_csv("angles2.txt", sep=" ", header=None)
            df_ang = bsas.replace(np.nan, " ", regex=True)
            if dihedral == True:
                bsas = pd.read_csv("dihedral2.txt", sep=" ", header=None)
                dh_ang = bsas.replace(np.nan, " ", regex=True)

        for row in df_bds.itertuples():

            df_bds.loc[row.Index, 0] += spacer
            df_bds.loc[row.Index, 1] += spacer

        for row in df_ang.itertuples():

            df_ang.loc[row.Index, 0] += spacer
            df_ang.loc[row.Index, 1] += spacer
            df_ang.loc[row.Index, 2] += spacer

        if dihedral == True:
            for row in dh_ang.itertuples():

                dh_ang.loc[row.Index, 0] += spacer
                dh_ang.loc[row.Index, 1] += spacer
                dh_ang.loc[row.Index, 2] += spacer
                dh_ang.loc[row.Index, 3] += spacer

            df = pd.concat([df, df_ang, df_bds, dh_ang], ignore_index=True)
        else:

            df = pd.concat([df, df_ang, df_bds], ignore_index=True)

    return df


def constraints_3(
    default_dir, spacer, sequence, geo_dict, filenames, dihedral=False
):
    pos = 0
    bonds_txt = default_dir + "/bonds.txt"
    angles_txt = default_dir + "/angles.txt"
    dihedral_txt = default_dir + "/dihedral.txt"
    for i in sequence:
        dict_name = filenames[i]
        spacer = len(geo_dict[dict_name])

        bsas = pd.read_csv(bonds_txt, sep=" ", header=None)
        df_bds = bsas.replace(np.nan, " ", regex=True)
        if spacer > 2:
            bsas = pd.read_csv(angles_txt, sep=" ", header=None)
            df_ang = bsas.replace(np.nan, " ", regex=True)
        if dihedral:
            bsas = pd.read_csv(dihedral_txt, sep=" ", header=None)
            dh_ang = bsas.replace(np.nan, " ", regex=True)

        for row in df_bds.itertuples():
            df_bds.loc[row.Index, 0] += pos
            df_bds.loc[row.Index, 1] += pos
        if spacer > 2:
            # spacer >2
            for row in df_ang.itertuples():

                df_ang.loc[row.Index, 0] += pos
                df_ang.loc[row.Index, 1] += pos
                df_ang.loc[row.Index, 2] += pos

            if dihedral == True:
                for row in dh_ang.itertuples():

                    dh_ang.loc[row.Index, 0] += pos
                    dh_ang.loc[row.Index, 1] += pos
                    dh_ang.loc[row.Index, 2] += pos
                    dh_ang.loc[row.Index, 3] += pos

                df = pd.concat([df, df_ang, df_bds, dh_ang], ignore_index=True)

                fnames = [df_ang, df_bds, dh_ang]
            else:
                fnames = [df_ang, df_bds]

        # spacer >2
        else:
            fnames = [df_bds]
        if pos == 0:
            df = pd.concat(fnames, ignore_index=True)
        else:

            if dihedral:
                df = pd.concat([df, df_ang, df_bds, dh_ang], ignore_index=True)
            else:
                if spacer > 2:
                    df = pd.concat([df, df_ang, df_bds], ignore_index=True)
                # spacer >2
                else:
                    df = pd.concat([df, df_bds], ignore_index=True)

        pos += spacer

    return df


def clean_dataframe(df):
    """This cleans the output of the dataframe to remove blanks"""
    df.to_csv("dataframe_test.csv", index=False, sep=" ")

    f = open("dataframe_test.csv", "r")
    a = ['" "']
    lst = []
    for line in f:
        for word in a:
            if word in line:
                line = line.replace(word, "")
        lst.append(line)
    f.close()
    f = open("dataframe_test.csv", "w")
    for line in lst:
        f.write(line)
    f.close()


def make_input_dir(
    dataPath, default_dir, dir_name_number, method, basis_set, mem_com, mem_pbs
):
    """
    Combines the geometry output and the constrained output.
    Then makes the .com and .pbs files in a subdirectory
    """

    data = data2 = ""

    with open("many.txt") as fp:
        data = fp.read()
    with open("dataframe_test.csv") as fp:
        data2 = fp.read()

    data += "\n\n"
    data += data2
    charges = "0 1"

    new_dir = dataPath + "/geom" + str(dir_name_number)
    os.mkdir(new_dir)
    with open(new_dir + "/mex.com", "w") as fp:
        fp.write("%mem={0}mb\n".format(mem_com))
        fp.write("%nprocs=4\n")
        fp.write(
            "#N {0}/".format(method)
            + "{0} opt=ModRedundant FREQ\n".format(basis_set)
        )
        fp.write("\n")
        fp.write("Name ModRedundant\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)

    with open(new_dir + "/mex.pbs", "w") as fp:
        fp.write("#!/bin/sh\n")
        fp.write(
            "#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l "
        )
        fp.write("mem={0}gb\n".format(mem_pbs))
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n"
        )
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
        )
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
        )
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
        )
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
        )
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
        )
        fp.write(
            """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
        )
        fp.write(
            """    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n"""
        )
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out\n\nrm -r $scrdir\n"
        )

    print("geom" + str(dir_name_number))
    add_qsub_dir("./", new_dir, default_dir + "/qsub_queue.txt")
    # os.chdir(new_dir)
    # os.system("qsub mex.pbs")
    # os.chdir(default_dir)

    # os.chdir("../..")


def make_input_files():
    """Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory"""

    data = data2 = ""

    with open("many.txt") as fp:
        data = fp.read()

    # Reading data from file2
    with open("dataframe_test.csv") as fp:
        data2 = fp.read()

    data += "\n\n"
    data += data2
    charges = "0 1"

    with open("mex.com", "w") as fp:
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=1\n")
        fp.write("#N wB97XD/6-31G(d) opt=ModRedundant FREQ\n")
        fp.write("\n")
        fp.write(
            "CH2O3 ModRedundant - Minimalist working constrained optimisation\n"
        )
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)

    with open("mex.pbs", "w") as fp:
        fp.write("#!/bin/sh\n")
        fp.write(
            "#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l "
        )
        fp.write("mem=15gb\n")
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n"
        )
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
        )
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
        )
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
        )
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
        )
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
        )
        fp.write(
            """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
        )
        fp.write(
            """    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n"""
        )
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out\n\nrm -r $scrdir\n"
        )


def ice_build(
    config={
        "enable": True,
        "jobList": [
            {
                "dataPath": "data/test",
                "inputCartesianFiles": [
                    {"file": "mon_h2o.xyz", "count": 1},
                    {"file": "mon_nh3.xyz", "count": 0},
                ],
                "clusters": 5,
                "boxLength": 3,
                "boxGrowth": {"enable": True, "increment": 3},
                "minDistanceMolecules": 2,
                "optMethod": "B3LYP",
                "optBasisSet": "6-31G(d)",
                "memComFile": "1600",
                "memPBSFile": "15",
                "startNum": 1,
            },
            {
                "dataPath": "data/test2",
                "inputCartesianFiles": [
                    {"file": "mon_h2o.xyz", "count": 0},
                    {"file": "mon_nh3.xyz", "count": 1},
                ],
                "clusters": 5,
                "boxLength": 3,
                "boxGrowth": {"enable": True, "increment": 3},
                "minDistanceMolecules": 2,
                "optMethod": "B3LYP",
                "optBasisSet": "6-31G(d)",
                "memComFile": "1600",
                "memPBSFile": "15",
                "startNum": 1,
            },
        ],
    },
):
    for job in config["jobList"]:
        default_dir = os.getcwd()
        filenames = []
        molecules_in_cluster = []
        for i in job["inputCartesianFiles"]:
            filenames.append("input_geoms/" + i["file"])
            molecules_in_cluster.append(i["count"])
        number_clusters = job["clusters"]
        box_length = job["boxLength"]
        minium_distance_between_molecules = job["minDistanceMolecules"]
        method_opt = job["optMethod"]
        basis_set_opt = job["optBasisSet"]
        mem_com_opt = job["memComFile"]
        mem_pbs_opt = job["memPBSFile"]
        start_num = job["startNum"]
        dataPath = job["dataPath"]
        boxGrowth = job["boxGrowth"]

        if not os.path.exists("data"):
            os.mkdir("data")
        if os.path.exists(dataPath):
            print(
                "ice_build.py: DataPath from %s/input.json already exists."
                % default_dir
            )
            return
        else:
            os.mkdir(dataPath)

        geo_dict = {}
        for f in filenames:
            geo_dict[f] = genfromtxt(f, delimiter=" ")

        for i in range(start_num, number_clusters + start_num, 1):
            final, mole, spacer, sequence = random_arrangement_3(
                filenames,
                geo_dict,
                i,
                molecules_in_cluster,
                box_length,
                minium_distance_between_molecules,
                boxGrowth,
            )

            out_file = "many.txt"

            np.savetxt(out_file, final, fmt="%.6f")

            clean_many_txt()
            pos = 0
            for key, val in geo_dict.items():
                bonds_txt = default_dir + "/bonds.txt"
                angles_txt = default_dir + "/angles.txt"
                # dihedral_txt = default_dir + "/dihedral.txt"

                bond_lengths_2(val, bonds_txt)
                bond_angles_2(val, angles_txt)
                pos += 1

            df = constraints_3(
                default_dir, spacer, sequence, geo_dict, filenames
            )

            clean_dataframe(df)

            make_input_dir(
                dataPath,
                default_dir,
                i,
                method_opt,
                basis_set_opt,
                mem_com_opt,
                mem_pbs_opt,
            )  # uncomment when want directories
            print("\n next directory\n")

        os.remove("bonds.txt")
        os.remove("angles.txt")
        os.remove("many.txt")
        os.remove("dataframe_test.csv")


# main()
