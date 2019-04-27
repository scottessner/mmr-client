import os
import re


def search_files(search_folder, include_regex=None, exclude_regex=None):
    results = list()

    for root, dirs, files in os.walk(search_folder):

        for file in files:

            folder = os.path.relpath(root, search_folder)

            relative_path = os.path.join(folder, file)

            if not include_regex or re.search(include_regex, relative_path):

                if not exclude_regex or not re.search(exclude_regex, relative_path):
                    results.append(relative_path)

    return results