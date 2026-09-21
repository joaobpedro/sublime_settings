import sublime
import sublime_plugin

def apply_resize(window):
    layout = window.get_layout()
    # Verify standard 2-column layout
    if len(layout.get('cols', [])) == 3 and len(layout.get('rows', [])) == 2 and len(layout.get('cells', [])) == 2:
        active_group = window.active_group()
        
        target_split = 0.7 if active_group == 0 else 0.3 if active_group == 1 else None
        
        if target_split and abs(layout['cols'][1] - target_split) > 0.01:
            layout['cols'][1] = target_split
            window.set_layout(layout)

def reset_layout(window):
    layout = window.get_layout()
    if len(layout.get('cols', [])) == 3 and len(layout.get('rows', [])) == 2 and len(layout.get('cells', [])) == 2:
        if abs(layout['cols'][1] - 0.5) > 0.01:
            layout['cols'][1] = 0.5
            window.set_layout(layout)

class ToggleAutoResizeColumnsCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Load global preferences
        prefs = sublime.load_settings("Preferences.sublime-settings")
        
        # Toggle the state (defaults to False if not set yet)
        current_state = prefs.get("auto_resize_columns_enabled", False)
        new_state = not current_state
        
        prefs.set("auto_resize_columns_enabled", new_state)
        sublime.save_settings("Preferences.sublime-settings")

        if new_state:
            sublime.status_message("Auto-Resize Columns: ON")
            apply_resize(self.window)
        else:
            sublime.status_message("Auto-Resize Columns: OFF")
            reset_layout(self.window)

class AutoResizeColumnsListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        prefs = sublime.load_settings("Preferences.sublime-settings")
        # Check if the feature is enabled; do nothing if it's off
        if not prefs.get("auto_resize_columns_enabled", False):
            return
            
        window = view.window()
        if window:
            apply_resize(window)