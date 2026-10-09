import sublime
import sublime_plugin
import time

class TripleDashSeparatorCommand(sublime_plugin.TextCommand):
    # Track timestamps and counts per view to prevent cross-file interference
    last_press_time = 0
    dash_count = 0
    TIMEOUT = 0.5  # Maximum time allowed (in seconds) between presses

    def run(self, edit):
        current_time = time.time()
        
        # Reset count if the user waited too long between presses
        if current_time - self.last_press_time > self.TIMEOUT:
            self.dash_count = 0

        self.dash_count += 1
        self.last_press_time = current_time

        if self.dash_count == 3:
            # We already have two dashes in the buffer, insert a visual separator line instead of a third
            # You can change the string inside "" to whatever separator style you prefer
            separator = "--------------------------------------------------\n"
            
            # Select the last two characters to overwrite them
            for region in self.view.sel():
                if region.empty():
                    # Move caret back 2 spaces to clear the existing '--'
                    start = region.a - 2
                    end = region.a
                    if self.view.substr(sublime.Region(start, end)) == "--":
                        self.view.replace(edit, sublime.Region(start, end), separator)
                        
            self.dash_count = 0  # Reset counter
        else:
            # Just insert a regular dash for the 1st and 2nd press
            self.view.run_command("insert", {"characters": "-"})
