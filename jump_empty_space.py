import sublime
import sublime_plugin

class JumpEmptySpaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=True, extend=False):
        view = self.view
        new_sel = []
        last_row = view.rowcol(view.size())[0]

        def is_empty(r):
            # Treat out-of-bounds as empty boundaries
            if r < 0 or r > last_row: return True
            line_text = view.substr(view.line(view.text_point(r, 0)))
            return len(line_text.strip()) == 0

        for region in view.sel():
            # region.b is always the active cursor position, even when selecting upwards
            start_row, _ = view.rowcol(region.b)
            step = 1 if forward else -1
            current_row = start_row

            # Step 1: If we are already on an empty line, skip past any adjacent empty lines
            if is_empty(current_row):
                while 0 <= current_row <= last_row and is_empty(current_row):
                    current_row += step
            
            # Step 2: Skip past all text lines until we land on the next empty line
            while 0 <= current_row <= last_row and not is_empty(current_row):
                current_row += step
            
            # Clamp to the top or bottom of the file
            current_row = max(0, min(current_row, last_row))
            target_pt = view.text_point(current_row, 0)

            if extend:
                new_sel.append(sublime.Region(region.a, target_pt))
            else:
                new_sel.append(sublime.Region(target_pt, target_pt))

        # Apply the new cursor positions
        view.sel().clear()
        view.sel().add_all(new_sel)
        view.show(view.sel())