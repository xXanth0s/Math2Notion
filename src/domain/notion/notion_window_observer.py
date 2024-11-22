import threading
import time
from rx.subject import BehaviorSubject

# Platform-specific imports
import platform
if platform.system() == 'Darwin':  # macOS
    from AppKit import NSWorkspace
elif platform.system() == 'Windows':
    import pygetwindow as gw

class NotionWindowObserver:
    def __init__(self, poll_interval: float):
        self.poll_interval = poll_interval
        self.stop_event = threading.Event()
        self.subject = BehaviorSubject(self.check_if_app_in_foreground())

    def check_if_app_in_foreground(self):
        if platform.system() == 'Darwin':  # macOS
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            return active_app is not None and "Notion" in active_app['NSApplicationName']
        else:  # Windows
            active_window_title = gw.getActiveWindow()
            return active_window_title and "Notion" in str(active_window_title)

    def poll_application_status(self):
        while not self.stop_event.is_set():
            new_app_in_foreground = self.check_if_app_in_foreground()
            if new_app_in_foreground != self.subject.value:
                self.subject.on_next(new_app_in_foreground)
            time.sleep(self.poll_interval)

    def start_polling(self):
        self.polling_thread = threading.Thread(target=self.poll_application_status)
        self.polling_thread.start()

    def stop_polling(self):
        print("Stopping...")
        self.stop_event.set()
        self.subject.on_completed()
        print("Stopped.")

    def get_observable(self):
        return self.subject