from unittest import TestCase, skip
from src.dynamic.mutator import *
import types

class MutatorTest(TestCase):
    def setUp(self):
        self.mutator = Mutator()

    def test_add_new_method(self):
        mycode = '''def duration(env):
    while True:
        print('we are at moment %d' % env.now)
        duration = 10
        yield env.timeout(duration)
    '''
        self.mutator.compile_code(mycode)
        context = self.mutator.get_context()

        self.assertIn('duration', context)

        selector = context['duration']
        self.assertTrue(isinstance(selector, types.FunctionType))


    def test_code_signature(self):
        mycode = '''def duration(env):
    while True:
        print('we are at moment %d' % env.now)
        duration = 10
        yield env.timeout(duration)
    '''
        signature = self.mutator.get_signature_string(mycode)
        self.assertEquals('duration', signature)

    def test_add_new_method_and_reset(self):
        mycode = '''def stub(env):
                return 34
               '''
        self.mutator.compile_code(mycode)
        context = self.mutator.get_context()
        self.assertIn('stub', context)
        context = self.mutator.get_context(True)
        self.assertNotIn('stub', context)

    def test_define_method(self):
        mycode = ''' return 34'''
        self.mutator.define_new_method('stub', [], mycode)
        context = self.mutator.get_context()

        self.assertIn('stub', context)

        selector = context['stub']
        self.assertTrue(isinstance(selector, types.FunctionType))
        self.assertEquals(34, selector())

    def test_with_arg_list(self):
        mycode = ''' return param '''
        self.mutator.define_new_method('stub', ['param'], mycode)
        context = self.mutator.get_context()

        self.assertIn('stub', context)
        selector = context['stub']
        param = 24
        self.assertEquals(param, selector(param))

    def test_with_variable_arg_list(self):
        mycode = ''' return args '''
        self.mutator.define_new_method('stub', [], mycode, variable_args=True)
        context = self.mutator.get_context()
        self.assertIn('stub', context)
        selector = context.get_selector('stub')
        param = (34, 21)
        self.assertEquals(param, selector(*param))
        another_param = ('324', 'test', 3)
        self.assertEquals(another_param, selector(*another_param))

    def test_create_class(self):
        class_name = 'TestClass'
        test_class = self.mutator.create_class(class_name)
        self.assertEquals(class_name, test_class.__name__)
        self.assertEquals((object,), test_class.__bases__)

    def test_create_class_with_methods(self):
        mycode = ''' return 134 '''
        self.mutator.define_new_method('test_method', [], mycode, instance_bound=True)

        # Finally create the class
        class_name = 'TestClass'
        test_class = self.mutator.create_class(class_name, bound_context=True)
        self.assertEquals(class_name, test_class.__name__)
        self.assertEquals((object,), test_class.__bases__)
        self.assertEquals(134, test_class().test_method())

    def test_set_method_to_instance(self):
        class A(object):
            pass

        instance = A()
        mycode = ''' return 432 '''
        new_selector = self.mutator.define_instance_method(instance, 'test_method', [], mycode)

        self.assertTrue(isinstance(new_selector, types.FunctionType))
        self.assertTrue(isinstance(instance.test_method, types.FunctionType))
        self.assertEqual(instance.test_method, new_selector)
        self.assertEqual(432, instance.test_method())
