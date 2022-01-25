"""


"""
import pandas as pd
from pathlib import Path

from math import sin, cos
import numpy as np

import json_loader
import laeo

from collections.abc import Sequence


class Vector_3D:  # or gaze_vector
    def __init__(self, yaw=None, pitch=None, roll=None):
        """Create a gaze vector.

        Extended description

        Parameters
        ----------
        yaw : array_like
            A list of two float values [yaw, yaw_uncertainty].
        pitch : array_like
            A list of two float values [pitch, pitch_uncertainty].
        roll : array_like
            A list of two float values [roll, roll_uncertainty].
        """
        if roll is None:
            roll = [0.0, 6.0]
        if pitch is None:
            pitch = [0.0, 6.0]
        if yaw is None:
            yaw = [0.0, 6.0]
        self.yaw, self.yaw_u = yaw
        self.pitch, self.pitch_u = pitch
        self.roll, self.roll_u = roll
        # if the uncertainty is not used and let to zero, set to a pre-defined value
        if int(self.yaw_u)==int(self.pitch_u)==int(self.roll_u)==0:
            self.__uncertainty_setter()

    def __getitem__(self, i):
        if i==0:
            return self.yaw
        if i==1:
            return self.pitch
        if i==2:
            return self.roll
        else:
            raise IndexError

    def __len__(self):
        return int(3)

    def project_on_2D(self):
        """ Project yaw pitch roll on image plane. Result is NOT normalised.

        :param yaw:
        :param pitch:
        :param roll:
        :return:
        """
        pitch = self.pitch * np.pi / 180
        yaw = -(self.yaw * np.pi / 180)
        roll = self.roll * np.pi / 180

        x3 = (sin(yaw))
        y3 = (-cos(yaw) * sin(pitch))

        # normalize the components
        length = np.sqrt(x3**2 + y3**2)

        # return [x3 / length, y3 / length]
        return [x3, y3]

    def __uncertainty_setter(self, value=6.0):
        """It set the uncertainty when it is not provided at initialisation.

        The function set the uncertainty in case it is not provided by the previous
        step. It helps managing case where uncertainty is not used, but however need
        to be set at a minimum level of degree, otherwise the gaze is just a directed
        line with no cone of view (very restrictive hypothesis).

        Parameters
        ----------
        value : float
            The value we want to set the angle of the cone of view.
        """
        self.yaw_u = value
        self.pitch_u = value
        self.roll_u = value

    def get_uncertainty(self):
        return self.yaw_u, self.pitch_u, self.roll_u

    def get_vector_components(self):
        return self.yaw, self.pitch, self.roll

    def __repr__(self):
        return f'3D vector yaw={self.yaw}, pitch={self.yaw}, roll={self.yaw}'

    def __eq__(self, other):
        return self.yaw==other.yaw and self.pitch==other.pitch and self.roll==other.roll


