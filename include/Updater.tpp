#include "wake_log.h"
#include "wake_updater.h"

namespace wake {
    template<int Size>
    void wake::Updater<Size>::update() {
        for (auto updatable : updatables) {
            updatable->update();
        }
    }
    
    template<int Size>
    void wake::Updater<Size>::add(IUpdatable& updatable) {
        updatables.push_back(&updatable);
    }
}