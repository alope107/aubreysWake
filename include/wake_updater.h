#ifndef WAKEUPDATER
#define WAKEUPDATER

#include "bn_vector.h"
#include "wake_log.h"

namespace wake {
    class IUpdatable {
        public:
            virtual void update() = 0;
    };

    template<int Size>
    class Updater {
        static_assert(Size > 0);
        public:
            void update();
            void add(IUpdatable& updatable);
        protected:
            bn::vector<IUpdatable*, Size> updatables;
    };

    class SillyUpdatable: public IUpdatable {
        public:
            void update();
    };
}

#include "Updater.tpp"
#endif //WAKEUPDATER