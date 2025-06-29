import json
import os
from datetime import datetime

from SetupPordaApp import PordaAppDir

from .EngineSetting import get_engines

default_settings = {
    "accuracy": 25,
    "network_width": 17,
    "network_height": 10,
    "active_timeout": 65,
    "sleep_timeout": 500,
    "keep_running_timeout": 10,
    "engine": "CPU Engine",
    "hardware_accelerated": True,
    "is_priority_realtime": False,
    "cover": "Bg Color",
    "is_blur": True,
    "is_bg_color": False,
    "is_color": False,
    "rgb_color_value": "(0,0,255)",
    "object": "Female",
    "is_detect_male": False,
    "is_detect_female": True,
    "cover_index": 0,
    "blur_kernel": 140,
    "obj_list": [1],
    "activity_status": True,
    "auto_startup": True,
    "startup_lagacy": True,
    "shortcut_key": "f2",
    "capture_screenshot": "f1",
    "dataset_path": os.path.join(PordaAppDir(), "PordaAi", "Dataset"),
    "initial_request_sent": False,
    "user_session": "",
    "is_all_window": False,
    "is_include_window": True,
    "is_exclude_window": False,
    "include_windows": "chrome.exe, msedge.exe, brave.exe, firefox.exe, opera.exe, PotPlayerMini64.exe, vlc.exe,",
    "exclude_windows": "explorer.exe, cmd.exe, winword.exe, pordaai.exe",
    "always_skip_windows": [
        ("explorer.exe", "Progman"),
        ("explorer.exe", "WorkerW"),
        ("explorer.exe", "Shell_TrayWnd"),
        ("explorer.exe", "LauncherTipWnd"),
        ("explorer.exe", "SystemTray_Main"),
        ("explorer.exe", "NotifyIconOverflowWindow"),
        ("ShellExperienceHost.exe", "Shell_TrayWnd"),
        ("ShellExperienceHost.exe", "Windows.UI.Core.CoreWindow"),
        ("SearchApp.exe", "Windows.UI.Core.CoreWindow"),
    ],
    "is_gpu_setup_properly": False,
    "is_allow_max_cpu_limit": False,
    "max_cpu_limit": 90,
    "average_reading_interval": 30,
    "last_message_shown": datetime.now().strftime("%Y-%m-%d"),
}


def cover_list() -> list[str]:
    """
    Returns a list of available cover options.
    Returns:
        list[str]: A list containing the names of cover styles.
    """

    values = ["Black", "White", "Bg Color", "Blur", "Mosaic"]
    return values


def object_list() -> list[str]:
    """
    Returns a list of predefined object categories.
    Returns:
        list[str]: A list of strings representing different object categories, such as gender and clothing attributes.
    """

    values = [
        "Male",
        "Female",
        "Female without Hijab",
        "Female without Borka",
        "Only NSFW",
        "All Human",
    ]
    return values


def engine_list() -> list[str]:
    """
    Retrieves a list of available engine names.
    Returns:
        list: A list of strings representing the available engines.
    """

    # "Dedicated GPU","Integrated GPU",
    values = get_engines()  # ["CPU Engine","Hp Elitbook G3"] + get_gpu_list()
    return values


def get_gpu_list() -> list[str]:
    """
    Retrieves a list of available GPU device names using the pyopencl library.
    Attempts to import pyopencl and enumerate all GPU devices across all available platforms.
    If an error occurs (e.g., pyopencl is not installed or no GPUs are found), returns a list containing "Got Error".
    Returns:
        list[str]: A list of GPU device names, or ["Got Error"] if an error occurs.
    """

    li = []
    try:
        import pyopencl as cl

        platforms = cl.get_platforms()
        for i, platform in enumerate(platforms):
            devices = platform.get_devices()
            for j, device in enumerate(devices):
                li.append(device.name)
    except Exception as e:
        print("Got error when finding gpu", e)
        li = ["Got Error"]
    return li


def load_settings() -> dict:
    """
    Loads application settings from a JSON file. If the settings file is missing, invalid, or inaccessible,
    it falls back to default settings and attempts to save them. Ensures all default keys are present in the
    returned settings dictionary.
    Returns:
        dict: The loaded or default settings as a dictionary.
    """

    # As I already created pordaAi folder, if i use base_path then the programme will look for pyinstaller temp folder
    porda_app_dir = PordaAppDir()

    settings_file_path = os.path.join(porda_app_dir, "pordaAi", "settings.json")

    try:
        with open(settings_file_path, "r") as f:
            settings = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        settings = default_settings
        save_settings(
            settings
        )  # Save the default settings if the file is missing or invalid
    except PermissionError as e:
        print(f"Permission Denied while loading settings: {e}")
        settings = default_settings
    except Exception as e:
        print(f"An error occurred while loading settings: {e}")
        settings = default_settings

    # Update settings with defaults for missing keys
    for key, value in default_settings.items():
        settings.setdefault(key, value)

    return settings


def save_settings(settings) -> None:
    """
    Saves the provided settings dictionary to a JSON file in the application's settings directory.
    Args:
        settings (dict): A dictionary containing the settings to be saved.
    Returns:
        None
    Raises:
        PermissionError: If the program does not have permission to write to the settings file.
        Exception: For any other errors that occur during the file write operation.
    Notes:
        If a PermissionError occurs, the function prints an error message and optionally resets settings to default.
        For any other exceptions, an error message is printed.
    """

    porda_app_dir = PordaAppDir()
    try:
        settings_file_path = os.path.join(porda_app_dir, "pordaAi", "settings.json")

        with open(settings_file_path, "w") as f:
            json.dump(settings, f)

    except PermissionError as e:
        print(f"Permission Denied while saving settings: {e}")
        # Optionally, you can choose to use default settings or take other actions here
        # For example, you can set settings to default_settings
        settings = default_settings
    except Exception as e:
        print(f"An error occurred while saving settings: {e}")
