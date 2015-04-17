import simpy


def duration(env):
    while True:
        print('we are at moment %d' % env.now)
        duration = 10
        yield env.timeout(duration)


env = simpy.Environment()
env.process(duration(env))
env.run(until=11)


