from unittest import TestCase, skip
from src.parser.parser import *


class TestSyntax(TestCase):
    def setUp(self):
        self.parser = Parser()


    def test_simple_definition_container(self):
        input = """
        enviroment {

        }
        enviroment.run(until=20)
        """
        ast = self.parser.parse(input)
        self.assertEqual(1, len(ast))
        enviroment = ast[0]
        self.assertIsInstance(enviroment.enviroment_name, EnviromentName)
        self.assertEqual('enviroment', enviroment.get_enviroment_name())


    def test_definition_of_container(self):
        pass
        # input = """
        # enviroment {
        # def context car {
        #         print('Start parking at %d',env.now)
        #         parking_duration = 5
        #         wait_timeout(parking_duration)
        #
        #         print('Start driving at %d',env.now)
        #         trip_duration = 2
        #         wait_timeout(trip_duration)
        #     }
        #
        # }
        # enviroment.process(car);
        # enviroment.run(until=20)
        # """
        # self.parser.parse(input)




