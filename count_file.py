"""
多进程文件计数
"""
import os
import atexit
import multiprocessing
import json
import time


class Count(object):
    def __init__(self, n):
        self.n = n
        self.num = 0
        # atexit.register(self.dump_file)

    def _count(self, path, count_type='.mp3'):
        path = os.path.abspath(path)
        path_list = os.listdir(path)
        num = 0
        # add_path = False
        for p in path_list:
            new_p = path + '/' + p
            if count_type in p:
                # add_path = True
                self.file_list.append(p)
                self.num += 1
                num += 1
                # print(' ' * 90, end='\r')
                # print(path, p, num, self.num, end='\r')
            elif os.path.isdir(new_p):
                self._count(new_p)

            self.sche_dict[self.n] = self.num

        # if add_path:
        #     self.path_map[path] = num
        #     # print(self.path_map)

    def count(self, pl, sche_dict, file_list):
        self.sche_dict = sche_dict
        self.file_list = file_list
        self.sche_dict[self.n] = 0
        for i in pl:
            self._count(i)


def dump_file(shce_dict, file_list):
    s = '█'
    print('dump to file....')
    with open('count.count', 'w') as f:
        allnum = sum(shce_dict.values())
        f.write('num: %s\n\n' % allnum)
        print('transf dict...')
        file_list = list(file_list)
        length = len(file_list)
        c = 0
        print('write to file...')
        for i in file_list:
            c += 1
            if c % 1000 == 0:
                print('%s%%' % round(c / length * 100, 1), '\x1b[?25l|' + format(s * int(c / length * 41), '<40') + '|', '%s/%s' % (c, length), ' ' * 20, end='\r')
                time.sleep(0.2)
            f.write('%s  \n' % i)
        else:
            print('100%', '\x1b[?25l|' + format(s * int(c / length * 41), '<40') + '|', '%s/%s' % (c, length), ' ' * 20)
        print('done')


def e(*args):
    print(args)


def s(*args):
    pass


def mmain():
    pool = multiprocessing.Pool(8)
    m = multiprocessing.Manager()
    shce_dict = m.dict()
    file_list = m.list()
    process_list = []
    for i in range(8):
        j = i + 1
        k = i * 128
        j *= 128
        path_list = [str(x) for x in range(k, j)]
        c = Count(str(i))
        a = pool.apply_async(c.count, args=(path_list, shce_dict, file_list), error_callback=e, callback=s)
        process_list.append(a)

    pool.close()
    while 1:
        l = [x.ready() for x in process_list]
        if all(l):
            break
        else:
            time.sleep(1)
            print(l)
            print(shce_dict)
            print('all num: %s' % sum(shce_dict.values()))
    dump_file(shce_dict, file_list)


# def main(path):
#     c = Count('')
#     c.count(path)


if __name__ == '__main__':
    # main(['/repertory/capture/downloads/tencent/mp3'])
    mmain()
