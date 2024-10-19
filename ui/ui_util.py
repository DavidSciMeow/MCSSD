from PyQt5.QtWidgets import QFileDialog
import global_vars

def file_save(save_function, initial_filename):
    options = QFileDialog.Options()
    #options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(None, global_vars.lang.get('save_file_str', 'Save File'), initial_filename, "JAR files (*.jar)", options=options)
    if file_name:
        save_function(file_name)