from greedy import tasks
from collections import Counter
from greedy import User



if __name__ == '__main__':
    summary_1st_place = Counter([tasks(['老王','老魏','佩佩猪'],0.3)[0] for i in range(1000)])
    summary_2nd_place = Counter([tasks(['老王','老魏','佩佩猪'],0.3)[1] for i in range(1000)])
    last_task = tasks(['老王','老魏','佩佩猪'],0.3)

    print('Using this algorithm, 1st place distribution', summary_1st_place)
    print('Using this algorithm, 2nd place distribution', summary_2nd_place)
    print('3 person, each raise a mantis, we arrange as follows', last_task)
