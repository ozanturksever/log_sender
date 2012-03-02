import unittest


from lib.test_log_sender import test_log_sender
suite = unittest.TestLoader().loadTestsFromTestCase(test_log_sender)
unittest.TextTestRunner(verbosity=2).run(suite)

from lib.tailer.test_rotatable_file import test_rotatable_file
suite = unittest.TestLoader().loadTestsFromTestCase(test_rotatable_file)
unittest.TextTestRunner(verbosity=2).run(suite)
