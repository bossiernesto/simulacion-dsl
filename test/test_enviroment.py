from src.wrapper.enviroment import *
from src.dynamic.mutator import *

mutator = Mutator()

my_code = '''
    while True:
        print('we are at moment %d' % env.now)
        duration = 10
        yield env.timeout(duration)
    '''

mutator.define_new_method('duration', ['env'], my_code)

env = EnviromentWrapper()
env.attach_context(mutator.get_context())
env.attach_process_name('duration')
env.execute(until=11)
print env.get_enviroment()