class Position_3D(Sequence):
    def __init__(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z

    def __getitem__(self, i):
        if i==0:
            return self.x
        if i==1:
            return self.y
        if i==2:
            return self.z
        else:
            raise IndexError

    def __len__(self):
        if self.z==0:
            return int(2)
        else:
            return int(3)

    def __repr__(self):
        return f'3D position x={self.x}, y={self.y}, z={self.z}'


class Video:
    frame_counter = 0  # the creation of the first frame takes frame

    def __init__(self):
        self.saving_folder = Path('')
        self.history_of_people = self.HistoryPeople(self)
        self.initialise_tracker()  # don't know exactly

    def start_analysis(self, video_path):
        # video_path is a folder with json for each person
        for frame in sorted(video_path.iterdir()):
            self.acquire_frame(frame)

    def initialise_tracker(self):
        self.tracker = Video.Tracker()
        pass

    def acquire_frame(self, file):
        if file.is_file():
            data = json_loader.load_data(file)
            self.frame = self.Frame(self, data)
        else:
            raise FileNotFoundError('.json file for this frame does not exist')

    class Tracker:
        def __init__(self):
            pass

        def update_tracker(self):
            self.people_list = None
            return self.people_list

        def person_is_new(self):
            return True

    class HistoryPeople:  # TODO implement
        def __init__(self, video_instance):
            self.video_instance = video_instance
            self.people_history = {}

        def add_person(self, id):
            self.people_history[id] = []
            if Video.frame_counter!=0:  # if it is not the first frame, add None at the beginning
                counter = Video.frame_counter
                while counter >= 0:
                    self.add_history_frame(id, None)
                    counter -= 1

        def add_history_frame(self, id, value):
            self.people_history[id].append(value)

        def save_history(self):
            destination_path = self.video_instance.saving_folder

    class Frame:
        # start of the frame class
        def __init__(self, video_instance, data):
            self.video_instance = video_instance
            self.frame_number = Video.frame_counter
            Video.frame_counter += 1
            self.people = []  # list of obj of type Person
            self.initialise_frame(data)
            self.observer = self.FrameObserver(self)  # you should have all people fixed to call it

        def initialise_frame(self, data):
            self.pose_estimator()
            self.instantiate_people(data)

        def instantiate_people(self, data):
            for p in data['people']:
                x, y, z = None, None, None
                if len(p['center_xy'])==2:
                    x, y = p['center_xy'][0], p['center_xy'][1]
                    z = 0
                elif len(p['center_xy'])==3:
                    x, y, z = p['center_xy'][0], p['center_xy'][1], p['center_xy'][2]
                new_person = Video.Frame.Person(p['id_person'][0][0], [p['yaw'][0], p['yaw_u'][0]],
                                                [p['pitch'][0], p['pitch_u'][0]],
                                                [p['roll'][0], p['roll_u'][0]], x, y, z)
                self.people.append(new_person)
            pass

        def add_person(self, new_person):

            if self.video_instance.tracker.person_is_new():
                if new_person not in self.people:  # check person is unique in frame
                    self.people.append(new_person)
            else:  # if tracker says it was a person already present, update id
                print(f'to implement!!!')

        def pose_estimator(self):
            pass

        def update_tracker(self):
            self.people_list = self.video_instance.tracker.update_tracker()

        def __repr__(self):
            return f'Frame number={self.frame_number}'

        def __eq__(self, other):
            return self.frame_number==other.frame_number

        class Person:
            _counter = 0

            def __init__(self, person_id, yaw, pitch, roll, tx, ty, tz=0):
                Video.Frame.Person._counter += 1
                self.id = Video.Frame.Person._counter
                self.position = Position_3D(tx, ty, tz)
                self.gaze = Vector_3D(yaw, pitch, roll)
                self.assign_id(person_id)
                if tz==0:  # we are in 2D
                    self.gaze.project_on_2D()

            def assign_id(self, new_id):
                self.id = new_id

            def __repr__(self):
                return f'Person id={self.id}'

            def __eq__(self, other):
                return self.id==other.id

        class FrameObserver:
            def __init__(self, frame_instance):

                self.interaction = None
                self.laeo = None
                self.frame_instance = frame_instance
                self.analyse_frame()
                # self.frame_number = frame_number

            def analyse_frame(self):
                self.create_matrices()
                self.compute_interactions()
                self.compute_laeo()

            def create_matrices(self):
                index = [p.id for p in self.frame_instance.people]
                self.interaction_matrix = pd.DataFrame(data=None, index=index, columns=index, dtype=float)
                self.laeo_matrix = pd.DataFrame(data=None, index=index, columns=index, dtype=float)
                # self.bool_matrix = pd.DataFrame(data=None, index=index, columns=index, dtype=float)
                # matrix.at[0,0] get value at location [raw, coloumn], matrix.loc[5].at['B']

            def compute_interactions(self):
                for subject in self.frame_instance.people:
                    for object in self.frame_instance.people:
                        a, b, c = subject.gaze.get_uncertainty()
                        # TODO clipping value to modify
                        uncertainty = laeo.calculate_uncertainty(a, b, c, clipping_value=10)
                        self.interaction_matrix.at[subject.id, object.id] = laeo.compute_interaction_cosine(
                                subject.position, subject.gaze, uncertainty, object.position)

            def compute_laeo(self):
                for subject in self.frame_instance.people:
                    for object in self.frame_instance.people:
                        if np.allclose(self.interaction_matrix.at[subject.id, object.id],0) or np.allclose(self.interaction_matrix.at[object.id, subject.id],0):
                            self.laeo_matrix.at[subject.id, object.id] = 0
                        else:
                            self.laeo_matrix.at[subject.id, object.id] = (self.interaction_matrix.at[
                                                                              subject.id, object.id] +
                                                                          self.interaction_matrix.at[
                                                                              object.id, subject.id]) / 2


            def save_interactions(self, path: Path):
                if path.is_dir():
                    destination = path / 'LAEO' / (str(self.frame_instance.frame_number) + '.csv')
                    self.laeo_matrix.to_csv(destination, sep=',', float_format='%.2f')
                    destination = path / 'Interactions' / (str(self.frame_instance.frame_number) + '.csv')
                    self.interaction_matrix.to_csv(destination, sep=',', float_format='%.2f')


class LAEO_matrix:
    def __init__(self):
        pass


if __name__=='__main__':
    current_video = Video()
    # per each frame
    current_frame = current_video.acquire_frame()
    current_frame.pose_estimator()
    people_list = current_frame.update_tracker()
    current_frame.observer.instantiate_people()
    current_frame.observer.compute_interactions()
    current_frame.observer.compute_laeo()
    current_frame.observer.save_interactions()
    current_video.save_history_current_frame()