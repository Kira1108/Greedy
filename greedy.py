
import random
import matplotlib.pyplot as plt
import pandas as pd
DATABASE = '忘不了你的坏.csv'

# Arm 1, Arm 2 rather than option 1, option 2...
# Reward, simply a measurement of success.
# General problem: having N arms
# When pulled, any give arm will output a reward. But these rewards are not reliable.
# Wen only receieve small information on each arm

# Explore: travel through (an unfamiliar area) in order to learn about it.
# Exploit: make full use of and derive benefit from (a resource).

# epsilon: chanes to Explore
# counts: how many times each arm is `played`,
# values: Average reward of each arm


class BernoulliArm():

    def __init__(self, p):
        '''p - probability of getting 1, success
            Use draw function to return rewards
        '''
        self.p = p

    def draw(self):
        return 0.0 if random.random() > self.p else 1.0


class EpsilonGreedy():
    '''
        To initialize a epsilon greedy algorithm, You need to
        1. setup a eposilon values
        2. setup a counts and values array, both can be empty array
        3. initialize the algorithm, choose number of arms,
            set all values of counts and values to zero
        4. select arm:
            darw a random number,
                if greater than eposilon - return max index of values
                else choose a random arm

        5. update belief:
             increase counts by 1
             update value of the chosen arm
    '''
    def __init__(self, epsilon, counts, values):
        self.epsilon = epsilon
        self.counts = counts   # an array used to keep counts
        self.values = values   # an array used to keep scores

    def initialize(self,n_arms):
        self.counts = [0 for col in range(n_arms)]
        self.values = [0.0 for col in range(n_arms)]

    @classmethod
    def new(cls, epsilon, n_arms):
        counts = [0 for col in range(n_arms)]
        values = [0.0 for col in range(n_arms)]
        return cls(epsilon, counts, values)


    @staticmethod
    def ind_max(x):
        '''find index of the max value in array x'''
        m = max(x)
        return x.index(m)


    def select_arm(self):
        """Tell the numeric name of the arm we should pull"""
        if random.random() > self.epsilon:
            # select best arm
            return EpsilonGreedy.ind_max(self.values)
        else:
            # select arm complete at random
            return random.randrange(len(self.values))

    def update(self, chosen_arm, reward):
        """Update algorithm belief about the quality of the am we just choose.
            By providing the reward information
        """
        # increase count of chosen arm by 1
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n = self.counts[chosen_arm]

        # old_value = sum rewards /  n - 1
        # sum_reward = old_value * (n-1)
        # new_sum_reward = old_value * (n - 1) + new_reward
        # new_value = (old_value * (n - 1) + new_reward )/ n
        # new_value = (n-1) * old_value / n +  new_reward / n
        value = self.values[chosen_arm]
        new_value = ((n-1)/float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value


def test_arm_selection():
    for i, epsilon in enumerate([0.1 ,0.3, 0.5, 0.7, 0.9, 0.95]):
        algo = EpsilonGreedy(epsilon,[],[])
        algo.initialize(4)
        arms_selected = [algo.select_arm() for _ in range(100)]
        plt.subplot(2,3, i + 1)
        plt.hist(arms_selected)
        plt.title("Epsiolon = {}".format(epsilon))
        plt.grid(linestyle = '--', color = 'gray')
    plt.tight_layout()
    plt.savefig('imgs/arms_epsilon.png', dpi = 300)
    plt.show()


class User():

    def __init__(self, epsilon, user_belief, user_count):
        self.user_count = user_count
        self.user_belief = user_belief
        self._user2id()
        self.algo = EpsilonGreedy(epsilon, list(self.counts.values()), list(self.belief.values()))

    def _user2id(self):
        self.user2id = {user:i for i, user in enumerate(self.user_belief.keys())}
        self.id2user = {v:k for k,v in self.user2id.items()}
        self.belief = {self.user2id[user] : belief
                        for user, belief in self.user_belief.items()}
        self.counts = {self.user2id[user] : cnt
                        for user, cnt in self.user_count.items()}


    @classmethod
    def from_csv(cls, path, epsilon, user_list = None):
        user_df = pd.read_csv(path,encoding = 'GBK')
        if user_list:
            user_df = user_df[user_df.user.isin(user_list)]
        counts = user_df.groupby('user')['value'].count().to_dict()
        beliefs = user_df.groupby('user')['value'].mean().to_dict()
        return cls(epsilon, beliefs, counts)


def tasks(user_list, epsilon = 0.7):
    sequence = []

    while len(user_list) > 1:
        user = User.from_csv(DATABASE,epsilon, user_list)
        choose = user.id2user[user.algo.select_arm()]
        sequence.append(choose)
        user_list.remove(choose)

    sequence.append(user_list[0])
    return sequence
