from PyQt5.QtWidgets import QMessageBox


def show_message_box(data):
    if isinstance(data, Exception):
        content = _get_error_message(data)
    else:
        pass
    _show_message_box(content)


def _get_error_message(e):
    content = dict()
    content['icon'] = QMessageBox.Critical
    content['title'] = "Error"
    content['text'] = "Error"
    content['desc'] = e.args[0]
    return content


def _show_message_box(d):
    if not d:
        return

    msg = QMessageBox()
    msg.setIcon(d['icon'])
    msg.setText(d['text'])
    msg.setInformativeText(d['desc'])
    msg.setWindowTitle(d['title'])
    msg.exec_()
