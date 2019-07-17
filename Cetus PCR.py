import constants as std
import functions
import interface


if __name__ == '__main__':
    cetus = interface.BaseWindow()
    functions.experiments = functions.open_pickle(std.exp_path)
    cetus.mainloop()

