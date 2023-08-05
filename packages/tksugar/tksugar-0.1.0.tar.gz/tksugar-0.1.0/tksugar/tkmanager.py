class TkManager(object):
  """
  Manager object for managing widgets generated by the `tksugar.Generator` object.
  Manages IDs and event handlers, and manages variables.
  """
  def __init__(self, window, widgets, vars):
    """
    Constructor

    Parameters
    ----
    window: Tk
      Tk window object
    widgets: list[TagData]
      An array of TagData objects containing widgets with ids.
    vars: dict[str, Variable]
      A dictionary containing widget variables declared by tags.
    """
    self._window = window
    self.widgets = {}
    self.vars = vars
    for tagdata in widgets:
      tagdata.tag = {
        "tag": tagdata.tag
      }
      if not tagdata.id in self.widgets:
        self.widgets[tagdata.id] = tagdata

  def mainloop(self):
    """
    Call the window's main loop.
    """
    self._window.mainloop()