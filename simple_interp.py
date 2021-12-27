import numpy as np
import linecache
import shutil

JOINT_NUM = 21
JOINT_POS_DIM = 3

DIR_IN = "input_data/test/"
DIR_OUT = "output_data/"


def calc_catmull_rom_spline(v_minus1, v0, v1, v2, t):
    c = (v1 - v_minus1) / 2.
    a = (v2 - v0) / 2. - 2. * (v1 - v0) + c
    b = 3. * (v1 - v0) - (v2 - v0) / 2. - 2. * c

    return v0 + ((((a * t) + b) * t) + c) * t


def calc_linear(v0, v1, t):
    return v0 + (v1 - v0) * t


def load_data(fname):
    header = linecache.getline(fname, 1)

    temp = np.genfromtxt(fname, delimiter=",", skip_header=1)

    motion_id_list = temp[:, 0].astype(np.int64).tolist()
    frame_id_list = temp[:, 1].astype(np.int64).tolist()
    pos_list = np.reshape(temp[:, 2:], (-1, JOINT_NUM, JOINT_POS_DIM))

    return header, motion_id_list, frame_id_list, pos_list


def save_data(fname, header, motion_id_list, frame_id_list, pos_list):
    with open(fname, "w") as f:
        f.write(header)

        for motion_id, frame_id, pos in zip(motion_id_list, frame_id_list, pos_list):
            f.write("%03d," % motion_id)
            f.write("%d," % frame_id)
            f.write(",".join(map(str, pos.flatten())))
            f.write("\n")

    return


def interp_pos(pos_list, skip_frames, method):
    loop = len(pos_list) // skip_frames

    for i in range(loop):
        for j in range(JOINT_NUM):
            v0 = pos_list[i * skip_frames][j]
            v1 = pos_list[(i + 1) * skip_frames][j]

            if i == 0:
                v_minus1 = pos_list[0][j]
            else:
                v_minus1 = pos_list[(i - 1) * skip_frames][j]

            if i >= loop - 2:
                v2 = pos_list[(i + 1) * skip_frames][j]
            else:
                v2 = pos_list[(i + 2) * skip_frames][j]

            for k in range(1, skip_frames):
                t = k / skip_frames

                if method == "catmull_rom_spline":
                    pos_list[i * skip_frames + k][j] = calc_catmull_rom_spline(v_minus1, v0, v1, v2, t)
                else:
                    pos_list[i * skip_frames + k][j] = calc_linear(v0, v1, t)

    return pos_list


def main():
    method_list = ["linear", "catmull_rom_spline"]

    job_list = [
        {"fname": "test_easy.csv", "skip_frames": 5},
        {"fname": "test_normal.csv", "skip_frames": 15},
        {"fname": "test_hard.csv", "skip_frames": 45},
    ]

    for method in method_list:
        for job in job_list:
            header, motion_id_list, frame_id_list, pos_list = load_data("%s%s" % (DIR_IN, job["fname"]))

            ptr_start = 0
            for i, motion_id in enumerate(motion_id_list):
                if i == len(motion_id_list) - 1 or motion_id != motion_id_list[i + 1]:
                    interp_pos_list = interp_pos(pos_list[ptr_start:i + 1].copy(), job["skip_frames"], method)
                    pos_list[ptr_start:i + 1] = interp_pos_list
                    ptr_start = i + 1

            save_data("%s%s/%s" % (DIR_OUT, method, job["fname"]), header, motion_id_list, frame_id_list, pos_list)

        shutil.make_archive("%s%s" % (DIR_OUT, method), "zip", root_dir="%s%s" % (DIR_OUT, method))

    return


if __name__ == '__main__':
    main()
