import unittest
import sys
import run  # this imports your run.py as a module

class TestRunScript(unittest.TestCase):
    
    def test_run_with_feature_1(self):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '1']
            
            # Run your script's main code
            run.main()  # assuming run.py has a main() you can call
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv

if __name__ == "__main__":
    unittest.main()
