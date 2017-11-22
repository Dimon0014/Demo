#!/usr/bin/env python

import sys

import wx

import ColorPanel
import GridSimple
import ListCtrl
import ScrolledWindow
import images

#----------------------------------------------------------------------------
class PageOne(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            self.SetBackgroundColour(wx.BLUE)
           # t = wx.StaticText(self, -1, "This is a PageOne object", (20, 20))

          #  t = wx.StaticText(self, -1,
          #                    "You can put nearly any type of window here,\n"
          #                   "and if the platform supports it then the\n"
          #                   "tabs can be on any side of the notebook.",
          #                   (10, 10))
           # t.SetForegroundColour(wx.WHITE)
           # t.SetBackgroundColour(wx.BLUE)


class MyApp(wx.App):

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, wx.ID_ANY, title='My Title')
        self.panel = wx.Panel(self.frame, wx.ID_ANY)
        self.notebook = wx.Notebook(self.panel, wx.ID_ANY)
        #log= self.log.startLogging(sys.stdout)
        #p = wx.Panel(self)
    # def __init__(self, parent, log):
        self.log = wx.Log

    #     wx.Panel.__init__(self, parent, -1)






    # def __init__(self, parent, id, log):
    #      wx.Notebook.__init__(self, parent, id, size=(21,21), style=
    #                           wx.BK_DEFAULT
    #                           #wx.BK_TOP
    #                           #wx.BK_BOTTOM
    #                           #wx.BK_LEFT
    #                           #wx.BK_RIGHT
    #                           # | wx.NB_MULTILINE
    #                           )

# class PageOne(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self.notebook, -1, "This is a PageOne object", (20, 20))
#

        # page1 = PageOne(self.notebook)
        # self.notebook.AddPage(page1, "Page 1")
        win = self.makeColorPanel(wx.BLUE)
        #page2 = PageOne(win)
        #self.notebook.AddPage(page2, "Page 2")
        self.notebook.AddPage(win, "Blue")
        st = wx.StaticText(win.win, -1,
                             "You can put nearly any type of window here,\n"
                            "and if the platform supports it then the\n"
                            "tabs can be on any side of the notebook.",
                             (10, 10))

        st.SetForegroundColour(wx.WHITE)
        st.SetBackgroundColour(wx.BLUE)

        # Show how to put an image on one of the notebook tabs, # смайл на табе
        # first make the image list:
        il = wx.ImageList(16, 16)                              # смайл на табе
        idx1 = il.Add(images.Smiles.GetBitmap())               # смайл на табе
        self.notebook.AssignImageList(il)                      # смайл на табе

        # now put an image on the first tab we just created: # кладем смайл на таб который только что сделали
        self.notebook.SetPageImage(0, idx1)

        #
        win = self.makeColorPanel(wx.RED)
        self.notebook.AddPage(win, "Red")
        #
        win = ScrolledWindow.MyCanvas(self.notebook)
        self.notebook.AddPage(win, 'ScrolledWindow')

        win = self.makeColorPanel(wx.GREEN)
        self.notebook.AddPage(win, "Green")
        #
        win = GridSimple.SimpleGrid(self.notebook, self.log) # ВТОРОЙ АРГУМЕНТ 10 -  на шару вбил
        self.notebook.AddPage(win, "Grid")
# ВСЕ РАБОТАЕТ ДО СИХ ПОР
        win = ListCtrl.TestListCtrlPanel(self.notebook, self.log)  # ВТОРОЙ АРГУМЕНТ 1 -  на шару вбил
        self.notebook.AddPage(win, 'List')
        #
        win = self.makeColorPanel(wx.CYAN)
        self.notebook.AddPage(win, "Cyan")
        #
        win = self.makeColorPanel(wx.Colour('Midnight Blue'))
        self.notebook.AddPage(win, "Midnight Blue")
        #
        win = self.makeColorPanel(wx.Colour('Indian Red'))
        self.notebook.AddPage(win, "Indian Red")

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)


        self.frame.Show()  # этой строки не было

    # class PageOne(wx.Panel):
    #     def __init__(self, parent):
    #         wx.Panel.__init__(self, parent)
    #         t = wx.StaticText(self, -1, "This is a PageOne object", (20, 20))
    #
    def makeColorPanel(self, color):
            p = wx.Panel(self.notebook, -1)
            win = ColorPanel.ColoredPanel(p, color)
            #win = p.SetBackgroundColour(color)
            p.win = win # здесь у p появляется свойство цвета
            def OnCPSize(evt, win=win):
                 win.SetPosition((0,0))
                 win.SetSize(evt.GetSize())
            p.Bind(wx.EVT_SIZE, OnCPSize)
            return p

    #
    def OnPageChanged(self, event):
         if self:
             old = event.GetOldSelection()
             new = event.GetSelection()
             #sel = self.GetSelection()
             sel=0
             #self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
         event.Skip()
    #
    def OnPageChanging(self, event):
         if self:
             old = event.GetOldSelection()
             new = event.GetSelection()
             #sel = self.GetSelection()
             sel = 0
             #self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
         event.Skip()

#----------------------------------------------------------------------------
#
# def runTest(frame, nb, log):
#     testWin = TestNB(nb, -1, log)
#     return testWin

#----------------------------------------------------------------------------


overview = """\
<html><body>
<h2>wx.Notebook</h2>
<p>
This class represents a notebook control, which manages multiple
windows with associated tabs.
<p>
To use the class, create a wx.Notebook object and call AddPage or
InsertPage, passing a window to be used as the page. Do not explicitly
delete the window for a page that is currently managed by wx.Notebook.

"""


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()






