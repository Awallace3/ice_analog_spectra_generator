import numpy as np
import os
import math
import random
from numpy import genfromtxt
import numpy as npimport
from numpy import genfromtxt
import pandas as pd
#import secrets


def yz_rotate(geom, yz_angle=np.pi/4):
    """This will take the original xyz geometry, rotate by radians and displace by x,y,z"""

    # builds new array with correct atom order
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k-1:k, 0] = i
        k += 1

    # rotates molecule by given yz-angle in radians

    Y = geom[:, 2]
    Z = geom[:, 3]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_y, atom_z in np.nditer([Y, Z]):

        if atom_y > 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_z))
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y < 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_z))
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y > 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_z)) + 180
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y < 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_z)) + 180
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y == 0 and atom_z == 0:
            theta_0[k-1:k] = 0
            hyp[k-1:k] = 0

        elif atom_y > 0 and atom_z == 0:
            theta_0[k-1:k] = math.degrees(np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y < 0 and atom_z == 0:
            theta_0[k-1:k] = math.degrees(3*np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y == 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(0)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        elif atom_y == 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(np.pi)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_z**2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k-1:k] = theta + math.degrees(yz_angle)
        k += 1

    xs = geom[:, 1]
    ys = np.zeros(int(len(geom[:, 0])))
    zs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        ys[k-1:k] = round(hypot*math.sin(math.radians(theta)), 8)
        zs[k-1:k] = round(hypot*math.cos(math.radians(theta)), 8)
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k-1:k, 1] = x
        k += 1

    k = 1
    for y in ys[:]:
        new_geom[k-1:k, 2] = y
        k += 1

    k = 1
    for z in zs[:]:
        new_geom[k-1:k, 3] = z
        k += 1

    return new_geom


