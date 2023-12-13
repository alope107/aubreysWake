# ifndef WAKELOG
# define WAKELOG

#include "bn_log.h"
#include "bn_string.h"

namespace wake {
    template<int maxSize=10000, typename... Types>
    inline void log(const Types&... vals) {
        bn::string<maxSize> message = "";
        (message += ... += (bn::to_string<maxSize>(vals) + bn::to_string<1>(" ")));
        bn::log(message);
    }
}
# endif // WAKELOG