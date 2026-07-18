import os
import pytest
from app.plugins.manager import PluginManager
from app.plugins.base import PluginValidator

# We will create a dummy plugin file in the tests directory to ensure discovery works.
@pytest.fixture
def dummy_plugin_dir(tmp_path):
    d = tmp_path / "plugins"
    d.mkdir()
    
    # Create __init__.py
    (d / "__init__.py").write_text("")
    
    # Create the dummy plugin file
    plugin_code = """
from app.plugins.base import PluginValidator

class MockPlagiarismValidator(PluginValidator):
    def validate(self, doc, rule):
        from app.validators.base import ValidationResult
        return ValidationResult(passed_checks=1, failed_checks=0, issues=[])
"""
    (d / "mock_plugin.py").write_text(plugin_code)
    
    return str(d)

def test_plugin_discovery_and_loading(dummy_plugin_dir):
    manager = PluginManager(plugin_dir=dummy_plugin_dir)
    manager.discover_and_load()
    
    # Assert the mock plugin was discovered
    assert len(manager.loaded_plugins) == 1
    assert manager.loaded_plugins[0].__name__ == "MockPlagiarismValidator"
    
    # Assert we can instantiate it
    instances = manager.get_plugin_instances()
    assert len(instances) == 1
    assert instances[0].plugin_name == "MockPlagiarismValidator"
    assert instances[0].plugin_version == "1.0.0"
