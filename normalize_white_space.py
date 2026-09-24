import sublime
import sublime_plugin
import re

class NormalizeWhitespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # If text is selected, only process the selections
        selections = [s for s in view.sel() if not s.empty()]
        
        # If no text is selected, process the entire file
        if not selections:
            selections = [sublime.Region(0, view.size())]

        # Process regions in reverse order so replacing text doesn't shift the coordinates of upcoming regions
        for region in reversed(selections):
            text = view.substr(region)
            # Replace 1 or more spaces/tabs with a single space
            normalized_text = re.sub(r'[ \t]+', ' ', text)
            view.replace(edit, region, normalized_text)