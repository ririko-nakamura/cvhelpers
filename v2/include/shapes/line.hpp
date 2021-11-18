#include <shapes/point.hpp>

template <typename T>
class Line
{

    protected:
        Point<T> p1;
        Point<T> p2;

    public:
        Line(Point<T> p1, Point<T> p2);
        Line(Point<T> p1, T k);
        Line(T rou, T theta);
        T y(T x);
        T x(T y);
};