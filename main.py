"""
Agenda:
    PS = pre setup turn
    S1 = setup turn
    S2 = setup followup / second setup turn
    TO = take out turn (the turn to take out some pieces from their slot)
    T2 = second teardown turn (to undo the second setup)
    T1 = teardown turn (to undo the first setup)

1. The order of turns for each cycle is: PS -> S1 -> S2 -> TO -> T2 -> T1
2. PS, S2 and T2 are optional. If S2 is skipped, T2 will also be skipped.
3. Perform as many cycles as necessary to reach the minimum turns. It's okay to go over slightly.
4. Minimum turns is 20.
"""
from random import choice
import tkinter as tk

pre_setup = ["D", "D'", "D2"]
setup = ["F", "F'", "B", "B'", "L", "L'", "R", "R'"]
setup_followup = {
    "F": ["B", "B'", "R", "R'"],
    "F'": ["B", "B'", "L", "L'"],
    "B": ["F", "F'", "L", "L'"],
    "B'": ["F", "F'", "R", "R'"],
    "L": ["F", "F'", "R", "R'"],
    "L'": ["B", "B'", "R", "R'"],
    "R": ["B", "B'", "L", "L'"],
    "R'": ["F", "F'", "L", "L'"]
}
take_out = ["U", "U'", "U2"]


# Main function that implements the logic to generate the scramble
def generate_scramble():
    final_scramble = []
    move_count = 0
    while move_count < int(chosen_option.get()):
        turns_for_current_cycle = []

        if flip_coin():
            turns_for_current_cycle.append(do_presetup())

        first_setup = do_setup()
        turns_for_current_cycle.append(first_setup)

        second_setup = None
        if flip_coin():
            second_setup = do_second_setup(first_setup)
            turns_for_current_cycle.append(second_setup)

        turns_for_current_cycle.append(do_take_out())

        if second_setup is not None:
            turns_for_current_cycle.append(do_teardown(second_setup))

        turns_for_current_cycle.append(do_teardown(first_setup))

        for turn in turns_for_current_cycle:
            final_scramble.append(turn)

        move_count = len(final_scramble)

    first_half, second_half = split_list_into_two(final_scramble)
    update_scramble_widget(first_half, second_half)


def flip_coin():
    return choice([True, False])


def do_presetup():
    return choice(pre_setup)


def do_setup():
    return choice(setup)


def do_second_setup(first_setup):
    return choice(setup_followup[first_setup])


def do_take_out():
    return choice(take_out)


def do_teardown(chosen_setup):
    if "'" in chosen_setup:
        output = chosen_setup.replace("'", "")
    else:
        output = f"{chosen_setup}'"
    return output


def display_scramble(scramble):
    output = ''
    for turn in scramble:
        output += f"{turn} "
    return output


def split_list_into_two(target_list):
    half = len(target_list) // 2
    return target_list[:half], target_list[half:]


def update_scramble_widget(first_half, second_half):
    scramble_text.config(text=display_scramble(first_half))
    scramble_text2.config(text=display_scramble(second_half))


root = tk.Tk()
root.title("F2L Scrambler")
# Set the GUI close to the centre
window_width, window_height = 750, 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
root.geometry(f'{window_width}x{window_height}+{position_right-20}+{position_top-20}')

# Define widgets
scramble_text = tk.Label(root, font=("Trebuchet MS", 24, "bold"))
scramble_text2 = tk.Label(root, font=("Trebuchet MS", 24, "bold"))
scramble_button = tk.Button(root, padx=30, pady=10, text="New Scramble", font=("Trebuchet MS", 12),
                            command=generate_scramble)
scramble_options = [20, 25, 30]
chosen_option = tk.StringVar()
chosen_option.set(scramble_options[0])
scramble_options_text = tk.Label(root, font=("Trebuchet MS", 12), text="Minimum scramble length (turns)")
scramble_options_menu = tk.OptionMenu(root, chosen_option, *scramble_options)
instruction_text = tk.Label(root, font=("Trebuchet MS", 12),
                            text="Note: Scramble with a solved cross facing down.")


# Position widgets
scramble_text.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
scramble_text2.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
scramble_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
scramble_options_text.place(relx=0.25, rely=0.63)
scramble_options_menu.place(relx=0.65, rely=0.65, anchor=tk.CENTER)
instruction_text.place(relx=0.25, rely=0.8)

generate_scramble()
root.mainloop()
