from sys import argv, stdin
from pytube import YouTube, exceptions
from urllib.error import HTTPError

import customtkinter as ctk


def download(url: str) -> tuple:
    """Downloads a YouTube video based on the specified URL.

    :param url: str, the URL of the YouTube video
    :return: A str representing whether the download was successful or not
    """
    try:
        youtube = YouTube(url)
        video = youtube.streams.filter(progressive=True).last()
        video.download("./videos/")
        return ("Video downloaded successfully.", "green")
    except HTTPError:
        return ("Invalid URL (HTTPError).", "red")
    except exceptions.RegexMatchError:
        return ("Invalid URL (RegexMatchError).", "red")
    except Exception as e:
        return (f"An unknown error occurred: {e}\nPlease try again later.", "red")

def download_from_entry() -> None:
    """Called when the download is called from the GUI.
    Downloads the YouTube video based on the URL entered in the input field 'input_url'.
    """
    message, color = download(input_url.get())
    label_message.configure(text=message, text_color=color)


def create_gui():
    """Creates a CTk GUI
    """
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    tk_width = 400
    tk_height = 250
    screen_width = (root.winfo_screenwidth() // 2) - (tk_width // 2)
    screen_height = (root.winfo_screenheight() // 2) - (tk_height // 2)
    root.geometry(f"{tk_width}x{tk_height}+{screen_width}+{screen_height}")

    frame = ctk.CTkFrame(master=root)
    frame.pack_configure(pady=20, padx=20, fill="both", expand=True)

    label_title = ctk.CTkLabel(master=frame, text="YouTube URL")
    label_title.pack_configure(pady=10, padx=10)

    global input_url
    input_url = ctk.CTkEntry(master=frame, placeholder_text="Enter URL here...", width=300)
    input_url.pack_configure(pady=10, padx=10)

    button_download = ctk.CTkButton(master=frame, text="Download", command=download_from_entry)
    button_download.pack_configure(pady=10, padx=10)

    global label_message
    label_message = ctk.CTkLabel(master=frame, text="")
    label_message.pack_configure(pady=10, padx=10)

    root.mainloop()


# Check if the script is run interactively or from the command line
if len(argv) > 1:
    print(argv)
    # Download using link from argv
    print(download(argv[1]))
elif stdin.isatty():
    # Running interactively (e.g. in IDE)
    create_gui()
else:
    # Running without arguments but not interactively
    print("No URL provided.")
