import os
import importlib.util
import inspect
from typing import List, Type
from app.plugins.base import PluginValidator

class PluginManager:
    """
    Scans the plugins directory and dynamically loads any classes
    that inherit from PluginValidator.
    """
    def __init__(self, plugin_dir: str = None):
        if plugin_dir is None:
            self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.plugin_dir = plugin_dir
            
        self.loaded_plugins: List[Type[PluginValidator]] = []

    def discover_and_load(self):
        """Scans the plugin directory and loads discovered plugins"""
        self.loaded_plugins = []
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename not in ["__init__.py", "base.py", "manager.py"]:
                module_name = filename[:-3]
                module_path = os.path.join(self.plugin_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Inspect module for PluginValidator subclasses
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, PluginValidator) and obj != PluginValidator:
                            self.loaded_plugins.append(obj)

    def get_plugin_instances(self) -> List[PluginValidator]:
        """Returns instantiated objects for all loaded plugins"""
        return [plugin_class() for plugin_class in self.loaded_plugins]
