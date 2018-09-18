import numpy as np
import gym
from Distributional_RL import Distributional_RL
import tensorflow as tf
from collections import deque

sess = tf.Session()
env = gym.make('CartPole-v0')
learning_rate = 0.0001
model = 'QRDQN'
qrdqn = Distributional_RL(sess, model, learning_rate)

sess.run(tf.global_variables_initializer())
#sess.run(qrdqn.assign_ops)
memory_size = 10000
memory = deque(maxlen=memory_size)

for episode in range(10000):
    e = 1. / ((episode / 10) + 1)
    done = False
    state = env.reset()
    global_step = 0
    l = 0
    while not done:
        global_step += 1
        if np.random.rand() < e:
            action = env.action_space.sample()
        else:
            action = qrdqn.choose_action(state)

        next_state, reward, done, _ = env.step(action)

        if done:
            reward = -1
        else:
            reward = 0

        if len(memory) > 1000:
            _, loss = qrdqn.train(memory)
            l += loss
            if global_step % 5 == 0:
                sess.run(qrdqn.assign_ops)
        action_one_hot = np.zeros(2)
        action_one_hot[action] = 1
        memory.append([state, next_state, action_one_hot, reward, done])
        state = next_state
        if done:
            print(episode, global_step, l)