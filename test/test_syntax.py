from unittest import TestCase, skip
from src.parser.parser_conbinator import parse_all
from src.parser.ast import *
from src.all_exceptions import DSLLexerException, DSLParserException

class TestSyntax(TestCase):
    def setUp(self):
        self.parser = parse_all

    def test_empty_expression(self):
        input = """
                """
        ast = self.parser(input)
        self.assertEqual(0, len(ast))

    def test_simple_definition_container(self):
        input = """
        environment {

        }
        environment.run(until=20)
        """
        ast = self.parser(input)
        self.assertEqual(2, len(ast))
        environment = ast[0]
        self.assertIsInstance(environment, Environment)
        self.assertEqual(ast[1].function_name, 'run')
        self.assertEqual(ast[1].arguments[0].name, 'until')
        self.assertEqual(ast[1].arguments[0].value, 20)

    def test_simple_assignment_container(self):
        input = """
        environment {
            parking_duration = 5
        }
        environment.run(until=20)
        """
        ast = self.parser(input)
        self.assertEqual(2, len(ast))
        enviro = ast[0]
        self.assertEqual(1, len(enviro.inner_block))
        self.assertIsInstance(enviro.inner_block[0], Assignment)


    def test_simple_context_definition_container(self):
        input = """
        environment {
           def context a {
           }
        }
        environment.run(until=20)
        """
        ast = self.parser(input)
        self.assertEqual(2, len(ast))
        enviro = ast[0]
        context = enviro.inner_block[0]
        self.assertEqual(1, len(enviro.inner_block))
        self.assertEqual('a', context.context_name)
        self.assertEqual(0, len(context.inner_block))

    def test_definition_of_container(self):
        pass
        input = """
        environment {
        def context car {
                print("Start parking at %d",env.now)
                parking_duration = 5
                wait_timeout(parking_duration)

                print("Start driving at %d",env.now)
                trip_duration = 2
                wait_timeout(trip_duration)
            }

        }
        environment.process(car)
        environment.run(until=20)
        """

        ast = self.parser(input)
        self.assertEqual(3, len(ast))
        enviro = ast[0]
        context = enviro.inner_block[0]
        self.assertEqual(6, len(context.inner_block))
        self.assertIsInstance(context.inner_block[0], FunctionCall)

    def test_failure_in_syntax(self):
        input = """
        environment {
            def context bleh {
                mark = 1;
            }
        }
        """
        self.assertRaises(DSLLexerException, self.parser, input)


    def test_failure_in_parsing(self):
        input = """
        environmennt {
        }
        environment.run(until=20)
        """
        self.assertRaises(DSLParserException, self.parser, input)