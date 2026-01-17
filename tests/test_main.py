import pytest
from unittest.mock import patch, MagicMock
import os
import json
import main

@pytest.fixture
def config_path():
    return os.path.join(main.BASE_DIR, "config.json")

@pytest.fixture
def sample_config():
    return {"weather-key": "test_key", "language": "En-US"}

@pytest.fixture(autouse=True)
def setup_and_teardown(config_path):
    # Backup existing config file if it exists
    if os.path.exists(config_path):
        os.rename(config_path, config_path + ".bak")
    yield
    # Restore original config file if it was backed up
    if os.path.exists(config_path + ".bak"):
        os.rename(config_path + ".bak", config_path)
    elif os.path.exists(config_path):
        os.remove(config_path)

# Context: Configuration Management
def test_save_config_creates_file(config_path, sample_config):
    main.save_config(("weather-key", "language"), ("test_key", "En-US"))
    assert os.path.exists(config_path)
    with open(config_path, "r") as f:
        config = json.load(f)
    assert config == sample_config

def test_load_config_existing_file(config_path, sample_config):
    with open(config_path, "w") as f:
        json.dump(sample_config, f)
    main.load_config()
    assert main.WEATHER_KEY == "test_key"
    assert main.LANGUAGE == "En-US"

def test_load_config_no_file(mocker):
    mock_tk = mocker.patch("main.Tk")
    mock_instance = mock_tk.return_value
    mock_instance.mainloop.return_value = None
    main.load_config()
    mock_tk.assert_called_once()

# Context: Language Settings
def test_set_language_updates_global():
    main.set_language("Es-ES")
    assert main.LANGUAGE == "Es-ES"
    assert main._("Hello") == "Hola"  # Assuming translations exist

# Context: Voice Assistant Functions
@patch("main.engine.say")
@patch("main.engine.runAndWait")
def test_talk_calls_engine(mock_run_and_wait, mock_say):
    main.talk("Hello")
    mock_say.assert_called_once_with("Hello")
    mock_run_and_wait.assert_called_once()

@patch("main.sr.Recognizer.recognize_google")
@patch("main.sr.Recognizer.listen")
@patch("main.sr.Microphone")
def test_listen_returns_command(mock_microphone, mock_listen, mock_recognize_google):
    mock_recognize_google.return_value = "test command"
    result = main.listen()
    assert result == "test command"

@patch("main.sr.Recognizer.recognize_google", side_effect=main.sr.UnknownValueError)
@patch("main.talk")
def test_listen_handles_unknown_value_error(mock_talk, mock_recognize_google):
    result = main.listen()
    assert result is None
    mock_talk.assert_called_once_with("Please repeat, I didn't understand that.")

# Context: Tray Icon Setup
@patch("main.Icon")
def test_setup_tray_icon_creates_icon(mock_icon):
    main.setup_tray_icon()
    mock_icon.assert_called_once_with("Barpsy Assistant", main.image, menu=pytest.ANY)
