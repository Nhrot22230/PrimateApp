import os


class FileManager:
    def __init__(self):
        pass

    def verify_directory(self, directory):
        """
        Check if the specified directory exists.

        Parameters:
            directory (str): The path to the directory.

        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return os.path.exists(directory)

    def get_files_in_directory(self, directory):
        """
        Get the list of files in the specified directory.

        Parameters:
            directory (str): The path to the directory.

        Returns:
            list: A list of file names in the directory.
        """
        if self.verify_directory(directory):
            files = os.listdir(directory)
            files.sort()
            return files
        else:
            return []

    def create_directory(self, directory):
        """
        Create the specified directory if it doesn't exist.

        Parameters:
            directory (str): The path to the directory to create.
        """
        if not self.verify_directory(directory):
            os.makedirs(directory)

    def filter_files_by_extension(self, files, extension):
        """
        Filter a list of files based on the specified file extension.

        Parameters:
            files (list): A list of file names.
            extension (str): The file extension to filter by (e.g., '.txt', '.wav').

        Returns:
            list: A list of file names with the specified extension.
        """
        return [file for file in files if file.endswith(extension)]
    
    def check_directories(self, needed_directories):
        """
        Check if the specified directories exist.

        Parameters:
            needed_directories (list): A list of directory names.

        Returns:
            bool: True if all directories exist, False otherwise.
        """
        for directory in needed_directories:
            if not self.verify_directory(directory):
                return False
        return True
    
    def restore_directories(self, needed_directories):
        """
        Restore the specified directories if they don't exist.

        Parameters:
            needed_directories (list): A list of directory names to restore.
        """
        for directory in needed_directories:
            if not self.verify_directory(directory):
                self.create_directory(directory)
