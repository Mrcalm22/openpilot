import pyray as rl

from openpilot.common.params import Params
from openpilot.system.ui.lib.application import gui_app, FontWeight
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.wrap_text import wrap_text
from openpilot.system.ui.widgets import Widget
from openpilot.system.ui.widgets.label import gui_label


class HomeStatusWidget(Widget):
  """Home screen status panel for Turbopilot."""

  BG_COLOR = rl.Color(51, 51, 51, 255)
  MUTED = rl.Color(178, 178, 178, 255)

  def __init__(self):
    super().__init__()
    self._params = Params()

  def _render(self, rect):
    rl.draw_rectangle_rounded(rect, 0.025, 10, self.BG_COLOR)

    x, y = rect.x + 80, rect.y + 75
    w = rect.width - 160

    gui_label(rl.Rectangle(x, y, w, 90), tr("Turbopilot"), 75, font_weight=FontWeight.BOLD)

    desc_y = y + 125
    font = gui_app.font(FontWeight.NORMAL)
    description = tr("Local driving assistance with device data kept on this unit unless you choose otherwise.")
    for line in wrap_text(font, description, 44, int(w)):
      rl.draw_text_ex(font, line, rl.Vector2(x, desc_y), 44, 0, self.MUTED)
      desc_y += 54

    rows = [
      (tr("Version"), self._params.get("UpdaterCurrentDescription") or self._params.get("Version") or tr("Unknown")),
      (tr("Branch"), self._params.get("GitBranch") or tr("Unknown")),
      (tr("Device ID"), self._params.get("DongleId") or tr("N/A")),
      (tr("Cloud"), tr("Disabled")),
    ]

    row_y = desc_y + 45
    for label, value in rows:
      gui_label(rl.Rectangle(x, row_y, 220, 58), label, 42, color=self.MUTED, font_weight=FontWeight.MEDIUM)
      gui_label(rl.Rectangle(x + 250, row_y, w - 250, 58), value, 42, alignment=rl.GuiTextAlignment.TEXT_ALIGN_RIGHT)
      row_y += 72
