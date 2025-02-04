import curses
class Menu:
    def __init__(self, version) -> None:
        self.version = version
        self.menu = [
            "Command Presets",
            "Color Themes",
            "About",
            "Exit"
        ]

        self.messages = {
            "Command Presets": "Switch to a different command preset",
            "Color Themes": "Set the system\'s colors",
            "About": "Display information about SYSOS Configuration Tool",
            "Exit": "Exit the configuration tool"
        }

    def show_title(self, w, h, stdscr, menu):
        # Initialize color pair 1 (red text on default background)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        title = "SYSOS Configuration Tool"
        x_title = w // 2 - len(title) // 2  # Center the title horizontally
        y_title = h // 2 - len(menu) // 2 - 3  # Place above the menu

        subtitle = f"Version {self.version}"
        x_subtitle = w // 2 - len(subtitle) // 2  # Center the title horizontally
        y_subtitle = h // 2 - len(menu) // 2 - 2  # Place above the menu

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
        max_length = max(len(f"{item}") for item in self.menu)

        current_row = 0

        while True:
            # Get terminal dimensions
            h, w = stdscr.getmaxyx()

            # Clear the screen
            stdscr.clear()

            # Display menu
            self.show_title(w, h, stdscr, self.menu)
            for idx, item in enumerate(self.menu):
                # Pad the item to match the longest length
                padded_item = f"{item.ljust(max_length)}"

                x = w // 2 - max_length // 2  # Center horizontally based on padded length
                y = h // 2 - len(self.menu) // 2 + idx  # Center vertically, adjust for index

                if idx == current_row:
                    # Highlight the current selection
                    stdscr.addstr(y, x, padded_item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, padded_item)

            # Display the corresponding message
            selected_item = self.menu[current_row]
            message = self.messages.get(selected_item, "")
            self.display_message(stdscr, message, color=curses.A_BOLD)

            stdscr.refresh()

            # User input
            key = stdscr.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.menu) - 1:
                current_row += 1
            elif key == ord("\n"):  # Enter key
                if current_row == self.menu.index("Exit"):  # Exit selected
                    self.display_message(stdscr, "Exiting...", color=curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1000)  # Pause for 1 second
                    break
                # Add actions for other menu items here
                self.display_message(stdscr, f"You selected: {selected_item}", color=curses.A_BOLD)
                stdscr.refresh()
                curses.napms(1000)  # Pause for a moment to show the message

if __name__ == "__main__":
    sysos_menu = Menu("1.3.2")
    curses.wrapper(sysos_menu.main_menu)