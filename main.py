import ui
import levels
import wx


class Main:
    def __init__(self):
        app = wx.App()
        self.window = ui.MainWindow(parent=None, id=wx.ID_ANY)
        self.window.Show()

        #read unlocked level
        try:
            f = open("unlocked_level.txt", 'r')
        except IOError:
            self.unlocked_level = 1
        else:
            self.unlocked_level = int(f.readline())
            f.close()

        self.load_level(self.get_max_available_level())
        self.window.set_level_list(self.get_max_available_level(), self.current_level)
        self.update_next_button()
        
        self.window.Bind(wx.EVT_BUTTON, self.check, self.window.check_button)
        self.window.Bind(wx.EVT_BUTTON, self.load_next_level, self.window.next_button)
        self.window.Bind(wx.EVT_CHOICE, self.change_level, self.window.level_selector)
        
        app.MainLoop()


    def change_level(self, event):
        level = event.GetSelection()+1
        if level != self.current_level:  #don't reload the current one
            self.load_level(level)
    

    def load_next_level(self, event):
        self.load_level(self.current_level + 1)


    def load_level(self, nr):
        index = nr-1
        if not levels.list[index]:
            return

        self.current_level = nr
        
        #transform the level string into a list and pass it to the window
        lines = levels.list[index].splitlines()
        nr_rows = len(lines)
        nr_columns = 0
        values = []
        
        for line in lines:
            columns = line.split()
            nr_columns = max(nr_columns, len(columns))
            for value in columns:
                values.append(value)
                
        self.window.set_values(values, nr_columns, nr_rows)
        self.window.set_level_list(self.get_max_available_level(), self.current_level)
        self.update_next_button()
        

    def set_unlocked_level(self, nr):
        self.unlocked_level = nr
        self.window.set_level_list(self.get_max_available_level(), self.current_level)
        self.update_next_button()


    def get_max_available_level(self):
        return min(self.unlocked_level, len(levels.list))


    def update_unlocked_level(self, nr):
        self.set_unlocked_level(nr)
        
        f = open("unlocked_level.txt", 'w')
        f.write(str(nr))
        f.close()


    def update_next_button(self):
        self.window.enable_next_level(self.current_level < self.unlocked_level)


    def check(self, event):
        values, puzzle_length = self.window.get_values()

        for row_nr, row in enumerate(values):
            for column_nr, cell in enumerate(row):
                valid = self.check_cell(row_nr, column_nr, values, puzzle_length)
                if not valid:
                    wx.MessageBox("The puzzle is not complete.", "Plase try again", wx.OK|wx.ICON_WARNING)
                    return

        wx.MessageBox("Puzzle Completed!", "Congratulations!", wx.OK|wx.ICON_INFORMATION)
        if self.unlocked_level == self.current_level:
            self.update_unlocked_level(self.unlocked_level+1)

    
    #checks if all cells respect Hidato's consecutive rule
    def check_cell(self, row_nr, column_nr, values, puzzle_length):
        cell = values[row_nr][column_nr]

        #cells not part of the puzzle are ok by default
        if cell == levels.CELL_NONE: return True
        if cell == levels.CELL_EMPTY: return False
        
        cell = int(cell)
        if cell == puzzle_length: return True
        
        for i in range(row_nr-1, row_nr+2):
            for j in range(column_nr-1, column_nr+2):
                
                #validity checks for the neighbour
                if i >= 0 and i < len(values) and \
                   j >= 0 and j < len(values[i]) and \
                   values[i][j] != levels.CELL_NONE and values[i][j] != levels.CELL_EMPTY:
                    
                    #the consecutive check
                    if int(values[i][j]) == cell+1:
                        return True
                    
        return False

    
if __name__=='__main__':
    main = Main()
