from ctypes import windll


def show_message(ms) -> None:
    """
    Displays a system modal message box with a check mark icon and plays a notification sound.
    Args:
        ms (str): The message to display in the message box.
    Returns:
        None
    """
    user32 = windll.user32
    user32.MessageBeep(0x00000040)
    # Display a "Saved Done" notification as a system modal window with a check mark icon
    user32.MessageBoxW(0, ms, "Porda Ai Message", 0x40 | 0x1000)


def make_notification_sound() -> None:
    """
    Plays a notification sound using the Windows API.
    Returns:
        None
    """
    user32 = windll.user32
    user32.MessageBeep(0x00000040)
