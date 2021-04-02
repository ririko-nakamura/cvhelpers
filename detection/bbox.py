class BBox:

    def __init__(self, det = (), xywh = True):
        if len(det) == 4:
            self.min_x = det[0]
            self.min_y = det[1]
            if xywh:
                self.w = det[2]
                self.h = det[3]   
                self.max_x = det[0] + det[2]
                self.max_y = det[1] + det[3]
            else:
                self.w = det[2] - det[0]
                self.h = det[3] - det[1]
                self.max_x = det[2]
                self.max_y = det[3]             
        else:
            self.max_x = -1
            self.min_x = 65535
            self.max_y = -1
            self.min_y = 65535
            self.w = -1
            self.h = -1

    def area(self):
        return self.w * self.h

    def __str__(self):
        return "[x1={}, y1={}, x2={}, y2={}, w={}, h={}]".format(self.min_x, self.min_y, self.max_x, self.max_y, self.w, self.h)


def intersect(a, b):
    min_x = max(a.min_x, b.min_x)
    max_x = min(a.max_x, b.max_x)
    min_y = max(a.min_y, b.min_y)
    max_y = min(a.max_y, b.max_y)
    w = max_x - min_x
    h = max_y - min_y
    if w <= 0 or h <= 0:
        return None
    else:
        return BBox((min_x, min_y, w, h))

def union(a, b):
    min_x = min(a.min_x, b.min_x)
    max_x = max(a.max_x, b.max_x)
    min_y = min(a.min_y, b.min_y)
    max_y = max(a.max_y, b.max_y)
    w = max_x - min_x
    h = max_y - min_y
    if w <= 0 or h <= 0:
        return None
    else:
        return BBox((min_x, min_y, w, h))

def IoU(a, b):
    c = intersect(a, b)
    if c is not None:
        return c.area() / (a.area() + b.area() - c.area())
    else:
        return 0
