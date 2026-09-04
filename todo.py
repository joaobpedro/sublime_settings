import sublime
import sublime_plugin

class TodoHighlighterListener(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        self.update_highlights(view)

    def on_load_async(self, view):
        self.update_highlights(view)

    def update_highlights(self, view):
        # Skip files over 1MB to prevent background performance hiccups
        if view.size() > 1000000:
            return

        # Dictionary of tag groups. 
        # The 'scope' determines the color pulled from your current color scheme.
        tags = {
            "highlight_info": {
                "pattern": r"\b(TODO|NOTE|INFO)\b",
                "scope": "markup.inserted"  # Usually renders green
            },
            "highlight_error": {
                "pattern": r"\b(FIXME|BUG|XXX)\b",
                "scope": "invalid"          # Usually renders bright red
            },
            "highlight_warning": {
                "pattern": r"\b(HACK|HARDCODED|WARN)\b",
                "scope": "markup.changed"   # Usually renders yellow/orange
            }
        }

        for key, config in tags.items():
            # Find all matching text regions in the file
            regions = view.find_all(config["pattern"])
            
            # Apply the regions to the view. 
            # Overwriting an existing key updates the regions automatically.
            # Passing an empty list automatically clears them.
            view.add_regions(
                key, 
                regions, 
                config["scope"], 
                "dot", # Adds a visual dot in the line number gutter
                sublime.DRAW_NO_OUTLINE
            )