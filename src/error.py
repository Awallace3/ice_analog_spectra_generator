import math


def mean_abs_error():
    # nh3, water, co2
    cam_dp= [
            7.32, 8.48, 9.07, 9.97
            ]
    exp = [
            7.00, 8.99, 8.83, 9.93
            ]
    perc = []
    for i in range(len(cam_dp)):
        t = cam_dp[i]
        e = exp[i]
        val = abs(t - e)/e
        perc.append(val)
    print(perc)

    val = 0
    for i in perc:
        val += i
    print(val/4)
    print((6.3-7.5)/6.3)




if __name__ == "__main__":
    mean_abs_error()
