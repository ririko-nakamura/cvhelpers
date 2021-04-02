import math

import cv2 as cv
import numpy as np


# All angles are in radians.
class Line:


    # Types of line annotations
    TWO_POINTS = 0
    # OpenCV HoughLines output format
    ROU_THETA = 1
    # Any point on the line and the line's slope value
    POINT_K = 2


    def __init__(self, annoType, params):
        assert annoType <= Horizon.POINT_K and annoType >= 0, "Invalid annotation type"
        if annoType == Horizon.TWO_POINTS:
            self.p1 = params[0]
            self.p2 = params[1]
        else:
            if annoType == Horizon.ROU_THETA:
                point = (params[0] * math.cos(params[1]), params[0] * math.sin(params[1]))
                k = -math.tan(np.pi / 2 - params[1])   
            elif annoType == Horizon.POINT_K:
                point = params[0]
                k = params[1]
            self.p1 = point
            self.p2 = (point[0]+1, point[1]+k)


    def y(self, x):
        assert(math.fabs(self.p1[0] - self.p2[0]) >= 1e-6)
        k = (self.p1[1] - self.p2[1]) / (self.p1[0] - self.p2[0])
        delta_x = x - self.p1[0]
        delta_y = delta_x * k
        return int(self.p1[1] + delta_y)


    def x(self, y):
        assert(math.fabs(self.p1[1] - self.p2[1]) >= 1e-6)
        m = (self.p1[0] - self.p2[0]) / (self.p1[1] - self.p2[1])
        delta_y = y - self.p1[1]
        delta_x = delta_y * m
        return int(self.p1[0] + delta_x)


    def step(self, point, step=1):
        try:
            k = (self.p1[1] - self.p2[1]) / (self.p1[0] - self.p2[0])
        except ZeroDivisionError:
            k = float("inf")
        if math.isinf(k):
            return (point[0], point[1] + 1)
        else:
            if math.fabs(k) >= 1:
                y = point[1] + 1
                return (self.x(y), y)
            else:
                x = point[0] + 1
                return (x, self.y(x))


    def render(self, img, color=(255, 0, 0)):
        A = (0, self.y(0))
        B = (img.shape[1] - 1, self.y(img.shape[1] - 1))
        if abs(A[1]) > 1e4 or abs(B[1]) > 1e4:
            return False
        cv.line(img, A, B, color)
        return True


    def renderSeg(self, img, color=(255, 0, 0)):
        cv.line(img, self.p1, self.p2, color)
        return


    def toYAlpha(self, maxX):
        return(self.y(maxX // 2), -math.atan(self.k))


    # roi format: p1, p2
    def pointsInROI(self, roi):
        
        x_min = int(roi[0])
        x_max = int(roi[2])
        y_min = int(roi[1])
        y_max = int(roi[3])
        points = []
        
        try:
            k = (self.p1[1] - self.p2[1]) / (self.p1[0] - self.p2[0])
        except ZeroDivisionError:
            k = float("inf")
        if math.isinf(k):
            x = self.p1[0]
            if x >= x_min and x < x_max:
                for y in range(y_min, y_max):
                    points.append((x, y))

        try:
            m = 1 / k
        except ZeroDivisionError:
            m = float("inf")
        if math.isinf(m):
            y = self.p1[1]
            if y >= y_min and y < y_max:
                for x in range(x_min, x_max):
                    points.append((x, y))
        
        if math.fabs(k) >= 1:
            for y in range(y_min, y_max):
                x = self.x(y)
                if x >= x_min and x < x_max:
                    points.append((x, y))
        else:
            for x in range(x_min, x_max):
                y = self.y(x)
                if y >= y_min and y < y_max:
                    points.append((x, y))
        
        return points



class Horizon(Line):


    def __init__(self, annoType, params):
        super().__init__(annoType, params)   


    def checkSuppress(self, det):
        Ay = self.y(det.min_x)
        if Ay >= det.min_y and Ay <= det.max_y:
            return False
        By = self.y(det.max_x)
        if By >= det.min_y and By <= det.max_y:
            return False
        return True



if __name__ == "__main__":

    TEST_POINTSROI = True
    TEST_RENDER = False
    
    if TEST_POINTSROI:
        l1 = Line(Line.ROU_THETA, ((200 + 300 * math.tan(np.pi / 6)) * math.cos(np.pi / 6), np.pi / 3))
        points = l1.pointsInROI([0, 0, 640, 480])
        l2 = Line(Line.TWO_POINTS, [(-1, 0), (1, 0)])
        points = l2.pointsInROI([0, 0, 640, 480])
        l3 = Line(Line.TWO_POINTS, [(0, 10000), (1, 10000)])
        points = l3.pointsInROI([0, 0, 640, 480])
        l4 = Line(Line.TWO_POINTS, [(50, 0), (0, 50)])
        points = l4.pointsInROI([0, 0, 640, 480])

    if TEST_RENDER:
        l1 = Line(Line.ROU_THETA, ((200 + 300 * math.tan(np.pi / 6)) * math.cos(np.pi / 6), np.pi / 3))
        l2 = Line(Line.POINT_K, ((300, 200), 0.5))
        # SMD Annotation
        l3 = Line(Line.POINT_K, ((300, 200), math.tan(np.pi / 6)))    
        img = np.zeros((400, 600, 3), np.uint8)
        l1.render(img)
        l2.render(img)
        l3.render(img)
        cv.imshow("debug", img)
        cv.waitKey()