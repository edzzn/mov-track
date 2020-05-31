import time


class RegisteredObject():
    def __init__(self, x, y, w, h, object_type, last_record_time=time.localtime()):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.object_type = object_type
        self.last_record_time = last_record_time

    def __str__(self):
        return f"{self.object_type}: [{self.x},{self.y}], {self.last_record_time}"


class ObjectsRecord():
    def __init__(self):
        self.objects = []
        self.ignored_objects = []
        self.tolerance_x = 10
        self.tolerance_y = 10
        self.tolerance_width = 20
        self.tolerance_height = 20

    def _remove_similar_objects(self):
        index_objects_to_ignore = set()
        index_objects_to_keep = set()
        for i, object_i in enumerate(self.objects):
            for j, object_j in enumerate(self.objects):
                if j > i:
                    delta_x = abs(object_i.x - object_j.x)
                    delta_y = abs(object_i.y - object_j.y)
                    delta_w = abs(object_i.w - object_j.w)
                    delta_h = abs(object_i.h - object_j.h)

                    if (
                        delta_x < self.tolerance_x and
                        delta_y < self.tolerance_y and
                        delta_h < self.tolerance_height and
                        delta_w < self.tolerance_width
                    ):
                        index_objects_to_ignore.add(j)
                        index_objects_to_keep.add(i)
                        break

        objects_to_keep = []
        for i in range(len(self.objects)):
            if (i in index_objects_to_keep):
                objects_to_keep.append(self.objects[i])
        self.objects = objects_to_keep

        # ? Bellow code is present for debugging
        # objects_to_ignore = []
        # for i in range(len(self.objects)):
        #     if (i in index_objects_to_ignore):
        #         objects_to_ignore.append(self.objects[i])
        # self.ignored_objects = objects_to_ignore

    def add_all(self, records):
        all_objects = self.objects[:]
        self.objects = records
        self.ignored_objects = []

        self._remove_similar_objects()

    def __str__(self):
        return f"ObjectsRecorded: {len(self.objects)}"
