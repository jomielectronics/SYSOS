import curses
import time


class NanoPy:
    def __init__(self, stdscr,current_dir,filename="sysos.py"):
        self.stdscr = stdscr
        self.cursor_x = 0
        self.cursor_y = 0
        self.scroll_offset = 0  # Offset for scrolling
        self.content = []
        self.running = True
        self.current_dir = current_dir
        self.filename = filename
        self.status_message = f"CTRL+S: Save | CTRL+Q: Quit | Status: unsaved | Name: {self.filename} (CTRL+N to rename)" if self.filename else "CTRL+S: Save | CTRL+Q: Quit | Status: unsaved | Name: unnamed"

        if self.filename:
            filedir = self.current_dir + "/" + self.filename
            with open(filedir, 'r') as f:
                for line in f.readlines():
                    self.content.append(line.strip())

        if not self.content:
            self.content = [""]

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def draw_interface(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        content_height = h - 1  # Leave space for the status bar

        # Draw content starting from scroll_offset
        for idx in range(content_height):
            line_idx = self.scroll_offset + idx
            if line_idx < len(self.content):
                line = self.content[line_idx].rstrip()
                # Display only visible part of the line
                self.stdscr.addstr(idx, 0, line[:w])

        # Draw the status bar
        self.stdscr.attron(curses.color_pair(1))
        try:
            truncated_status = self.status_message[:w]
            self.stdscr.addstr(h - 1, 0, truncated_status.ljust(w)[:w])
        except curses.error:
            pass
        self.stdscr.attroff(curses.color_pair(1))

        # Adjust cursor position relative to scroll_offset
        cursor_y_on_screen = self.cursor_y - self.scroll_offset
        self.stdscr.move(cursor_y_on_screen, self.cursor_x)
        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()
        h, w = self.stdscr.getmaxyx()
        content_height = h - 1

        if key == curses.KEY_UP:
            if self.cursor_y > 0:
                self.cursor_y -= 1
            if self.cursor_y < self.scroll_offset:
                self.scroll_offset -= 1  # Scroll up
        elif key == curses.KEY_DOWN:
            if self.cursor_y < len(self.content) - 1:
                self.cursor_y += 1
            if self.cursor_y >= self.scroll_offset + content_height:
                self.scroll_offset += 1  # Scroll down
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(self.cursor_x - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.cursor_x + 1,
                                len(self.content[self.cursor_y].rstrip()))
        elif key == 10:  # Enter key
            current_line = self.content[self.cursor_y]
            self.content[self.cursor_y] = current_line[:self.cursor_x]
            self.content.insert(self.cursor_y + 1,
                                current_line[self.cursor_x:])
            self.cursor_x = 0
            self.cursor_y += 1
            if self.cursor_y >= self.scroll_offset + content_height:
                self.scroll_offset += 1
        elif key == 127:  # Backspace
            if self.cursor_x > 0:
                current_line = self.content[self.cursor_y]
                self.content[self.cursor_y] = current_line[:self.cursor_x -
                                                           1] + current_line[self.cursor_x:]
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                prev_line = self.content[self.cursor_y - 1]
                self.cursor_x = len(prev_line.rstrip())
                self.content[self.cursor_y -
                             1] += self.content.pop(self.cursor_y)
                self.cursor_y -= 1
                if self.cursor_y < self.scroll_offset:
                    self.scroll_offset -= 1
        elif key == 19:  # CTRL+S to save
            self.save_file(self.current_dir)
        elif key == 17:  # CTRL+Q to quit
            self.running = False
        elif key == 14:  # CTRL+N to set filename
            curses.echo()
            self.stdscr.addstr(self.stdscr.getmaxyx()[
                               0] - 1, 0, "Enter filename: ")
            self.stdscr.clrtoeol()
            self.filename = self.stdscr.getstr().decode("utf-8").strip()
            curses.noecho()
            self.status_message = f"Filename set to {self.filename}"
        else:
            char = chr(key)
            # if self.cursor_y >= len(self.content):
            #     self.content.append("")  # Add a new empty line if needed
            current_line = self.content[self.cursor_y]
            self.content[self.cursor_y] = current_line[:self.cursor_x] + \
                char + current_line[self.cursor_x:]
            self.cursor_x += 1

    def save_file(self, dir):
        if not self.filename:
            self.status_message = "Filename not set. Use 'Ctrl+N' to set a name."
            return
        try:
            filedir = dir + "/" + self.filename
            with open(filedir, "w") as file:
                file.write("\n".join(self.content))
            self.status_message = f"File saved to {self.filename}"
            time.sleep(1)
            self.status_message = f"CTRL+S: Save | CTRL+Q: Quit | Status: saved | Name: {self.filename}"
        except Exception as e:
            self.status_message = f"Error saving file: {str(e)}"

    def run(self):
        while self.running:
            self.draw_interface()
            self.handle_input()


def main(stdscr):
    editor = NanoPy(stdscr)
    editor.run()


if __name__ == "__main__":
    curses.wrapper(main)
