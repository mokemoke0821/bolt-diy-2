# event_manager.py
import logging
from typing import Dict, Callable

class EventManager:
    def __init__(self, root):
        self.root = root
        self.bindings = {}
        self.callbacks = {}

    def register_callback(self, action: str, callback: Callable) -> None:
        self.callbacks[action] = callback

    def bind_shortcuts(self, settings: Dict[str, str]) -> None:
        self.unbind_all()
        
        used_keys = set()
        for action, key in settings.items():
            if key in used_keys:
                logging.warning(f"重複したショートカットキー: {key}")
                continue
            used_keys.add(key)
            self.bind_shortcut(action, key)

    def bind_shortcut(self, action: str, key: str) -> None:
        if action not in self.callbacks:
            logging.warning(f"未定義のアクション: {action}")
            return

        binding_id = self.root.bind(f'<{key}>', 
                                  lambda e: self.callbacks[action]())
        self.bindings[action] = binding_id

    def unbind_all(self) -> None:
        for binding_id in self.bindings.values():
            self.root.unbind('', binding_id)
        self.bindings.clear()