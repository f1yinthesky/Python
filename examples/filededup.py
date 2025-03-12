from typing import List, DefaultDict, Optional
import os
from collections import namedtuple, defaultdict
import hashlib
import filecmp 
FileInfo = namedtuple("FileInfo", "file_size, small_hash")

def getFileHash(path:str, max_size:Optional[int] = None) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        if max_size is None:
            hasher.update(f.read())
        else:
            hasher.update(f.read(max_size))
    return hasher.hexdigest()

def genFileInfo(entry: os.DirEntry) -> FileInfo:
    file_path = entry.path
    file_size = entry.stat().st_size
    return (file_size, getFileHash(file_path, 10))

file_path_hash = {}
def SlowCompareFile(left_file:str, right_file:str) -> bool:
    if left_file not in file_path_hash:
        file_path_hash[left_file] = getFileHash(left_file)
    if right_file not in file_path_hash:
        file_path_hash[right_file] = getFileHash(right_file)

    if file_path_hash[left_file] != file_path_hash[right_file]:
        return False
    
    return filecmp.cmp(left_file, right_file, shallow=False)

def mergeDefaultDict(src: DefaultDict[FileInfo, List[str]], des: DefaultDict[FileInfo, List[str]]) -> None:
    for key, value in src.items():
        des[key].extend(value)

def getAllFiles(one_dir:str) -> DefaultDict[FileInfo, List[str]]:
    all_files = defaultdict(list)
    with os.scandir(one_dir) as entry_iterator:
        for entry in entry_iterator:
            if entry.is_file(follow_symlinks=False):
                file_info = genFileInfo(entry)
                all_files[file_info].append(entry.path)
            if entry.is_dir(follow_symlinks=False):
                mergeDefaultDict(getAllFiles(entry.path), all_files)
            # Symlink
    return all_files

def duplicateFiles(one_dir: str) -> List[List[str]]:
    all_files = getAllFiles(one_dir)
    answer = []
    for _, file_list in all_files.items():
        if len(file_list) == 1:
            continue
        used_file = set()
        for i in range(len(file_list)):
            left_file = file_list[i]
            left_duplicate = [left_file]
            if left_file in used_file:
                continue
            used_file.add(left_file)
            for j in range(i + 1, len(file_list)):
                right_file = file_list[j]
                if right_file in used_file:
                    continue
                if SlowCompareFile(left_file, right_file):
                    left_duplicate.append(right_file)
                    used_file.add(right_file)
                else:
                    print(f"hash collision between {left_file} and {right_file}")
            if len(left_duplicate) > 1:
                answer.append(left_duplicate)
    return answer

def main() -> None:
    one_dir = r"C:\Users\huang\Downloads\tmp"
    print(duplicateFiles(one_dir))

if __name__ == '__main__':
    main()