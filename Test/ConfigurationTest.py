import unittest, configuration

class ConfigurationTest(unittest.TestCase):

    def setUp(self):
        self.configuration = configuration.Configuration(3,2, [1,1,1,1,1,1])

    def test_configuration(self):
        self.assertIsNotNone(self.configuration.get_spins())
        self.assertEqual(self.configuration.get_spins(), [[1,1,1],[1,1,1]])

if __name__ == '__main__':
    unittest.main()
