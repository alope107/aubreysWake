#ifndef WAKEWALKER
#define WAKEWALKER
#include "wake_updater.h"
#include "bn_sprite_ptr.h"

namespace wake {
    class Walker : public IUpdatable {
        bn::sprite_ptr& spr;
        int step_size;
        public:
            Walker(bn::sprite_ptr& spr, int step_size_arg);
            void update();
            bn::fixed_point position();
    };
}

#endif //WAKEWALKER