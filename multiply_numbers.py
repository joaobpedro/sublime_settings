import sublime
import sublime_plugin

class MultiplyNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit, factor):
        try:
            factor_val = float(factor)
        except ValueError:
            sublime.status_message("Invalid multiplier factor.")
            return

        # Process in reverse so string length changes don't misalign subsequent cursors
        for region in reversed(self.view.sel()):
            if region.empty():
                continue
                
            text = self.view.substr(region).strip()
            
            try:
                num = float(text)
                
                # Multiply, round to nearest whole number, and convert to integer
                result = int(round(num * factor_val))
                
                self.view.replace(edit, region, str(result))
            except ValueError:
                # Silently skip any cursors that highlighted text instead of numbers
                pass

class PromptMultiplyNumbersCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Multiply selected numbers by (rounds to integer):", 
            "2", 
            self.on_done, 
            None, 
            None
        )

    def on_done(self, text):
        view = self.window.active_view()
        if view:
            # Pass the input factor to the TextCommand to apply the edit
            view.run_command("multiply_numbers", {"factor": text})