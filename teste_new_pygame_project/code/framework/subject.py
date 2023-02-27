class Subject:
    
    def __init__(self):
        self.observers = []
    
    def notify_all_observers(self, action):
        for observer in self.observers:
            observer.on_notify(action)
        
    def notify_observer(self, observer, action):
        observer.on_notify(action)
    
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
    