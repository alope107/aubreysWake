/*
Adapted from Butano audio example
*/
#include "bn_core.h"
#include "bn_log.h"
#include "bn_size.h"
#include "bn_keypad.h"
#include "bn_bg_palettes.h"
#include "bn_sound_actions.h"
#include "bn_sprite_text_generator.h"
#include "bn_string.h"

#include "wake_log.h"
#include "wake_updater.h"
#include "wake_walker.h"
#include "wake_geometry.h"
#include "wake_text.h"

#include "bn_sound_items.h"
#include "bn_sprite_items_circle.h"

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
        bn::sprite_font font = common::variable_8x16_sprite_font;

        bn::sprite_text_generator text_generator(font);
        common::info info("", info_text_lines, text_generator);
        info.set_show_always(true);
        int x = 0;

        bn::vector<bn::sound_item, 6> sounds;
        sounds.push_back(bn::sound_items::r);
        sounds.push_back(bn::sound_items::ih1);
        sounds.push_back(bn::sound_items::v);
        sounds.push_back(bn::sound_items::er0);
        sounds.push_back(bn::sound_items::ah0);
        sounds.push_back(bn::sound_items::n);

        MultiSound<6> loop = {sounds};

        wake::Updater<10> updater;

        auto circle_spr = bn::sprite_items::circle.create_sprite(0, 0);

        auto walker = wake::Walker(circle_spr, 1);
        updater.add(walker);

        while(! bn::keypad::start_pressed())
        {
            if(bn::keypad::a_pressed())
            {
                x = 0;
            }
            
            bn::vector<bn::sprite_ptr, 32> text_sprites;

            auto to_display = bn::to_string<32>(x);
            auto center = bn::fixed_point(0, 40);
            text_generator.generate(center, to_display, text_sprites);
            auto text_bounds = wake::text_bounds(center, to_display, font);
            wake::log(text_bounds.top_left.x(), text_bounds.top_left.y(), text_bounds.bottom_right.x(), text_bounds.bottom_right.y());

            if (!wake::point_in_rect(walker.position(), text_bounds)) {
                x++;
            }
            

            if(bn::keypad::b_pressed())
            {
                wake::log(walker.position().x(), walker.position().y());
            }
            
            updater.update();
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