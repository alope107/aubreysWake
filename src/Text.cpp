#include "bn_string_view.h"
#include "bn_sprite_font.h"
#include "bn_sprite_ptr.h"
#include "wake_geometry.h"
#include "wake_log.h"

namespace wake {
    int string_width(bn::string_view string, bn::sprite_font & font) {
        auto widths = font.character_widths_ref();
        constexpr char STARTING_CHAR = 32;
        int total_width = 0;
        for (const char & c : string) {
            total_width += widths[c - STARTING_CHAR];
        }
        return total_width;
    }

    Rectangle text_bounds(bn::fixed_point center, bn::string_view string, bn::sprite_font & font, int font_height=16) {
        bn::fixed halfWidth = bn::fixed(string_width(string, font)) / 2; // TODO(auberon): Keep in ints for rounding and to use shifts instead of division?
        bn::fixed halfHeight = bn::fixed(font_height) / 2;
        return {
            bn::fixed_point(center.x() - halfWidth, center.y() - halfHeight),
            bn::fixed_point(center.x() + halfWidth, center.y() + halfHeight),
        };
    }
}