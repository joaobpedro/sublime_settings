import sublime
import sublime_plugin
import os

# class AutoPaneCppListener(sublime_plugin.EventListener):
#     def on_load(self, view):
#         window = view.window()
#         if not window:
#             return

#         # Ensure we have at least 2 columns
#         if window.num_groups() < 2:
#             return

#         file_name = view.file_name()
#         if not file_name:
#             return

#         _, ext = os.path.splitext(file_name)
#         current_group = window.active_group()

#         # Define destination groups (0 = Left, 1 = Right)
#         if ext in ['.h', '.hpp', '.hh']:
#             target_group = 0
#         elif ext in ['.cpp', '.cc', '.cxx', '.c']:
#             target_group = 1
#         else:
#             return

#         # If the file opened in the wrong pane, migrate it using sheets API
#         if current_group != target_group and view.sheet():
#             window.move_sheets_to_group([view.sheet()], target_group)
#             window.focus_view(view)


class OrganizeCppPanesCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        
        # 1. Force the layout into 2 Columns
        window.set_layout({
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })
        
        # 2. Collect all currently open views across all groups
        all_views = []
        for group in range(window.num_groups()):
            all_views.extend(window.views_in_group(group))
            
        # 3. Sort views into their respective targets (0 = Left, 1 = Right)
        for view in all_views:
            file_name = view.file_name()
            if not file_name or not view.sheet():
                continue
                
            _, ext = os.path.splitext(file_name)
            
            if ext in ['.h', '.hpp', '.hh']:
                window.move_sheets_to_group([view.sheet()], 0)
            elif ext in ['.cpp', '.cc', '.cxx', '.c']:
                window.move_sheets_to_group([view.sheet()], 1)
