import sublime
import sublime_plugin
import re

class FormatMarkdownTableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            # If nothing is selected, attempt to auto-expand to the table's boundaries
            if region.empty():
                region = self._get_table_region(region.a)
                if not region:
                    continue
            
            text = self.view.substr(region)
            formatted_text = self._format_table(text)
            
            if formatted_text:
                self.view.replace(edit, region, formatted_text)

    def _get_table_region(self, pt):
        """Expands up and down from the cursor to find all connected lines containing a pipe '|'."""
        row, col = self.view.rowcol(pt)
        
        # Expand upwards
        start_row = row
        while start_row >= 0:
            line_text = self.view.substr(self.view.line(self.view.text_point(start_row, 0)))
            if '|' not in line_text:
                start_row += 1
                break
            start_row -= 1
        if start_row < 0: start_row = 0

        # Expand downwards
        last_row = self.view.rowcol(self.view.size())[0]
        end_row = row
        while end_row <= last_row:
            line_text = self.view.substr(self.view.line(self.view.text_point(end_row, 0)))
            if '|' not in line_text:
                end_row -= 1
                break
            end_row += 1
        if end_row > last_row: end_row = last_row

        if start_row <= end_row:
            start_pt = self.view.text_point(start_row, 0)
            end_pt = self.view.line(self.view.text_point(end_row, 0)).b
            return sublime.Region(start_pt, end_pt)
        
        return None

    def _format_table(self, text):
        lines = [line.strip() for line in text.strip().split('\n')]
        if not lines: 
            return None

        parsed_rows = []
        col_widths = []

        # First pass: parse cells and determine maximum column widths
        for line in lines:
            if not line: continue
            
            # Strip outer pipes to avoid empty edge columns
            if line.startswith('|'): line = line[1:]
            if line.endswith('|'): line = line[:-1]
            
            cells = [cell.strip() for cell in line.split('|')]
            parsed_rows.append(cells)
            
            for i, cell in enumerate(cells):
                width = max(len(cell), 3) # Enforce a minimum of 3 dashes for the separator row
                if i >= len(col_widths):
                    col_widths.append(width)
                else:
                    col_widths[i] = max(col_widths[i], width)

        # Second pass: reconstruct the table with padding
        formatted_lines = []
        for cells in parsed_rows:
            # Detect if this is the structure row (e.g., |---|:---|)
            is_separator = all(re.match(r'^:?-+:?$', c) for c in cells if c)
            
            formatted_cells = []
            for i in range(len(col_widths)):
                cell = cells[i] if i < len(cells) else ""
                width = col_widths[i]
                
                if is_separator:
                    # Preserve markdown alignment colons
                    left = cell.startswith(':')
                    right = cell.endswith(':')
                    if left and right:
                        formatted_cells.append(':' + '-' * (width - 2) + ':')
                    elif left:
                        formatted_cells.append(':' + '-' * (width - 1))
                    elif right:
                        formatted_cells.append('-' * (width - 1) + ':')
                    else:
                        formatted_cells.append('-' * width)
                else:
                    # Pad text cells with spaces
                    formatted_cells.append(cell.ljust(width))
                    
            formatted_lines.append("| " + " | ".join(formatted_cells) + " |")
            
        return '\n'.join(formatted_lines)