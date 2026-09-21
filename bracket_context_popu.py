import sublime
import sublime_plugin
import html

class BracketScopePopupListener(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        # Only trigger if there is exactly one cursor and no text selected
        sel = view.sel()
        if len(sel) != 1 or not sel[0].empty():
            view.hide_popup()
            return

        pt = sel[0].b
        
        # Look at the character immediately to the left and right of the cursor
        char_left = view.substr(pt - 1) if pt > 0 else ''
        char_right = view.substr(pt) if pt < view.size() else ''
        
        pairs = {'}': '{', ']': '[', ')': '('}
        
        char = None
        search_pt = -1
        
        # Verify it's a bracket and NOT inside a string or comment
        if char_left in pairs and not view.match_selector(pt - 1, 'string | comment'):
            char = char_left
            search_pt = pt - 2
        elif char_right in pairs and not view.match_selector(pt, 'string | comment'):
            char = char_right
            search_pt = pt - 1
            
        if not char:
            return
            
        target_open = pairs[char]
        target_close = char
        depth = 1
        
        # Safeguard to prevent freezing on massive minified files (searches ~100k chars back)
        max_search = 100000 
        
        while search_pt >= 0 and max_search > 0:
            # Ignore brackets inside strings or comments while searching backward
            if not view.match_selector(search_pt, 'string | comment'):
                c = view.substr(search_pt)
                
                if c == target_close:
                    depth += 1
                elif c == target_open:
                    depth -= 1
                    
                # We found the matching opening bracket
                if depth == 0:
                    open_line = view.line(search_pt)
                    visible_region = view.visible_region()
                    
                    # Only show the popup if the opening bracket is off-screen
                    if not visible_region.contains(open_line):
                        line_text = view.substr(open_line).strip()
                        
                        # Handle C-style bracing where `{` is alone on a line
                        # by grabbing the previous line (e.g. the actual `if(...)` statement)
                        if len(line_text) <= 1:
                            prev_pt = open_line.a - 1
                            if prev_pt > 0:
                                prev_line = view.line(prev_pt)
                                line_text = view.substr(prev_line).strip() + " " + line_text
                        
                        escaped = html.escape(line_text)
                        
                        # Use Sublime's minihtml to style the popup matching your color scheme
                        popup_html = f"""
                        <body id="bracket-popup">
                            <style>
                                body {{ 
                                    margin: 0; 
                                    padding: 6px 12px; 
                                    font-family: monospace; 
                                    background-color: color(var(--background) blend(blue 75%)); 
                                    border-radius: 4px;
                                }}
                                .code {{ color: var(--foreground); font-size: 1.1rem; }}
                            </style>
                            <div class="code">{escaped}</div>
                        </body>
                        """
                        
                        view.show_popup(
                            popup_html, 
                            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY | sublime.HIDE_ON_CHARACTER_EVENT, 
                            location=-1, 
                            max_width=800
                        )
                    break
            
            search_pt -= 1
            max_search -= 1