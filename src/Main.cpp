/*
Adapted from Butano audio example
*/
#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_bg_palettes.h"
#include "bn_sound_actions.h"
#include "bn_sprite_text_generator.h"

#include "bn_sound_items.h"

#include "common_info.h"
#include "common_variable_8x16_sprite_font.h"

namespace
{
    void sound_scene(bn::sprite_text_generator& text_generator)
    {
        constexpr bn::string_view info_text_lines[] = {
            "riverrun, past Eve and Adam's",
            "from swerve of shore to bend of bay",
            "brings us by",
            "a commodius vicus of recirculation",
            "back to Howth Castle and Environs",
        };

        common::info info("", info_text_lines, text_generator);
        info.set_show_always(true);

        while(! bn::keypad::start_pressed())
        {
            if(bn::keypad::a_pressed())
            {
                bn::sound_items::riverrun_demo.play(1);
            }

            info.update();
            bn::core::update();
        }
    }
}

int main()
{
    bn::core::init();

    bn::sprite_text_generator text_generator(common::variable_8x16_sprite_font);
    bn::bg_palettes::set_transparent_color(bn::color(16, 16, 16));

    while(! bn::keypad::start_pressed())
    {
        sound_scene(text_generator);
        bn::core::update();
    }
}