from Application.gui import Application
from Application.bracelet import Bracelet


def show_window(app):
    app.mainloop()


if __name__ == "__main__":
    bracelet = Bracelet()
    app = Application(bracelet)
    show_window(app)
