import sublime
import sublime_plugin
import os
import re
import threading

class ListTodosCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders:
            sublime.status_message("No project folders open.")
            return
        
        sublime.status_message("Searching root folder(s) for TODOs...")
        
        # Run in a background thread so the editor UI doesn't freeze
        thread = threading.Thread(target=self._search_root, args=(folders,))
        thread.start()

    def _search_root(self, folders):
        pattern = re.compile(r'\b(TODO|FIXME|NOTE|BUG|XXX)\b.*', re.IGNORECASE)
        results = []
        
        # Extensions to skip to prevent reading binary files
        ignore_exts = {'.png', '.jpg', '.jpeg', '.gif', '.zip', '.pdf', '.pyc', '.exe', '.dll', '.so', '.sublime-project', '.sublime-workspace'}

        for folder in folders:
            try:
                # os.listdir only looks at the immediate children of the directory
                for item in os.listdir(folder):
                    file_path = os.path.join(folder, item)
                    
                    # Skip directories entirely
                    if not os.path.isfile(file_path):
                        continue
                        
                    ext = os.path.splitext(item)[1].lower()
                    if ext in ignore_exts:
                        continue
                    
                    # Try reading the file; gracefully skip binary files
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line_num, line in enumerate(f, 1):
                                match = pattern.search(line)
                                if match:
                                    col = match.start() + 1
                                    results.append((file_path, line_num, col, line.strip()))
                    except (UnicodeDecodeError, PermissionError):
                        pass
            except PermissionError:
                pass
        
        # Pass the results back to the main UI thread to render the panel
        sublime.set_timeout(lambda: self._show_results(results), 0)

    def _show_results(self, results):
        if not results:
            sublime.status_message("No TODOs found in the root folder(s).")
            return

        panel_name = 'todo_root_list'
        panel = self.window.create_output_panel(panel_name)
        
        # Enable double-click navigation to File Path, Line, and Column
        panel.settings().set("result_file_regex", r"^(.+?):([0-9]+):([0-9]+)")
        
        output_lines = [f"Found {len(results)} TODOs in Project Root", "=" * 70]
        for file_path, line_num, col, line_text in results:
            output_lines.append(f"{file_path}:{line_num}:{col}: {line_text}")

        panel.set_read_only(False)
        panel.run_command('append', {'characters': '\n'.join(output_lines) + '\n'})
        panel.set_read_only(True)
        
        self.window.run_command('show_panel', {'panel': f'output.{panel_name}'})
        sublime.status_message(f"Found {len(results)} root TODOs.")