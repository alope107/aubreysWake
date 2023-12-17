#ifndef WAKEGEOM
#define WAKEGEOM

#include "bn_fixed_point.h"

namespace wake {
    struct Rectangle {
        bn::fixed_point top_left;
        bn::fixed_point bottom_right;
    };

    template <typename T>
    inline bool point_in_rect(T x, T y, T left, T right, T top, T bottom) {
        bool in = x >= left && x <= right && y >= top && y <= bottom;
        return in;
    }

    inline bool point_in_rect(bn::fixed_point point, 
                              bn::fixed_point top_left,
                              bn::fixed_point bottom_right) {
        return point_in_rect(point.x(), point.y(), top_left.x(), bottom_right.x(), top_left.y(), bottom_right.y());
    };

    inline bool point_in_rect(bn::fixed_point point, Rectangle rect) {
        return point_in_rect(point.x(), point.y(), rect.top_left.x(), rect.bottom_right.x(), rect.top_left.y(), rect.bottom_right.y());
    }
}

#endif // WAKEGEOM