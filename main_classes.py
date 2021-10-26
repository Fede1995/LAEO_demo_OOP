"""


"""
import pandas as pd
from pathlib import Path


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

    def project_on_2D(self):
        pass

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

    def __repr__(self):
        return f'3D vector yaw={self.yaw}, pitch={self.yaw}, roll={self.yaw}'

    def __eq__(self, other):
        return self.yaw==other.yaw and self.pitch==other.pitch and self.roll==other.roll


class Position_3D:
    def __init__(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z


class Video:
    frame_counter = 0  # the creation of the first frame takes frame

    def __init__(self):
        self.saving_folder = Path('')
        self.history_of_people = self.HistoryPeople(self)
        self.initialise_tracker()  # don't know exactly

    def initialise_tracker(self):
        self.tracker = Video.Tracker()
        pass

    def acquire_frame(self):
        self.frame = self.Frame(self)
        return self.frame

    def save_history_current_frame(self):
        pass



    class Tracker:
        def __init__(self):
            pass

        def update_tracker(self):
            people_list = None
            return people_list

    class HistoryPeople:
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
        class Person:
            _counter = 0

            def __init__(self, yaw, pitxh, roll, tx, ty, tz=0):
                Video.Frame.Person._counter += 1
                self.id = Video.Frame.Person._counter
                self.gaze = Vector_3D(yaw, pitxh, roll)
                self.position = Position_3D(tx, ty, tz)

            def assign_id(self, new_id):
                self.id = new_id

            def __repr__(self):
                return f'Person id={id}'

            def __eq__(self, other):
                return self.id==other.id

        class FrameObserver:
            def __init__(self,frame_instance):
                self.people = []  # list of obj of type Person
                self.interaction = None
                self.laeo = None
                self.frame_instance=frame_instance
                # self.frame_number = frame_number

            def instantiate_people(self):
                pass

            def add_person(self, new_person):
                # if tracker says it was a person already present, update id
                if True:
                    print(f'to implement!!!')
                # check person is unique in frame
                if new_person not in self.people:
                    self.people.append(new_person)

            def create_matrix(self):
                index = [p.id for p in self.people]
                matrix = pd.DataFrame(data=None, index=index, columns=index, dtype=float)
                # matrix.at[0,0] get value at location [raw, coloumn], matrix.loc[5].at['B']
            def compute_interactions(self):
                pass
            def compute_laeo(self):
                pass
            def save_interactions(self):
                pass
        # start of the frame class
        def __init__(self, video_instance):
            self.video_instance = video_instance
            self.frame_number = Video.frame_counter
            Video.frame_counter += 1
            self.observer = self.FrameObserver(self)

        def pose_estimator(self):
            pass

        def update_tracker(self):
            self.people_list = self.video_instance.tracker.update_tracker()


        def __repr__(self):
            return f'Frame number={self.frame_number}'

        def __eq__(self, other):
            return self.frame_number==other.frame_number


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