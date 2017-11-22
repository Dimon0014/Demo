#!/usr/bin/env python

import wx

from wx.lib.activexwrapper import MakeActiveXClass
import win32com.client.gencache
browserModule = win32com.client.gencache.EnsureModule(
    "{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}", 0, 1, 1)


#----------------------------------------------------------------------

class TestPanel(wx.Window):
    def __init__(self, parent, frame=None):
        wx.Window.__init__(self, parent)
        self.ie = None
        self.current = "http://wxPython.org/"
        self.frame = frame
        if frame:
            self.titleBase = frame.GetTitle()


        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Make a new class that derives from the WebBrowser class in the
        # COM module imported above.  This class also derives from wxWindow and
        # implements the machinery needed to integrate the two worlds.
        theClass = MakeActiveXClass(browserModule.WebBrowser, eventObj=self)

        # Create an instance of that class
        self.ie = theClass(self, -1)


        btn = wx.Button(self, wx.NewId(), "Open", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "Home", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnHomeButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "<--", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "-->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "Stop", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "Search", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnSearchPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Location:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(self, wx.NewId(), "", style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.ie, 1, wx.EXPAND)

        self.ie.Navigate2(self.current)
        self.location.Append(self.current)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)



    def OnDestroy(self, evt):
        if self.ie:
            self.ie.Cleanup()
            self.ie = None
            self.frame = None


    def OnSize(self, evt):
        self.Layout()


    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.ie.Navigate2(url)

    def OnLocationKey(self, evt):
        if evt.KeyCode() == wx.WXK_RETURN:
            URL = self.location.GetValue()
            self.location.Append(URL)
            self.ie.Navigate2(URL)
        else:
            evt.Skip()

    def IgnoreReturn(self, evt):
        if evt.KeyCode() != wx.WXK_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, "Open Location",
                                "Enter a full URL or local path",
                                self.current, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.ie.Navigate2(self.current)
        dlg.Destroy()

    def OnHomeButton(self, event):
        self.ie.GoHome()

    def OnPrevPageButton(self, event):
        self.ie.GoBack()

    def OnNextPageButton(self, event):
        self.ie.GoForward()

    def OnStopButton(self, evt):
        self.ie.Stop()

    def OnSearchPageButton(self, evt):
        self.ie.GoSearch()

    def OnRefreshPageButton(self, evt):
        self.ie.Refresh2(3)



    # The following event handlers are called by the web browser COM
    # control since  we passed self to MakeActiveXClass.  It will look
    # here for matching attributes and call them if they exist.  See the
    # module generated by makepy for details of method names, etc.
    def OnNavigateComplete2(self, pDisp, URL):
        self.current = URL
        self.location.SetValue(URL)

    def OnTitleChange(self, text):
        if self.frame:
            self.frame.SetTitle(self.titleBase + ' -- ' + text)

    def OnStatusTextChange(self, text):
        if self.frame:
            self.frame.SetStatusText(text)


#----------------------------------------------------------------------


if __name__ == '__main__':
    class TestFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, -1, "ActiveX test -- Internet Explorer",
                             size=(640, 480))
            self.CreateStatusBar()
            self.tp = TestPanel(self, frame=self)
            self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        def OnCloseWindow(self, evt):
            self.tp.Destroy()
            self.Destroy()

    app = wx.App()
    frame = TestFrame()
    frame.Show(True)

    import wx.py
    shell = wx.py.shell.ShellFrame(frame, size=(640,480),
                                   locals=dict(wx=wx, frame=frame, ie=frame.tp.ie))
    shell.Show()
    frame.Raise()
    app.MainLoop()