def xz_rotate(geom, xz_angle=np.pi/4):
    """This will take the original xyz geometry, rotate by radians and displace by x,y,z"""

    # builds new array with correct atom order
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k-1:k, 0] = i
        k += 1

    # rotates molecule by given yz-angle in radians

    X = geom[:, 1]
    Z = geom[:, 3]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_x, atom_z in np.nditer([X, Z]):

        if atom_x > 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_x/atom_z))
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x < 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_x/atom_z))
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x > 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_x/atom_z)) + 180
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x < 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_x/atom_z)) + 180
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x == 0 and atom_z == 0:
            theta_0[k-1:k] = 0
            hyp[k-1:k] = 0

        elif atom_x > 0 and atom_z == 0:
            theta_0[k-1:k] = math.degrees(np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x < 0 and atom_z == 0:
            theta_0[k-1:k] = math.degrees(3*np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x == 0 and atom_z > 0:
            theta_0[k-1:k] = math.degrees(0)
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        elif atom_x == 0 and atom_z < 0:
            theta_0[k-1:k] = math.degrees(np.pi)
            hyp[k-1:k] = math.sqrt(atom_x**2 + atom_z**2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k-1:k] = theta + math.degrees(xz_angle)
        k += 1

    xs = np.zeros(int(len(geom[:, 0])))
    ys = geom[:, 2]
    zs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        xs[k-1:k] = round(hypot*math.sin(math.radians(theta)), 8)
        zs[k-1:k] = round(hypot*math.cos(math.radians(theta)), 8)
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k-1:k, 1] = x
        k += 1

    k = 1
    for y in ys[:]:
        new_geom[k-1:k, 2] = y
        k += 1

    k = 1
    for z in zs[:]:
        new_geom[k-1:k, 3] = z
        k += 1

    return new_geom


def xy_rotate(geom, xy_angle=np.pi/4):
    """ First, must initialize a np.array to store new geometry based on input geometry's size """
    new_geom = np.zeros(((int(len(geom[:, 0]))), 4))
    k = 1
    for i in geom[:, 0]:
        new_geom[k-1:k, 0] = i
        k += 1

    Y = geom[:, 2]
    X = geom[:, 1]
    theta_0 = np.zeros(int(len(geom[:, 0])))
    hyp = np.zeros(int(len(geom[:, 0])))
    k = 1
    for atom_y, atom_x in np.nditer([Y, X]):
        """ Accounts for each quadrant that the inverse tangent function produces """

        if atom_y > 0 and atom_x > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_x))
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y < 0 and atom_x > 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_x))
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y > 0 and atom_x < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_x)) + 180
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y < 0 and atom_x < 0:
            theta_0[k-1:k] = math.degrees(math.atan(atom_y/atom_x)) + 180
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y == 0 and atom_x == 0:
            theta_0[k-1:k] = 0
            hyp[k-1:k] = 0

        elif atom_y > 0 and atom_x == 0:
            theta_0[k-1:k] = math.degrees(np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y < 0 and atom_x == 0:
            theta_0[k-1:k] = math.degrees(3*np.pi/2)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y == 0 and atom_x > 0:
            theta_0[k-1:k] = math.degrees(0)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        elif atom_y == 0 and atom_x < 0:
            theta_0[k-1:k] = math.degrees(np.pi)
            hyp[k-1:k] = math.sqrt(atom_y**2 + atom_x**2)

        k += 1

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1

    for i in range(len(theta_0)):
        if math.isnan(theta_0[i]) == True:
            theta_0[i] = 0

    theta_fin = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta in theta_0[:]:

        theta_fin[k-1:k] = theta + math.degrees(xy_angle)
        k += 1

    zs = geom[:, 3]
    ys = np.zeros(int(len(geom[:, 0])))
    xs = np.zeros(int(len(geom[:, 0])))
    k = 1
    for theta, hypot in np.nditer([theta_fin, hyp]):
        ys[k-1:k] = round(hypot*math.sin(math.radians(theta)), 8)
        xs[k-1:k] = round(hypot*math.cos(math.radians(theta)), 8)
        k += 1

    """ Saves the rotated x and y values to new array"""

    k = 1
    for y in ys[:]:
        new_geom[k-1:k, 2] = y
        k += 1

    k = 1
    for x in xs[:]:
        new_geom[k-1:k, 1] = x
        k += 1
    k = 1
    for z in zs[:]:
        new_geom[k-1:k, 3] = z
        k += 1

    return new_geom


def displacement(new_geom, x_dis=5, y_dis=0, z_dis=0):
    """ displacements for x, y, z coordinates for the whole monomer """

    cnt = 0
    for x in new_geom[:, 1]:
        new_geom[cnt: cnt+1, 1] = x + x_dis
        cnt += 1

    cnt = 0
    for y in new_geom[:, 2]:
        new_geom[cnt: cnt+1, 2] = y + y_dis
        cnt += 1

    cnt = 0
    for z in new_geom[:, 3]:
        new_geom[cnt: cnt+1, 3] = z + z_dis
        cnt += 1

    return new_geom


def convertTuple(tup):
    str = ''.join(tup)
    return str


def ran_angle():
    """ Randomly selects a rotation from 0 to 2pi """
    return np.random.random_sample()*4*np.pi - 2*np.pi
    # uses the Mersenne twister sequence to generate psuedo-random numbers
    # Mersenne twister generates Mersenne primes which are M_n=2^n-1
    # Passes Diehard tests but not all TestU01 tests


def ran_dis(boxlength):
    """ Change the coefficient and subtracted constant to build the rectangular box of your choosing """

    # change for rectangular box size
    return np.random.random_sample()*boxlength - boxlength/2


#############################################################
##############################################################
#############################################################

def distance(geom1, geom2):
    """ Three dimensional distance formula for evaluating the distance betweeen molecules """
    return math.sqrt((geom1[1] - geom2[1]) ** 2 + (geom1[2] - geom2[2])**2 + (geom1[3] - geom2[3])**2)


def random_arrangement_2(geom1, geom2, geom_num, num, percent_chance_mol_1, box_length, minium_distance_between_molecules):
    choice = int(np.random.choice(range(100)))
    sequence = []
    spacer_1 = len(geom1[:, 0])  # if spacing issue... investigate
    spacer_2 = len(geom2[:, 0])
    current_spacer = 0
    if choice >= percent_chance_mol_1:
        geom = geom1
        sequence.append(0)
        current_spacer = spacer_1
    else:
        geom = geom2
        sequence.append(1)
        current_spacer = spacer_2
    arching = geom[:, :]
    cnt = 1
    molecule = [current_spacer]

    check_tf = True
    while (cnt < num):
        #choice = int(np.random.choice([0, 1]))
        if check_tf == True:
            choice = int(np.random.choice(range(100)))
            mol_num = 0

            if choice >= percent_chance_mol_1:
                geom = geom1
                current_spacer = spacer_1

            else:
                geom = geom2
                mol_num = 1
                current_spacer = spacer_2
            check_tf = False
        """
        if choice == 0:
            geom = geom1
            print(len(geom))
        else:
            geom = geom2
            mol_num = 1
        """

        yz = yz_rotate(geom, ran_angle())
        xy = xy_rotate(yz, ran_angle())
        xz = xz_rotate(xy, ran_angle())

        dis = displacement(xz, ran_dis(box_length), ran_dis(
            box_length), ran_dis(box_length))
        #check_tf = False

        for i in range(len(molecule)):
            # print(molecule)

            #dist_CC = distance(dis[0, :], arching[0 + i*spacer_1, :])
            length_sum = 0
            dist_CC = distance(dis[0, :], arching[0 + length_sum, :])

            #print(arching[0 + length_sum, :])
            length_sum += molecule[i]
            # print(dist_CC)
            #print((dis[0, :]))
            #print(arching[0 + i*spacer, :])

            if dist_CC < minium_distance_between_molecules:  # change for the minimum distance between molecules
                check_tf = True

        if check_tf == False:
            molecule.append(current_spacer)
            arching = np.concatenate((arching, dis))
            cnt += 1
            sequence.append(mol_num)

    arching = np.round_(arching, decimals=16)
    print("\nXYZ molecule {0}\n".format(geom_num))
    for k in arching:
        print(int(k[0]), k[1], k[2], k[3])  # for quick testing purposes
    print()
    return arching, len(molecule), spacer_1, sequence


def clean_many_txt():
    """ This will replace the numerical forms of the elements as their letters numbered in order """

    f = open('many.txt', 'r')
    a = ['6.0 ', '8.0 ', '1.0 ']
    table = {
        '6.0 ': 'C', '8.0 ': 'O', '1.0 ': 'H'
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
    f = open('many.txt', 'w')
    for line in lst:
        f.write(line)
    f.close()


def bond_lengths_2(geom, name):

    lines = []
    for i in range(len(geom[:, 0])):
        for j in range(len(geom[:, 0])):

            distances = round(distance(geom[i, :], geom[j, :]), 3)

            if j > i and distances < 1.8:

                line = str(i + 1) + " ", str(j + 1) + " ", "=" + \
                    str(distances), " B", "\n", str(
                        i + 1) + " ", str(j + 1) + " ", "F\n"
                line = convertTuple(line)
                lines.append(line)
            if j > i and distances < 1.8 and i == len(geom[:, 0]):

                line = str(i + 1) + " ", str(j + 1) + " ", "=" + \
                    str(distances), " B", "\n", str(
                        i + 1) + " ", str(j + 1) + " ", "F"
                line = convertTuple(line)
                lines.append(line)
    lines = ''.join(lines)
    with open(name, 'w') as fp:
        fp.write(lines)


def bond_angles_2(geom, name):
    length = len(geom[:, 0])
    angles = []
    for i in range(length - 2):

        ab = distance(geom[i, :], geom[i+1, :])
        ac = distance(geom[i, :], geom[i+2, :])
        bc = distance(geom[i+1, :], geom[i+2, :])

        angle = math.degrees(
            math.acos((ab ** 2 + ac ** 2 - bc ** 2)/(2*ab*ac)))

        angle = round(angle, 3)
        if i < length:
            ang = str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " ", "=" + \
                str(angle), " B\n", str(i + 1) + \
                " ", str(i + 2) + " ", str(i + 3) + " F\n"
            ang = convertTuple(ang)
            angles.append(ang)
        if i == length:
            ang = str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " ", "=" + \
                str(angle), " B\n", str(i + 1) + \
                " ", str(i + 2) + " ", str(i + 3) + " F"
            ang = convertTuple(ang)
            angles.append(ang)
    angles = ''.join(angles)
    with open(name, 'w') as fp:
        fp.write(angles)


def dihedral_2(geom, name):
    """Praxeolitic formula
    1 sqrt, 1 cross product"""
    length = len(geom[:, 0])
    di_angles = []

    for i in range(length - 3):
        p0 = geom[i, 1:]  # in the form np.array[x,y,z]
        p1 = geom[i+1, 1:]
        p2 = geom[i+2, 1:]
        p3 = geom[i+3, 1:]

        b0 = -1.0*(p1 - p0)
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
        v = b0 - np.dot(b0, b1)*b1
        w = b2 - np.dot(b2, b1)*b1

        # angle between v and w in a plane is the torsion angle
        # v and w may not be normalized but that's fine since tan is y/x
        x = np.dot(v, w)
        y = np.dot(np.cross(b1, v), w)
        di_ang = np.degrees(np.arctan2(y, x))
        di_angle = round(di_ang, 3)
        if i < length:
            di_ang = (str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " ", str(i + 4) + " ", "=" + str(di_angle), " B\n",
                      str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " " + str(i + 4) + " ", " F\n")
            di_ang = convertTuple(di_ang)
            di_angles.append(di_ang)
        if i == length:
            di_ang = (str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " ", str(i + 4) + " ", "=" + str(di_angle), " B\n",
                      str(i + 1) + " ", str(i + 2) + " ", str(i + 3) + " " + str(i + 4) + " ", " F")
            di_ang = convertTuple(di_ang)
            di_angles.append(di_ang)

    di_angles = ''.join(di_angles)
    with open(name, 'w') as fp:
        fp.write(di_angles)


def constraints_2(molecule_cnt, spacer, sequence, dihedral=False):
    """ Must be called after random_arrangement() since it takes the value of len(molecule) from the function's output. Takes the bonds.txt and angles.txt of the monomer's geometry  """

    if sequence[0] == 0:
        bsas = pd.read_csv('bonds1.txt', sep=' ', header=None)
        df_bds = bsas.replace(np.nan, ' ', regex=True)

        bsas = pd.read_csv('angles1.txt', sep=' ', header=None)
        df_ang = bsas.replace(np.nan, ' ', regex=True)
        if dihedral == True:
            bsas = pd.read_csv('dihedral1.txt', sep=' ', header=None)
            dh_ang = bsas.replace(np.nan, ' ', regex=True)

    else:
        bsas = pd.read_csv('bonds2.txt', sep=' ', header=None)
        df_bds = bsas.replace(np.nan, ' ', regex=True)

        bsas = pd.read_csv('angles2.txt', sep=' ', header=None)
        df_ang = bsas.replace(np.nan, ' ', regex=True)
        if dihedral == True:
            bsas = pd.read_csv('dihedral2.txt', sep=' ', header=None)
            dh_ang = bsas.replace(np.nan, ' ', regex=True)

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

        if sequence[i+1] == 0:
            bsas = pd.read_csv('bonds1.txt', sep=' ', header=None)
            df_bds = bsas.replace(np.nan, ' ', regex=True)

            bsas = pd.read_csv('angles1.txt', sep=' ', header=None)
            df_ang = bsas.replace(np.nan, ' ', regex=True)
            if dihedral == True:
                bsas = pd.read_csv('dihedral1.txt', sep=' ', header=None)
                dh_ang = bsas.replace(np.nan, ' ', regex=True)

        else:
            bsas = pd.read_csv('bonds2.txt', sep=' ', header=None)
            df_bds = bsas.replace(np.nan, ' ', regex=True)

            bsas = pd.read_csv('angles2.txt', sep=' ', header=None)
            df_ang = bsas.replace(np.nan, ' ', regex=True)
            if dihedral == True:
                bsas = pd.read_csv('dihedral2.txt', sep=' ', header=None)
                dh_ang = bsas.replace(np.nan, ' ', regex=True)

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


def clean_dataframe(df):
    """ This cleans the output of the dataframe to remove blanks """
    df.to_csv('dataframe_test.csv', index=False, sep=" ")

    f = open('dataframe_test.csv', 'r')
    a = ['" "']
    lst = []
    for line in f:
        for word in a:
            if word in line:
                line = line.replace(word, '')
        lst.append(line)
    f.close()
    f = open('dataframe_test.csv', 'w')
    for line in lst:
        f.write(line)
    f.close()


def make_input_dir(dir_name_number):
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = data2 = ""

    with open('many.txt') as fp:
        data = fp.read()
    print(data)
    # Reading data from file2
    with open('dataframe_test.csv') as fp:
        data2 = fp.read()

    data += "\n\n"
    data += data2
    charges = "0 1"

    new_dir = "calc_zone/geom" + str(dir_name_number)
    os.mkdir(new_dir)
    with open(new_dir + '/mex.com', 'w') as fp:
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=4\n")
        fp.write("#N wB97XD/6-31G(d) opt=ModRedundant FREQ\n")
        fp.write("\n")
        fp.write("Name ModRedundant\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)

    with open(new_dir + '/mex.pbs', 'w') as fp:
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mex\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem=15gb\n")
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out\n\nrm -r $scrdir\n")

    print("\ngeom" + str(dir_name_number) + "\n")
    os.chdir("calc_zone/geom" + str(dir_name_number))
    os.system("qsub mex.pbs")
    os.chdir("../..")


def make_input_files():
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = data2 = ""

    with open('many.txt') as fp:
        data = fp.read()

    # Reading data from file2
    with open('dataframe_test.csv') as fp:
        data2 = fp.read()

    data += "\n\n"
    data += data2
    charges = "0 1"

    with open('mex.com', 'w') as fp:
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=1\n")
        fp.write("#N wB97XD/6-31G(d) opt=ModRedundant FREQ\n")
        fp.write("\n")
        fp.write("CH2O3 ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)

    with open('mex.pbs', 'w') as fp:
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mex\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem=15gb\n")
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out\n\nrm -r $scrdir\n")


def xyz_remove_whitespace(mol_xyz1, mol_xyz2):
    with open(mol_xyz1) as fp:
        data = fp.read()
    print(data)
    geo1 = geo2 = 0
    return geo1, geo2


def main(molecules_in_cluster, number_clusters, box_length,  minium_distance_between_molecules,
         percent_chance_mol_1, mol_xyz1, mol_xyz2):
    geo1, geo2 = xyz_remove_whitespace(mol_xyz1, mol_xyz2)

    geo1 = genfromtxt(mol_xyz1, delimiter=' ')
    geo2 = genfromtxt(mol_xyz2, delimiter=' ')

    # plus two since starting at 1 and range goes up to second val
    for i in range(1, number_clusters + 1, 1):

        """ Takes array and saves it to file """

        final, mole, spacer, sequence = random_arrangement_2(
            geo1, geo2, i, molecules_in_cluster, percent_chance_mol_1, box_length, minium_distance_between_molecules)

        # print(sequence)

        out_file = "many.txt"

        np.savetxt(out_file, final,
                   fmt="%s")
        """ end """

        clean_many_txt()

        bond_lengths_2(geo1, 'bonds1.txt')
        bond_angles_2(geo1, 'angles1.txt')

        bond_lengths_2(geo2, 'bonds2.txt')
        bond_angles_2(geo2, 'angles2.txt')

        df = constraints_2(mole, spacer, sequence)

        clean_dataframe(df)

        # make_input_files()
        # make_input_dir(i) # uncomment when want directories
        print("\n\n\n next directory \n\n\n")

    os.remove("many.txt")
    os.remove("dataframe_test.csv")
    os.remove("bonds1.txt")
    os.remove("angles1.txt")
    os.remove("bonds2.txt")
    os.remove("angles2.txt")

    # uncomment line 404


# main()
