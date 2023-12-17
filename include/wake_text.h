#ifndef WAKETEXT
#define WAKETEXT

#include "bn_string_view.h"
#include "bn_sprite_font.h"
#include "bn_sprite_ptr.h"
#include "wake_geometry.h"


namespace wake {
    int string_width(bn::string_view string, bn::sprite_font & font);
    Rectangle text_bounds(bn::fixed_point center, bn::string_view string, bn::sprite_font & font, int font_height=16);
}

#endif // WAKETEXT