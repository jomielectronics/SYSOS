import curses
import toml
import os
class Menu:
    def __init__(self, version) -> None:

        self.version = version
        self.main_menus = [
            "Command Presets",
            "Color Themes",
            "About",
            "Exit"
        ]
        self.main_messages = {
            "Command Presets": "Switch to a different command preset",
            "Color Themes": "Set the system\'s colors",
            "About": "Display information about SYSOS Configuration Tool",
            "Exit": "Exit the configuration tool"
        }

        self.avaliable_presets = [
            "Unix",
            "SYSOS",
            "Windows"
        ]
        self.preset_messages = {
            "Unix": "This preset includes commands for Unix-like systems",
            "SYSOS": "This preset includes commands for SYSOS",
            "Windows": "This preset includes commands for Windows"
        }        
        self.selected_preset = None
        
        self.available_colors = [
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", 
            "light_grey", "dark_grey", "light_red", "light_green", "light_yellow", 
            "light_blue", "light_magenta", "light_cyan"
        ]

        self.output_colors = {
            "Error": self.available_colors[1],        # red
            "Warning": self.available_colors[11],     # light_green
            "SystemOut": self.available_colors[3],    # yellow
            "Advice": self.available_colors[5],       # magenta
            "Other": self.available_colors[7],        # white
            "cPrompt": self.available_colors[9]       # dark_grey
        }

        self.file_colors = {
            "Direc": self.available_colors[4],        # blue
            "Text": self.available_colors[5],         # magenta
            "Program": self.available_colors[2],      # green
            "Other": self.available_colors[3]         # yellow
        }

        self.text_types = list(self.output_colors.keys())
        self.file_types = list(self.file_colors.keys())
        self.all_types = self.text_types + self.file_types

    def onkill(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")
        data = {
            "selected_preset": "" if self.selected_preset is None else self.selected_preset,
            "output_colors": self.output_colors,
            "file_colors": self.file_colors
        }
        
        with open(config_path, "w") as f:
            toml.dump(data, f)


    def show_title(self, w, h, stdscr, menu, v_offset=1):
        # Initialize color pair 1 (red text on default background)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        v_offset += 1 if v_offset else 0
        title = "SYSOS Configuration Tool"
        x_title = w // 2 - len(title) // 2  # Center the title horizontally
        y_title = (h // 2 - len(menu) // 2 - 3)  - v_offset # Place above the menu

        subtitle = f"Version {self.version}"
        x_subtitle = w // 2 - len(subtitle) // 2  # Center the title horizontally
        y_subtitle = (h // 2 - len(menu) // 2 - 2) - v_offset # Place above the menu

        if menu == self.all_types:
            subsubtitle = "\u2190 and \u2192 to change colors, and \u23ce to save and exit"
            x_subsubtitle = w // 2 - len(subsubtitle) // 2  # Center the title horizontally
            y_subsubtitle = (h // 2 - len(menu) // 2 - 1) - v_offset # Place above the menu
            stdscr.addstr(y_subsubtitle, x_subsubtitle, subsubtitle, curses.color_pair(3)) #add to screen
        elif menu == self.avaliable_presets:
            subsubtitle = "\u23ce to save and exit"
            x_subsubtitle = w // 2 - len(subsubtitle) // 2  # Center the title horizontally
            y_subsubtitle = (h // 2 - len(menu) // 2 - 1) - v_offset # Place above the menu
            stdscr.addstr(y_subsubtitle, x_subsubtitle, subsubtitle, curses.color_pair(3)) #add to screen
        else:
            subsubtitle = "Use arrow keys to navigate"
            x_subsubtitle = w // 2 - len(subsubtitle) // 2  # Center the title horizontally
            y_subsubtitle = (h // 2 - len(menu) // 2 - 1) - v_offset # Place above the menu
            stdscr.addstr(y_subsubtitle, x_subsubtitle, subsubtitle, curses.color_pair(3)) #add to screen
        

        # Display the title in red
        stdscr.addstr(y_title, x_title, title, curses.color_pair(1))
        stdscr.addstr(y_subtitle, x_subtitle, subtitle, curses.color_pair(2))
        

    def display_message(self, stdscr, message, color=curses.A_NORMAL):
        """Displays a message at the bottom of the screen."""
        h, w = stdscr.getmaxyx()
        stdscr.addstr(h - 1, 0, " " * (w - 1))  # Clear the message line
        stdscr.addstr(h - 1, 0, message, color)
        stdscr.refresh()

    def main_menu(self, stdscr):
        # Disable cursor
        curses.curs_set(0)

        # Calculate the length of the longest menu item
        max_length = max(len(f"{item}") for item in self.main_menus)

        current_row = 0

        while True:
            # Get terminal dimensions
            h, w = stdscr.getmaxyx()

            # Clear the screen
            stdscr.clear()

            # Display menu
            self.show_title(w, h, stdscr, self.main_menus)
            for idx, item in enumerate(self.main_menus):
                # Pad the item to match the longest length
                padded_item = f"{item.ljust(max_length)}"

                x = w // 2 - max_length // 2  # Center horizontally based on padded length
                y = h // 2 - len(self.main_menus) // 2 + idx  # Center vertically, adjust for index

                if idx == current_row:
                    # Highlight the current selection
                    stdscr.addstr(y, x, padded_item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, padded_item)

            # Display the corresponding message
            selected_item = self.main_menus[current_row]
            message = self.main_messages.get(selected_item, "")
            self.display_message(stdscr, message, color=curses.A_BOLD)

            stdscr.refresh()

            # User input
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.main_menus) - 1:
                current_row += 1
            elif key == ord("\n"):  # Enter key
                if current_row == self.main_menus.index("Exit"):  # Exit selected
                    self.display_message(stdscr, "Saving to user prefrences...", color=curses.A_BOLD)
                    stdscr.refresh()
                    self.onkill()
                    curses.napms(1000)  # Pause for 1 second
                    self.display_message(stdscr, "Exiting...", color=curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1000)  # Pause for 1 second
                    break
                elif current_row == self.main_menus.index("Command Presets"):
                    curses.wrapper(self.command_presets)
                    break
                elif current_row == self.main_menus.index("Color Themes"):
                    curses.wrapper(self.color_themes)
                    break

                elif current_row == self.main_menus.index("About"):
                    self.display_message(stdscr, "About page is currently not supported.", color=curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1000)  # Pause for a moment to show the message
                else:

                    # Add actions for other menu items here
                    self.display_message(stdscr, f"You selected: {selected_item}", color=curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1000)  # Pause for a moment to show the message

    def command_presets(self, stdscr):
        # Disable cursor
        curses.curs_set(0)

        # Calculate the length of the longest menu item
        max_length = max(len(f"{item}") for item in self.avaliable_presets)

        current_row = 0

        while True:
            # Get terminal dimensions
            h, w = stdscr.getmaxyx()

            # Clear the screen
            stdscr.clear()

            # Display menu
            self.show_title(w, h, stdscr, self.avaliable_presets)
            for idx, item in enumerate(self.avaliable_presets):
                # Pad the item to match the longest length
                padded_item = f"{item.ljust(max_length)}"

                x = w // 2 - max_length // 2  # Center horizontally based on padded length
                y = h // 2 - len(self.avaliable_presets) // 2 + idx  # Center vertically, adjust for index

                if idx == current_row:
                    # Highlight the current selection
                    stdscr.addstr(y, x, padded_item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, padded_item)

            # Display the corresponding message
            selected_item = self.avaliable_presets[current_row]
            message = self.preset_messages.get(selected_item, "")
            self.display_message(stdscr, message, color=curses.A_BOLD)

            stdscr.refresh()

            # User input
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.avaliable_presets) - 1:
                current_row += 1
            elif key == ord("\n"):  # Enter key
                # Add actions for other menu items here
                self.display_message(stdscr, f"You selected: {selected_item}. Saving to cache.", color=curses.A_BOLD)
                self.selected_preset = self.avaliable_presets[current_row]
                stdscr.refresh()
                curses.napms(1000)  # Pause for a moment to show the message
                curses.wrapper(self.main_menu)
                break
    
    def color_themes(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()  # Allows using -1 as the default background color

        # Standard curses colors (0-7)
        color_mapping = {
            "black": curses.COLOR_BLACK,
            "red": curses.COLOR_RED,
            "green": curses.COLOR_GREEN,
            "yellow": curses.COLOR_YELLOW,
            "blue": curses.COLOR_BLUE,
            "magenta": curses.COLOR_MAGENTA,
            "cyan": curses.COLOR_CYAN,
            "white": curses.COLOR_WHITE
        }

        # Manually assign extended colors (if supported)
        if curses.can_change_color():
            curses.init_color(8, 500, 500, 500)    # light_grey
            curses.init_color(9, 250, 250, 250)    # dark_grey
            curses.init_color(10, 1000, 500, 500)  # light_red
            curses.init_color(11, 500, 1000, 500)  # light_green
            curses.init_color(12, 1000, 1000, 500) # light_yellow
            curses.init_color(13, 500, 500, 1000)  # light_blue
            curses.init_color(14, 1000, 500, 1000) # light_magenta
            curses.init_color(15, 500, 1000, 1000) # light_cyan

            color_mapping.update({
                "light_grey": 8,
                "dark_grey": 9,
                "light_red": 10,
                "light_green": 11,
                "light_yellow": 12,
                "light_blue": 13,
                "light_magenta": 14,
                "light_cyan": 15
            })

        self.available_colors = list(color_mapping.keys())  # Ensure correct order

        # Initialize color pairs
        for i, (name, color) in enumerate(color_mapping.items(), start=1):
            curses.init_pair(i, color, -1)  # Use default background (-1)

        # self.text_types = list(self.output_colors.keys())
        # self.file_types = list(self.file_colors.keys())
        # self.all_types = self.text_types + self.file_types

        # Ensure every color is in available_colors; fallback to 'white' if missing
        color_indices = {
            key: self.available_colors.index(value) if value in self.available_colors else self.available_colors.index("white")
            for key, value in {**self.output_colors, **self.file_colors}.items()
        }

        current_row = 0  # This will track the position across both sections

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            self.show_title(w, h, stdscr, self.all_types)
            
            # Display the title for text colors
            text_title = "Text colors:"
            stdscr.addstr((h // 2 - len(self.text_types) // 2) - 1, w // 2 - len(text_title) // 2, text_title)

            # Display text color items
            for idx, type in enumerate(self.text_types):
                color_idx = color_indices[type] + 1  # Ensure color pairs align with curses (starting from 1)
                color_pair = curses.color_pair(color_idx)
                x = w // 2 - 10
                y = h // 2 - len(self.text_types) // 2 + idx
                
                if idx == current_row:
                    stdscr.addstr(y, x, f"{type}: {self.available_colors[color_idx - 1]}", curses.A_REVERSE | color_pair)
                else:
                    stdscr.addstr(y, x, f"{type}: {self.available_colors[color_idx - 1]}", color_pair)


            # Display the title for file colors
            file_title = "Filecolors:"
            stdscr.addstr(h // 2 + len(self.text_types) // 2 + 1, w // 2 - len(file_title) // 2, file_title)

            # Display file color items
            for idx, type in enumerate(self.file_types):
                color_idx = color_indices[type] + 1  # Ensure color pairs align with curses (starting from 1)
                color_pair = curses.color_pair(color_idx)
                x = w // 2 - 10
                y = h // 2 + len(self.text_types) // 2 + idx + 2

                # Update current_row for file colors (after the text_colors items)
                adjusted_row = current_row - len(self.text_types)

                if adjusted_row == idx:
                    stdscr.addstr(y, x, f"{type}: {self.available_colors[color_idx - 1]}", curses.A_REVERSE | color_pair)
                else:
                    stdscr.addstr(y, x, f"{type}: {self.available_colors[color_idx - 1]}", color_pair)

            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.all_types) - 1:
                current_row += 1
            elif key == curses.KEY_LEFT:
                # Only update color for the current row item (text or file)
                current_row_type = self.all_types[current_row]
                color_indices[current_row_type] = (color_indices[current_row_type] - 1) % len(self.available_colors)
            elif key == curses.KEY_RIGHT:
                # Only update color for the current row item (text or file)
                current_row_type = self.all_types[current_row]
                color_indices[current_row_type] = (color_indices[current_row_type] + 1) % len(self.available_colors)
            elif key == ord("\n"):
                self.display_message(stdscr, f"Saving to cache.", color=curses.A_BOLD)
                stdscr.refresh()
                curses.napms(1000)  # Pause for a moment to show the message
                curses.wrapper(self.main_menu)
                break

            # Update the color settings for the selected row
            selected_type = self.all_types[current_row]
            new_color = self.available_colors[color_indices[selected_type]]
            if selected_type in self.output_colors:
                self.output_colors[selected_type] = new_color
            else:
                self.file_colors[selected_type] = new_color

if __name__ == "__main__":
    sysos_menu = Menu("1.3.2")
    curses.wrapper(sysos_menu.main_menu)
    