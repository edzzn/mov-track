import time
from collections import deque


class RegisteredObject():
    def __init__(self, x, y, w, h, object_type, last_record_time=time.localtime()):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.object_type = object_type
        self.last_record_time = last_record_time
        self.path = deque([])

    def __str__(self):
        return f"{self.object_type}: [{self.x},{self.y}], {self.last_record_time}, path:{self.path}"

    def add_step_to_path(self, x, y):
        PATH_SIZE = 100
        if len(self.path) > PATH_SIZE:
            self.path.pop()

        self.path.appendleft((x, y))

    def _equals(self, other_record):

        TOLERANCE_X = 30
        TOLERANCE_Y = 30
        TOLERANCE_W = 20
        TOLERANCE_H = 20

        delta_x = abs(self.x - other_record.x)
        delta_y = abs(self.y - other_record.y)
        delta_w = abs(self.w - other_record.w)
        delta_h = abs(self.h - other_record.h)

        return (
            delta_x < TOLERANCE_X and
            delta_y < TOLERANCE_Y and
            delta_h < TOLERANCE_H and
            delta_w < TOLERANCE_W
        )


class ObjectsRecord():
    def __init__(self):
        self.objects = []
        self.ignored_objects = []

    def _remove_similar_objects(self):
        objects_to_keep = []
        for object_i in self.objects:
            should_keep = True
            for saved_object in objects_to_keep:
                if object_i._equals(saved_object):
                    should_keep = False
                    break

            if should_keep:
                objects_to_keep.append(object_i)

        self.objects = objects_to_keep

    def _add_path_to_objects(self, objects_from_last_frame):
        for object in self.objects:
            for old_object in objects_from_last_frame:
                if(object._equals(old_object)):
                    object.path = old_object.path
                    object.add_step_to_path(old_object.x, old_object.y)

    def add_all(self, records):
        objects_from_last_frame = self.objects[:]
        self.objects = records
        self.ignored_objects = []

        self._remove_similar_objects()
        self._add_path_to_objects(objects_from_last_frame)

    def __str__(self):
        if len(self.objects) <= 3 and len(self.objects) > 0:
            return f"""
              {str(object) for object in self.objects}
          """
        return f"ObjectsRecorded: {len(self.objects)}"
