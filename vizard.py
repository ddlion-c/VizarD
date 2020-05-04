import os
import sys
import yaml
import logging
import logging.config
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from ui.main import MainWindow


logger = logging.getLogger(__name__)


class VizarDApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)

        # Initialize instances

        self.mainWindow = MainWindow()

        self.mainWindow.resize(1024, 768)
        g = self.mainWindow.frameGeometry()

        c = QDesktopWidget().availableGeometry().center()
        g.moveCenter(c)
        self.mainWindow.move(g.topLeft())


def setup_logging():
    config = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logging.conf")
    with open(config, 'rt') as f:
        try:
            log_conf = yaml.safe_load(f.read())
            logging.config.dictConfig(log_conf)
        except Exception as e:
            print(e)
            print("Error in logging configuration: {}".format(config))
            raise


def main():
    setup_logging()
    # TODO: Commented license line for debugging purpose
    # check_license()

    app = VizarDApplication(sys.argv)
    app.mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
