#Wrappers

This external dsl, when executes the AST, it'll generate string that will be generated to the respective python code,
using the simPy backend. For this there will be wrapper classes that will encapsulate the code generated from the information
that the AST holds. 

##Enviroment 

The enviroment class enables to emulate a enviroment instance, that will be attached events and run with a duration
a very simple example lies here (Note: You'll need to read about how the mutator works if you want to define the 
behaviour from string as the AST does when it's processed):

'''python

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

'''