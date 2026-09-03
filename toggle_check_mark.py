import sublime
import sublime_plugin
import re


class ToggleMarkdownTaskCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    # Iterate over all cursor/selection regions
    for region in self.view.sel():
      # Expand region to cover the entire line(s)
      line = self.view.line(region)
      line_text = self.view.substr(line)

      # Check if the line already has a task pattern
      # Matches: optional leading whitespace, dash, spaces, and brackets with anything inside or empty
      match = re.match(r"^(\s*)-\s*\[([ xX]?)\](.*)$", line_text)

      if match:
        indent, state, rest = match.groups()
        # Toggle state: empty/space -> 'x', anything else -> ' '
        new_state = "x" if state.strip() == "" else " "
        new_line = f"{indent}- [{new_state}]{rest}"
      else:
        # If no task list exists, check if it's a bullet list or empty line to format nicely,
        # or simply prepend '- [ ] ' to the existing line content.
        bullet_match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line_text)
        if bullet_match:
          indent, _, rest = bullet_match.groups()
          new_line = f"{indent}- [ ] {rest}"
        else:
          # Just add it to the start of the line text (preserving any leading whitespace)
          indent_match = re.match(r"^(\s*)(.*)$", line_text)
          indent, rest = indent_match.groups()
          new_line = f"{indent}- [ ] {rest}"

      # Replace the text of the line
      self.view.replace(edit, line, new_line)