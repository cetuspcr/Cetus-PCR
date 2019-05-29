import interface
import functions
import constants as std


if __name__ == '__main__':
    cetus = interface.BaseWindow()
    functions.experiments = functions.open_pickle(std.exp_path)
    cetus.mainloop()
