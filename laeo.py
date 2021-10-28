from math import sin, cos
import numpy as np

def project_ypr_in2d(yaw, pitch, roll):
    """ Project yaw pitch roll on image plane. Result is NOT normalised.

    :param yaw:
    :param pitch:
    :param roll:
    :return:
    """
    pitch = pitch * np.pi / 180
    yaw = -(yaw * np.pi / 180)
    roll = roll * np.pi / 180

    x3 = (sin(yaw))
    y3 = (-cos(yaw) * sin(pitch))

    # normalize the components
    length = np.sqrt(x3 ** 2 + y3 ** 2)

    # return [x3 / length, y3 / length]
    return [x3, y3]


def uncertainty_to_deg(uncertainty):
    return np.mean(uncertainty)


def compute_interaction_cosine(head_position, gaze_direction, uncertainty, target, visual_cone=True):
    """Computes the interaction between two people using the angle of view.

    The interaction in measured as the cosine of the angle formed by the line from person A to B
    and the gaze direction of person A.
    Reference system of zero degree:


    :param head_position: position of the head of person A
    :param gaze_direction: gaze direction of the head of person A
    :param target: position of head of person B
    :param uncertainty: in degree ?
    :param visual_cone: (default) True, if False gaze is a line, otherwise it is a cone (more like humans)
    :return: float or double describing the quantity of interaction
    """
    if np.array_equal(head_position, target):
        return 0  # or -1
    else:
        cone_aperture = uncertainty_to_deg(uncertainty)
        # if 0 <= uncertainty < 0.4:
        #     cone_aperture = np.deg2rad(3)
        # elif 0.4 <= uncertainty <= 0.6:
        #     cone_aperture = np.deg2rad(6)
        # elif 0.6 < uncertainty <= 1:
        #     cone_aperture = np.deg2rad(9)
        # direction from observer to target
        # plane xy
        _direction_xy_ = np.arctan2((target[1] - head_position[1]), (target[0] - head_position[0]))
        _direction_gaze_xy_ = np.arctan2(gaze_direction[1], gaze_direction[0])
        difference_xy = _direction_xy_ - _direction_gaze_xy_  # radians

        if visual_cone and (0 < difference_xy < cone_aperture):
            difference_xy = 0
        # difference of the line joining observer -> target with the gazing direction,

        # other plane zx
        _direction_zx_ = np.arctan2((target[2] - head_position[2]), (target[0] - head_position[0]))
        _direction_gaze_zx_ = np.arctan2(gaze_direction[2], gaze_direction[0])
        difference_zx = _direction_zx_ - _direction_gaze_zx_  # radians


        if visual_cone and (0 < difference_zx < cone_aperture): # probably better to leave more freedom
            difference_zx = 0



        val = (np.cos(difference_xy) + np.cos(difference_zx))/2
        if val < 0:
            return 0
        else:
            return val


def calculate_uncertainty(yaw_1, pitch_1, roll_1, clipping_value, clip=True):
    # res_1 = abs((pitch_1 + yaw_1 + roll_1) / 3)
    res_1 = abs((pitch_1 + yaw_1) / 2)
    if clip:
        # it binarize the uncertainty
        if res_1 > clipping_value:
            res_1 = clipping_value
        else:
            res_1 = 0
    else:
        # it leaves uncertainty untouched except for upper bound
        if res_1 > clipping_value:
            res_1 = clipping_value
        elif res_1 < 0:
            res_1 = 0

    # normalize
    res_1 = res_1 / clipping_value
    # assert res_1 in [0, 1], 'uncertainty not binarized'
    return res_1