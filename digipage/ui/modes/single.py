from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from digipage.ui.modes.base import BaseScanMode
from digipage.ui.viewer.canvas import ImageCanvas
from digipage.workers.image_worker import ImageProcessor

class SingleSplitModeWidget(BaseScanMode):
    """
    Single-Shot mode: Displays one image.
    User defines crop boxes, system auto-splits.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        from digipage.ui.widgets.image_viewer import ImageViewer
        from digipage.ui.panels.toolbar import ViewerToolbar

        self.viewer = ImageViewer()
        self.toolbar = ViewerToolbar()

        # Link toolbar
        self.toolbar.zoom_in.connect(self.viewer.zoom_in)
        self.toolbar.zoom_out.connect(self.viewer.zoom_out)
        self.toolbar.fit_view.connect(self.viewer.reset_view)
        self.toolbar.rotate_left.connect(lambda: self.viewer.rotate(-90))
        self.toolbar.rotate_right.connect(lambda: self.viewer.rotate(90))
        self.toolbar.crop_mode.connect(lambda checked: self.viewer.set_cropping_mode(checked))

        layout.addWidget(self.viewer)
        layout.addWidget(self.toolbar)

    def load_image(self, path):
        self.viewer.request_image_load(path)

    def get_layout_for_image(self, path):
        # Placeholder for layout logic
        return None

    def save_layout_data(self, path, layout):
        pass

    def remove_layout_data(self, path):
        pass
