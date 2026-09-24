import sublime
import sublime_plugin

class EmacsTransposeWordsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        new_sel = []

        # Process selections in reverse to prevent replacement coordinate shifting
        for region in reversed(view.sel()):
            # If the user has highlighted text, ignore the Emacs behavior
            if not region.empty():
                new_sel.append(region)
                continue

            pt = region.b
            
            # 1. Find the start of the next word (or current word if pt is at the start)
            next_word_start = pt
            if not (view.classify(next_word_start) & sublime.CLASS_WORD_START):
                next_word_start = view.find_by_class(next_word_start, True, sublime.CLASS_WORD_START)
            
            if next_word_start is None or next_word_start >= view.size():
                new_sel.append(region)
                continue
                
            word2 = view.word(next_word_start)
            
            # 2. Find the previous word
            prev_word_end = view.find_by_class(word2.begin(), False, sublime.CLASS_WORD_END)
            if prev_word_end is None or prev_word_end <= 0:
                new_sel.append(region)
                continue
                
            word1 = view.word(prev_word_end - 1)
            
            # Ensure we actually have two distinct words in proper order
            if word1.begin() >= word2.begin():
                new_sel.append(region)
                continue

            # 3. Extract strings and execute the swap
            word1_text = view.substr(word1)
            word2_text = view.substr(word2)
            
            between_region = sublime.Region(word1.end(), word2.begin())
            between_text = view.substr(between_region)

            replace_region = sublime.Region(word1.begin(), word2.end())
            replacement = word2_text + between_text + word1_text
            
            view.replace(edit, replace_region, replacement)

            # Move cursor past the newly transposed words to allow rapid consecutive swapping
            new_pt = replace_region.begin() + len(replacement)
            new_sel.append(sublime.Region(new_pt, new_pt))

        # Apply the new cursor coordinates
        if new_sel:
            view.sel().clear()
            for s in reversed(new_sel):
                view.sel().add(s)
            view.show(view.sel())