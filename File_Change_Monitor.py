import hashlib
import time


def CalculateFileHash(filePath):
    with open(filePath, "rb") as f:
        fileHash = hashlib.sha256(f.read()).hexdigest()
    return fileHash


# we want to run this on a separate thread and read the return value every few seconds.
# from this we can add a little ("You have unsaved changes") message at the top @TODO
def DetectFileChange(filePath, lastHash):
    curHash = CalculateFileHash(filePath)
    if lastHash != curHash:
        print("File has changed!")
        return "Unsaved"
        # update classes stored hash
