from py4web import action, Reloader

class main_page(action):
    
    def __call__(self, func):
        """Building the decorator.  This decorator declares the page as the main page."""
        app_name = action.app_name
        if self.path[0] == "/":
            path = self.path.rstrip("/") or "/"
        else:
            base_path = "" if app_name == "_default" else f"/{app_name}"
            path = (f"{base_path}/{self.path}").rstrip("/")
        Reloader.register_route(app_name, path, self.kwargs, func)
        Reloader.register_route(app_name, "/", self.kwargs, func)
        return func
    
# @action("/hello")
# @topurlaction("/banana")
