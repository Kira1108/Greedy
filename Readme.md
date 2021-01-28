```python
from greedy import tasks
from collections import Counter
from greedy import User

if __name__ == '__main__':
    # 随便看一下，给这三个人怎么排任务的先后
    summary_1st_place = Counter([tasks(['老王','老魏','佩佩猪'],0.3)[0] for i in range(1000)])
    summary_2nd_place = Counter([tasks(['老王','老魏','佩佩猪'],0.3)[1] for i in range(1000)])

    # 0.3的概率随机探索，给这个人重新做人的机会
    # 0.7的概率探索最好的
    last_task = tasks(['老王','老魏','佩佩猪'],0.3)

    print('Using this algorithm, 1st place distribution', summary_1st_place)
    print('Using this algorithm, 1st place distribution', summary_2nd_place)
    print('3 person, each raise a mantis, we arrange as follows', last_task)

    # 每次干完这个事儿以后，更新数据库文件
```

这样，坏人在数据库里面自动更新自己坏的likelihood，我们只在小部分时间给坏人自己更新自己的机会。
把大多数的时间留给优秀的，需求，和需求提出者。
