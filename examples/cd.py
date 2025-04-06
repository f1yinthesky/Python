from typing import Optional

def cd(current_dir: str, relative_dir:str, short_link: dict[str,str] = {}) -> Optional[str]:
    current_dir_list = [dir for dir in current_dir.split('/') if dir != '']
    relative_dir_list = [dir for dir in relative_dir.split('/') if dir != '']

    all_dir_list = current_dir_list
    if relative_dir.startswith('/'):
        all_dir_list = relative_dir_list
    else:
        all_dir_list.extend(relative_dir_list)

    output_list = []
    for dir in all_dir_list:
        if dir == ".":
            continue
        if dir == "..":
            if len(output_list) == 0:
                return None
            output_list.pop()
        else:
            output_list.append(dir)

    for i in range(len(output_list) - 1, -1, -1):
        current_list = output_list[0:i+1]
        current_dir = '/' + '/'.join(current_list)
        if current_dir in short_link:
            output_list = [dir for dir in short_link[current_dir].split('/') if dir != ''] + output_list[i+1:]
            break
    return '/' + '/'.join(output_list)

def test_cd():
    test_data = [
        ('/', 'foo/bar/', '/foo/bar'),
        ('/', './foo/../bar/', '/bar'),
        ('/foo/bar', './foo/../bar/', '/foo/bar/bar'),
        ('/foo/./bar', './foo/../bar/', '/foo/bar/bar'),
        ('/foo/bar', './foo/../../bar/', '/foo/bar'),
        ('/', '../', None),
        ('/foo/bar', '/foo/../bar/', '/bar'),
        ('/', 'foo/bar/', {'/foo/bar':'/f/b', '/foo': '/f'},'/f/b'),
        ('/', 'foo/bar1/', {'/foo/bar':'/f/b', '/foo': '/f'},'/f/bar1'),
    ]

    for one_test in test_data:
        if len(one_test) == 3:
            assert cd(one_test[0], one_test[1]) == one_test[2], f"failed on one_test with cd({one_test[0]}, {one_test[1]}) is {cd(one_test[0], one_test[1])} vs expected {one_test[2]})"
        else:
            cd_result = cd(one_test[0], one_test[1], one_test[2])
            assert cd_result == one_test[3], f"failed on one_test with cd({one_test[0]}, {one_test[1]}, {one_test[2]}) is {cd_result} vs expected {one_test[3]})"

test_cd()