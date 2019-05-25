import interface
import functions


if __name__ == '__main__':
    cetus = interface.BaseWindow()
    functions.experiments = functions.open_pickle('experiments.pcr')
    cetus.mainloop()
