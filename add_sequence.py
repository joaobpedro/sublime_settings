import sublime
import sublime_plugin

class InsertSequenceCommand(sublime_plugin.TextCommand):
    def run(self, edit, start=1, step=1):
        cursors = list(self.view.sel())
        
        # Process in reverse to prevent text coordinate shifting,
        # but calculate the correct forward-counting value for each cursor
        for i, region in enumerate(reversed(cursors)):
            # Total cursors minus current reverse index minus 1 gives the top-to-bottom index
            current_index = len(cursors) - 1 - i
            val = start + (current_index * step)
            
            self.view.replace(edit, region, str(val))

class PromptInsertSequenceCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Enter starting number (default is 1):", 
            "1", 
            self.on_done, 
            None, 
            None
        )

    def on_done(self, text):
        try:
            start_val = int(text.strip())
            view = self.window.active_view()
            if view:
                view.run_command("insert_sequence", {"start": start_val})
        except ValueError:
            sublime.status_message("Invalid starting number.")