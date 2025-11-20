from PySide6.QtWidgets import QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from digipage.ui.modes.base import BaseScanMode
from digipage.ui.viewer.canvas import ImageCanvas
from digipage.workers.image_worker import ImageProcessor

class DualScanModeWidget(BaseScanMode):
    """
    Standard mode: Displays two images side-by-side (Left Page, Right Page).
    """
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # This seems to be expecting a structure where viewer1 and viewer2 are dictionaries containing the viewer and toolbar
        # This matches MainWindow logic: self.viewer1 = self.current_ui_mode.viewer1

        from digipage.ui.widgets.image_viewer import ImageViewer
        from digipage.ui.panels.toolbar import ViewerToolbar
        from PySide6.QtWidgets import QStackedWidget, QVBoxLayout

        self.viewer1 = self._create_viewer_panel()
        self.viewer2 = self._create_viewer_panel()

        layout.addWidget(self.viewer1['frame'])
        layout.addWidget(self.viewer2['frame'])

    def _create_viewer_panel(self):
        from digipage.ui.widgets.image_viewer import ImageViewer
        from digipage.ui.panels.toolbar import ViewerToolbar
        from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        viewer = ImageViewer()
        toolbar = ViewerToolbar()

        # Link toolbar to viewer
        toolbar.zoom_in.connect(viewer.zoom_in)
        toolbar.zoom_out.connect(viewer.zoom_out)
        toolbar.fit_view.connect(viewer.reset_view)
        toolbar.rotate_left.connect(lambda: viewer.rotate(-90))
        toolbar.rotate_right.connect(lambda: viewer.rotate(90))
        toolbar.crop_mode.connect(lambda checked: viewer.set_cropping_mode(checked))

        frame_layout.addWidget(viewer)
        frame_layout.addWidget(toolbar)

        return {
            'frame': frame,
            'viewer': viewer,
            'toolbar': toolbar,
            'controls_stack': QStackedWidget() # Placeholder if needed
        }
