import json

def load_data(path):
    """Input the data from .json.

    It handles input path as file or dir with files. It opens them and save all in a list of frames

    :rtype: list
    :param path: path of the directory or file to calculate the interactions
    :return: return the set of people in the current frame where to calculate interactions
    """
    # if it is a single file, just extract it
    if path.is_file():
        with open(path) as file:
            data = json.load(file)
        return data
    # # if it is a directory, look for all files and open all and put in a list to return
    # elif path.is_dir():
    #     # folder should contain only files
    #     data = []
    #     # elements = sorted(path.glob('*.json'))
    #
    #     my_array = []
    #     for filename in (path.glob('*.json')):
    #         my_array.append(str(filename))
    #
    #     my_array.sort(key=natural_keys)
    #     for i in range(len(my_array)):
    #         with open(my_array[i]) as file:
    #             data.append(json.load(file))
    #     return data

    # if the path is not a directory nor a file, btw should never happen
    else:
        raise FileNotFoundError('path is not a directory nor a file. Exeption from people_interaction', path)

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
           alist.sort(key=natural_keys) sorts in human order
           http://nedbatchelder.com/blog/200712/human_sorting.html
           (See Toothy's implementation in the comments)
           """
    return [atoi(c) for c in re.split(r'(\d+)', text)]