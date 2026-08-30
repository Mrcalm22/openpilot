import pyray as rl
from openpilot.system.ui.lib.application import gui_app, FontWeight, FONT_SCALE
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.lib.wrap_text import wrap_text
from openpilot.system.ui.widgets import Widget
from openpilot.system.ui.widgets.button import Button, ButtonStyle


class SetupWidget(Widget):
  def __init__(self):
    super().__init__()
    self._open_settings_callback = None
    self._open_settings_btn = Button(lambda: tr("Open"), lambda: self._open_settings_callback() if self._open_settings_callback else None,
                                     button_style=ButtonStyle.PRIMARY)

  def set_open_settings_callback(self, callback):
    self._open_settings_callback = callback

  def _render(self, rect: rl.Rectangle):
    self._render_status_prompt(rect)

  def _render_status_prompt(self, rect: rl.Rectangle):
    rl.draw_rectangle_rounded(rl.Rectangle(rect.x, rect.y, rect.width, rect.height), 0.03, 20, rl.Color(51, 51, 51, 255))

    x = rect.x + 64
    y = rect.y + 48
    w = rect.width - 128

    font = gui_app.font(FontWeight.BOLD)
    rl.draw_text_ex(font, tr("Ready"), rl.Vector2(x, y), 75, 0, rl.WHITE)
    y += 113  # 75 + 38 spacing

    desc = tr("Review driving settings, device status, and software updates.")
    light_font = gui_app.font(FontWeight.NORMAL)
    wrapped = wrap_text(light_font, desc, 50, int(w))
    for line in wrapped:
      rl.draw_text_ex(light_font, line, rl.Vector2(x, y), 50, 0, rl.WHITE)
      y += 50 * FONT_SCALE

    button_rect = rl.Rectangle(x, y + 30, w, 200)
    self._open_settings_btn.render(button_rect)
