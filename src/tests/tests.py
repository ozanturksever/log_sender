import unittest

import test_rotatable_file, test_text_file, test_watch_file_manager, test_config, test_config_client, test_syslog_processor, test_processor_manager

suite = unittest.TestLoader().loadTestsFromTestCase(test_config.test_config)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_config_client.test_config_client)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_watch_file_manager.test_watch_file_manager)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_rotatable_file.test_rotatable_file)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_text_file.test_text_file)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_syslog_processor.test_syslog_processor)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(test_processor_manager.test_processor_manager)
unittest.TextTestRunner(verbosity=2).run(suite)
