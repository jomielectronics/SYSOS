import curses
import time

class NanoPy:
    def __init__(self, stdscrm, filename=""):
        self.stdscr = stdscrm
        self.cursor_x = 0
        self.cursor_y = 0
        self.content = ["vibity vub"]
        self.running = True 
        self.filename = filename
        self.status_message =  f"CTRL+S: Save | CTRL+Q: Quit | Status: unsaved | Name: {self.filename}" if self.filename else "CTRL+S: Save | CTRL+Q: Quit | Status: unsaved | Name: unnamed"
        if filename:
            with open(filename, 'r') as f:
                self.content = f
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def draw_interface(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()  # Get the terminal's height and width

        # Ensure the terminal has at least two rows for content and status bar
        if h < 2 or w < 1:
            self.stdscr.addstr(0, 0, "Terminal too small. Resize to continue.".ljust(w)[:w])
            self.stdscr.refresh()
            return

        # Draw text content, truncated to fit the visible screen
        for idx, line in enumerate(self.content):
            if idx < h - 1:  # Leave space for the status bar
                try:
                    self.stdscr.addstr(idx, 0, line[:w])  # Truncate lines to fit the width
                except curses.error:
                    continue  # Handle any unexpected curses errors gracefully

        # Draw the status bar at the bottom
        self.stdscr.attron(curses.color_pair(1))
        try:
            truncated_status = self.status_message[:w]  # Ensure it fits the screen width
            self.stdscr.addstr(h - 1, 0, truncated_status.ljust(w)[:w])  # Draw status bar at the bottom
        except curses.error:
            pass  # Ignore any drawing issues here
        self.stdscr.attroff(curses.color_pair(1))

        # Move the cursor within bounds (above the status bar)
        self.cursor_x = min(self.cursor_x, w - 1)  # Ensure the cursor stays within the width
        self.cursor_y = min(self.cursor_y, h - 2)  # Ensure the cursor stays within the height
        self.stdscr.move(self.cursor_y, self.cursor_x)
        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()

        if key == curses.KEY_UP:
            self.cursor_y = max(self.cursor_y - 1, 0)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.cursor_y + 1, len(self.content) - 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(self.cursor_x - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.cursor_x + 1, len(self.content[self.cursor_y]))
        elif key == 10:  # Enter key
            current_line = self.content[self.cursor_y]
            self.content[self.cursor_y] = current_line[:self.cursor_x]
            self.content.insert(self.cursor_y + 1, current_line[self.cursor_x:])
            self.cursor_x = 0
            self.cursor_y += 1
        elif key == 127:  # Backspace key
            if self.cursor_x > 0:
                current_line = self.content[self.cursor_y]
                self.content[self.cursor_y] = current_line[:self.cursor_x - 1] + current_line[self.cursor_x:]
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                current_line = self.content.pop(self.cursor_y)
                self.cursor_y -= 1
                self.cursor_x = len(self.content[self.cursor_y])
                self.content[self.cursor_y] += current_line
        elif key == 19:  # CTRL+S to save
            self.save_file()
        elif key == 17:  # CTRL+Q to quit
            self.running = False
        elif key == 14:  # CTRL+N to set filename
            curses.echo()
            self.stdscr.addstr(self.stdscr.getmaxyx()[0] - 1, 0, "Enter filename: ")
            self.stdscr.clrtoeol()  # Clear the rest of the status line
            self.filename = self.stdscr.getstr().decode("utf-8").strip()
            curses.noecho()
            self.status_message = f"Filename set to {self.filename}"
        else:
            char = chr(key)
            current_line = self.content[self.cursor_y]
            self.content[self.cursor_y] = current_line[:self.cursor_x] + char + current_line[self.cursor_x:]
            self.cursor_x += 1

    def save_file(self):
        if not self.filename:  # Check if filename is empty
            self.status_message = "Filename not set. Use 'Ctrl+N' to set a name."
            return
        
        try:
            with open(self.filename, "w") as file:
                file.write("\n".join(self.content))  # Write all lines to the file
            self.status_message = f"File saved to {self.filename}"
            self.stdscr.refresh()
            curses.napms(1000)  # Wait for 1 second (1000 milliseconds)
            self.status_message = f"CTRL+S: Save | CTRL+Q: Quit | Status: saved | Name: {self.filename}"
        except Exception as e:
            self.status_message = f"Error saving file: {str(e)}"

    def run(self):
        """Run the main editor loop."""
        curses.raw()  # Enable raw mode for precise input handling

        while self.running:
            self.draw_interface()
            self.handle_input()

def main(stdscr):
    editor = NanoPy(stdscr, "vibityvub")
    editor.run()

if __name__ == "__main__":
    curses.wrapper(main)