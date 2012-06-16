import unittest

import test_rotatable_file, test_text_file, test_log_sender,test_config, test_config_client

suite = unittest.TestLoader().loadTestsFromTestCase(test_config.test_config)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_config_client.test_config_client)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_log_sender.test_log_sender)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_rotatable_file.test_rotatable_file)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_text_file.test_text_file)
unittest.TextTestRunner(verbosity=2).run(suite)
