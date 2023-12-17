#include "wake_walker.h"
#include "bn_sprite_ptr.h"
#include "bn_keypad.h"
#include "bn_fixed_point.h"

namespace wake {
    Walker::Walker(bn::sprite_ptr& spr_arg, int step_size_arg = 1) : 
        spr(spr_arg), step_size(step_size_arg) {};
    
    void Walker::update() {
        if (bn::keypad::left_held()) {
            spr.set_x(spr.x() - step_size);
        }
        if (bn::keypad::right_held()) {
            spr.set_x(spr.x() + step_size);
        }
        if (bn::keypad::up_held()) {
            spr.set_y(spr.y() - step_size);
        }
        if (bn::keypad::down_held()) {
            spr.set_y(spr.y() + step_size);
        }
    }

    bn::fixed_point Walker::position() {
        return spr.position();
    }
}