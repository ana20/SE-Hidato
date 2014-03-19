import wx
import wx.lib.intctrl as intctrl
import levels


class MainWindow(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent=parent, id=id, title="Hidato")

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(frame_sizer)


        puzzle_panel = wx.Panel(self, style=wx.BORDER_SIMPLE)
        frame_sizer.Add(puzzle_panel, 1, wx.EXPAND)
        puzzle_sizer = wx.GridSizer()
        puzzle_panel.SetSizer(puzzle_sizer)


        controls_panel = wx.Panel(self)
        frame_sizer.Add(controls_panel, 0, wx.EXPAND)
        controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controls_panel.SetSizer(controls_sizer)

        check_button = wx.Button(controls_panel, label="Check")
        controls_sizer.Add(check_button, 0, wx.EXPAND)
        
        next_button = wx.Button(controls_panel, label="Next Level")
        controls_sizer.Add(next_button, 0, wx.EXPAND)

        level_selector = wx.Choice(controls_panel)
        controls_sizer.Add(level_selector, 0, wx.EXPAND)


        #export necesary controls
        self.puzzle_panel = puzzle_panel
        self.puzzle_sizer = puzzle_sizer
        self.level_selector = level_selector
        self.check_button = check_button
        self.next_button = next_button
        

    
    def clear_grid(self):
        self.puzzle_sizer.Clear(True)

    
    def set_grid_size(self, width, height):
        self.puzzle_sizer.SetCols(width)
        self.puzzle_sizer.SetRows(height)
        

    def refresh(self):
        self.puzzle_sizer.Layout()
        self.Fit()
        

    def add_cell(self, value):
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
        if value == levels.CELL_NONE:
            cell = wx.StaticText(self.puzzle_panel, style=wx.ALIGN_CENTRE_HORIZONTAL, label="")
        elif value == levels.CELL_EMPTY:
            cell = intctrl.IntCtrl(self.puzzle_panel, style=wx.TE_CENTRE, limited=True, min=1, allow_none=True, value=None)
        else:
            cell = wx.StaticText(self.puzzle_panel, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.BORDER_SIMPLE, label=value)

        cell.SetFont(font)   
        cell.SetMinSize(wx.Size(30,30))
        self.puzzle_sizer.Add(cell, 0, wx.EXPAND)


    def set_values(self, values, nr_columns, nr_rows):
        self.clear_grid()
        self.set_grid_size(nr_columns, nr_rows)
        for value in values:
            self.add_cell(value)
        self.refresh()


    def get_values(self):
        values = []
        puzzle_length = 0
        
        for item_nr, item in enumerate(self.puzzle_sizer.GetChildren()):
            cell = item.GetWindow()

            #the sizer gives us a list, but we need to split into rows for the cell checks
            if item_nr % self.puzzle_sizer.GetCols() == 0:
                row = []
                values.append(row)
            
            if isinstance(cell, wx.StaticText): #we need to check object type because they use different methods
                if cell.GetLabel() == "":
                    row.append(levels.CELL_NONE)
                else:
                    row.append(cell.GetLabel())
                    puzzle_length +=1
            elif isinstance(cell, intctrl.IntCtrl):
                if cell.GetValue() == None:
                    row.append(levels.CELL_EMPTY)
                else:
                    row.append(int(cell.GetValue()))
                puzzle_length +=1
            
        return values, puzzle_length


    def set_level_list(self, max_level, current_level):
        self.level_selector.Clear()
        for i in range(max_level):
            self.level_selector.Append("Level "+str(i+1))
        self.level_selector.SetSelection(current_level-1)


    def enable_next_level(self, b_enable):
        self.next_button.Enable(b_enable)



#Interface test
if __name__=='__main__':
    app = wx.App()
    window = MainWindow(parent=None, id=wx.ID_ANY)
    window.Show()
    
    app.MainLoop()
