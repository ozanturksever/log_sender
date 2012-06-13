import unittest


from lib.test_log_sender import test_log_sender
suite = unittest.TestLoader().loadTestsFromTestCase(test_log_sender)
unittest.TextTestRunner(verbosity=2).run(suite)
#
from lib.tailers.test_rotatable_file import test_rotatable_file
suite = unittest.TestLoader().loadTestsFromTestCase(test_rotatable_file)
unittest.TextTestRunner(verbosity=2).run(suite)
#
from lib.importers.test_text_file import test_text_file
suite = unittest.TestLoader().loadTestsFromTestCase(test_text_file)
unittest.TextTestRunner(verbosity=2).run(suite)
