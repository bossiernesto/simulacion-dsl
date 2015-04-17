from unittest import TestCase, skip

class TestSyntax(TestCase):

    def setUp(self):
        pass

    @skip
    def test_definition_of_container(self):
        input = """
        enviroment {
            def context car {
                print('Start parking at %d',env.now)
                parking_duration = 5
                wait_timeout(parking_duration)

                print('Start driving at %d',env.now)
                trip_duration = 2
                wait_timeout(trip_duration)
            }

        }
        enviroment.process(car);
        enviroment.run(until=20)
        """

