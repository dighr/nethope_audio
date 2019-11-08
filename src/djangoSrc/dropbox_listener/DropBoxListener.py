
import dropbox
import pathlib
from helpers import constants
from dropbox.files import FolderMetadata, FileMetadata
from audio_transcription.models import AudioFiles
import os
import errno


def file_exists(filename):
    return AudioFiles.objects.filter(filename=filename).exists()
    # return False


class DropBoxListener:
    files = []
    output_files = []
    dbx = None

    def __init__(self):
        self.dbx = dropbox.Dropbox(constants.DropBox_API_KEY)
        self.get_valid_files()

    def get_valid_files(self):
        """
        Returns all the valid files from dropbox, return only if they do not exist in the db
        :return:
        """
        folders = ['']
        while len(folders) > 0:
            current_path = folders.pop(-1)
            for entry in self.dbx.files_list_folder(path=current_path, recursive=False).entries:
                if isinstance(entry, FolderMetadata):
                    folders.append(current_path + '/' + entry.name)
                elif isinstance(entry, FileMetadata):
                    if pathlib.Path(entry.name).suffix in constants.SUPPORTED_AUDIO_ENCODING:
                        if not file_exists(current_path + '/' + entry.name):
                            self.files.append(current_path + '/' + entry.name)

    def download_all_file(self):
        self.output_files = []
        for file in self.files:
            try:
                filename = self.download_file(file)
                print(filename)
                self.output_files.append(filename)
            except Exception as e:
                print(e)
                print("Error downloading file: " + file)

    def get_output_files(self):
        return self.output_files

    def download_file(self, path):
        # Separate the path from the file name
        filename = path.split("/")[-1]
        filepath = constants.DOWNLOAD_PATH
        if not os.path.exists(os.path.dirname(filepath + filename)):
            try:
                os.makedirs(os.path.dirname(filepath + filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filepath + filename, "wb+") as f:
            meta_data, res = self.dbx.files_download(path=path)
            f.write(res.content)

        return filepath + filename


