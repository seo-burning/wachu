if __name__ == '__main__':
    with open('./crawling/account_list.txt') as f:
        old_lines = f.readlines()
    with open('./crawling/del_list.txt') as f:
        del_lines = f.readlines()
    del_num = 0
    with open('./crawling/account_list.txt', 'wt') as f:
        for item in old_lines:
            if item not in del_lines:
                f.writelines(item)
            else:
                print("{} is deleted from list".format(item))
                del_num = del_num + 1
        print("{} accounts are deleted from list".format(del_num))
