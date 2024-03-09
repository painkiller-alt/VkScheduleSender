from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:

    @property
    def menu(self):
        markup = VkKeyboard(one_time=False, inline=True)

        markup.add_callback_button(
            label='Расписание (Вкл/Выкл.)',
            color=VkKeyboardColor.SECONDARY,
            payload={"type": f"timetable"}
        )
        markup.add_line()

        markup.add_callback_button(
            label='Замены (Вкл/Выкл.)',
            color=VkKeyboardColor.SECONDARY,
            payload={"type": f"repls"}
        )

        return markup.get_keyboard()

kboards = Keyboards()