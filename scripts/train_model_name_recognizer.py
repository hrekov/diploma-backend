import argparse
import os

def validate_folder_path(folder_path):
    """
    Validate whether or not the provided folder path exists.
    """
    if not os.path.exists(folder_path):
        raise argparse.ArgumentTypeError(f"{folder_path} does not exist.")

    return folder_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate dataset folder path')
    parser.add_argument('dataset_path', type=validate_folder_path,
                        help='Path to the dataset folder')

    args = parser.parse_args()
