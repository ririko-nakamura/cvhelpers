#include <line.hpp>

template <typename T> Line<T>::Line(Point<T> p1, Point<T> p2)
{
    this->p1 = p1;
    this->p2 = p2;
}
template <typename T> Line<T>::Line(Point<T> p1, T k)
{
    this->p1 = p1;
    this->p2 = Point<T>(p1.x + 1, p1.y + k);
}
template <typename T> Line<T>::Line(T rou, T theta)
{
    Point<T> p1(rou * math.cos(theta), rou * math.sin(theta));
    //k = -math.tan(np.pi / 2 - params[1]) 
    this->p1 = p1;
    this->p2 = Point(p1.x + 1, p1.y + k);
}
template <typename T> T Line<T>::y(T x)
{
//    if math.fabs(self->p1.x - self->p2.x) <= 1e-6:
//        raise NotAFunctionException("This line has k=0 and all the same y coords")
    double k = (p1.y - p2.y) / (p1.x - p2.x);
    double delta_x = x - p1.x;
    double delta_y = delta_x * k;
    return int(p1.y + delta_y);
}
template <typename T> T Line<T>::x(T y)
{
//    if math.fabs(self->p1.x - self->p2.x) <= 1e-6:
//        raise NotAFunctionException("This line has k=0 and all the same y coords")
    double m = (p1.x - p2.x) / (p1.y - p2.y);
    double delta_y = y - p1.y;
    double delta_x = delta_y * m;
    return int(p1.x + delta_x);
}

// __all__ = ["Line", "Horizon", "NotAFunctionException"]


// class NotAFunctionException(Exception):

//     def __init__(self, arg):
//         self.args = arg


// # All angles are in radians.
// class Line:


//     def step(self, point, step=1):
//         try:
//             k = (self.p1[1] - self.p2[1]) / (self.p1[0] - self.p2[0])
//         except ZeroDivisionError:
//             k = float("inf")
//         if math.isinf(k):
//             return (point[0], point[1] + 1)
//         else:
//             if math.fabs(k) >= 1:
//                 y = point[1] + 1
//                 return (self.x(y), y)
//             else:
//                 x = point[0] + 1
//                 return (x, self.y(x))


//     '''
//     Calculate the point whose distance to input point equals to step
//     on the normal direction
//     '''
//     def vstep(self, point, step=-1):
//         normal_vec = (self.p2[0] - self.p1[0], self.p2[1] - self.p1[1])
//         point2 = (point[0] + normal_vec[0], point[1] + normal_vec[1])
//         normal = Line(Line.TWO_POINTS, (point, point2))
//         return normal.step(point, step)


//     def render(self, img, color=(255, 0, 0)):
//         A = (0, self.y(0))
//         B = (img.shape[1] - 1, self.y(img.shape[1] - 1))
//         if abs(A[1]) > 1e4 or abs(B[1]) > 1e4:
//             return False
//         cv.line(img, A, B, color)
//         return True


//     def renderSeg(self, img, color=(255, 0, 0)):
//         cv.line(img, self.p1, self.p2, color)
//         return


//     def toYAlpha(self, maxX):
//         return(self.y(maxX // 2), -math.atan(self.k))


//     # roi format: p1, p2
//     def pointsInROI(self, roi):
        
//         x_min = int(roi[0])
//         x_max = int(roi[2])
//         y_min = int(roi[1])
//         y_max = int(roi[3])
//         points = []
        
//         try:
//             k = (self.p1[1] - self.p2[1]) / (self.p1[0] - self.p2[0])
//         except ZeroDivisionError:
//             k = float("inf")
//         if math.isinf(k):
//             x = self.p1[0]
//             if x >= x_min and x < x_max:
//                 for y in range(y_min, y_max):
//                     points.append((x, y))

//         try:
//             m = 1 / k
//         except ZeroDivisionError:
//             m = float("inf")
//         if math.isinf(m):
//             y = self.p1[1]
//             if y >= y_min and y < y_max:
//                 for x in range(x_min, x_max):
//                     points.append((x, y))
        
//         if math.fabs(k) >= 1:
//             for y in range(y_min, y_max):
//                 x = self.x(y)
//                 if x >= x_min and x < x_max:
//                     points.append((x, y))
//         else:
//             for x in range(x_min, x_max):
//                 y = self.y(x)
//                 if y >= y_min and y < y_max:
//                     points.append((x, y))
        
//         return points

// if __name__ == "__main__":

//     TEST_POINTSROI = True
//     TEST_RENDER = False
    
//     if TEST_POINTSROI:
//         l1 = Line(Line.ROU_THETA, ((200 + 300 * math.tan(np.pi / 6)) * math.cos(np.pi / 6), np.pi / 3))
//         points = l1.pointsInROI([0, 0, 640, 480])
//         l2 = Line(Line.TWO_POINTS, [(-1, 0), (1, 0)])
//         points = l2.pointsInROI([0, 0, 640, 480])
//         l3 = Line(Line.TWO_POINTS, [(0, 10000), (1, 10000)])
//         points = l3.pointsInROI([0, 0, 640, 480])
//         l4 = Line(Line.TWO_POINTS, [(50, 0), (0, 50)])
//         points = l4.pointsInROI([0, 0, 640, 480])

//     if TEST_RENDER:
//         l1 = Line(Line.ROU_THETA, ((200 + 300 * math.tan(np.pi / 6)) * math.cos(np.pi / 6), np.pi / 3))
//         l2 = Line(Line.POINT_K, ((300, 200), 0.5))
//         # SMD Annotation
//         l3 = Line(Line.POINT_K, ((300, 200), math.tan(np.pi / 6)))    
//         img = np.zeros((400, 600, 3), np.uint8)
//         l1.render(img)
//         l2.render(img)
//         l3.render(img)
//         cv.imshow("debug", img)
//         cv.waitKey()