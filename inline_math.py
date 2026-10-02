import sublime
import sublime_plugin

class EvaluateMathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty(): continue
            text = self.view.substr(region).strip()
            try:
                # Safely evaluate the math string
                result = eval(text, {"__builtins__": None}, {})
                
                # Format: remove decimals if it's a whole number, otherwise round to 2 decimal places
                if isinstance(result, float):
                    if result.is_integer():
                        res_str = str(int(result))
                    else:
                        res_str = f"{round(result, 2)}"
                else:
                    res_str = str(result)
                    
                self.view.replace(edit, region, res_str)
            except Exception:
                pass # Skip if it's not valid math