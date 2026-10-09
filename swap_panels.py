import sublime
import sublime_plugin

class SwapPanesCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        
        # Ensure we have at least two groups (panels)
        if window.num_groups() < 2:
            return

        # Get the active views (files) in the first two panels
        view_left = window.active_view_in_group(0)
        view_right = window.active_view_in_group(1)

        # We need at least one file open to perform a swap move
        if not view_left and not view_right:
            return

        # Handle moving the left file to the right group
        if view_left:
            # Get the current index of the view in its current group
            _, index = window.get_view_index(view_left)
            window.set_view_index(view_left, 1, 0)

        # Handle moving the right file to the left group
        if view_right:
            # Get the current index of the view in its current group
            _, index = window.get_view_index(view_right)
            window.set_view_index(view_right, 0, 0)
