/*
Adapted from Butano audio example
*/
#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_bg_palettes.h"
#include "bn_sound_actions.h"
#include "bn_sprite_text_generator.h"
#include "bn_string.h"

#include "bn_sound_items.h"

#include "common_info.h"
#include "common_variable_8x16_sprite_font.h"

#include "sound_duration_metadata.h"

namespace
{
    template<int SoundCount>
    class MultiSound {
        static_assert(SoundCount > 0);

        bn::vector<bn::sound_item, SoundCount> sounds;
        int timer;
        int i;
      public:
        MultiSound(bn::vector<bn::sound_item, SoundCount> s): sounds(s), timer(0), i(0) {}
        void update() {
            if (timer++ == 0) {
                sounds[i].play();
            }
            if (timer == wake::duration(sounds[i])) {
                timer = 0;
                i = (i+1) % SoundCount;
            }
        }
    };

    void sound_scene()
    {
        constexpr bn::string_view info_text_lines[] = {
            "riverrun, past Eve and Adam's",
            "from swerve of shore to bend of bay",
            "brings us by",
            "a commodius vicus of recirculation",
            "back to Howth Castle and Environs",
        };

        bn::sprite_text_generator text_generator(common::variable_8x16_sprite_font);
        common::info info("", info_text_lines, text_generator);
        info.set_show_always(true);
        int x = 0;
        // int i = 0;
        bn::vector<bn::sound_item, 2> sounds;
        sounds.push_back(bn::sound_items::riverrun);
        sounds.push_back(bn::sound_items::base);
        //  {, bn::sound_items::riverrun_demo}
        MultiSound<2> loop = {sounds};

        while(! bn::keypad::start_pressed())
        {
            if(bn::keypad::a_pressed())
            {
                // bn::sound_items::riverrun_demo.id
                bn::sound_items::riverrun.play(1);
                x = 0;
            }
            int duration = wake::duration(bn::sound_items::crummy);
            
            bn::vector<bn::sprite_ptr, 32> text_sprites;
            text_generator.generate(0, 40, bn::to_string<32>(x++), text_sprites);
            loop.update();
            bn::core::update();
        }
    }
}

int main()
{
    bn::core::init();

    bn::bg_palettes::set_transparent_color(bn::color(16, 16, 16));

    while(! bn::keypad::start_pressed())
    {
        sound_scene();
        bn::core::update();
    }
}