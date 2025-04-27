import unittest
import sys
from unittest.mock import patch


import run  

class TestRunScript(unittest.TestCase):
    
    @patch('builtins.input', return_value='1')
    def test_run_with_feature_1(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '1']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            
    @patch('builtins.input', return_value='2')
    def test_run_with_feature_1_full(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '1']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            
    @patch('builtins.input', return_value='1')
    def test_run_with_feature_2(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '2']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            
    @patch('builtins.input', return_value='2')
    def test_run_with_feature_2_full(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '2']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            
    @patch('builtins.input', return_value='1')
    def test_run_with_feature_3(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '3']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            
    @patch('builtins.input', return_value='2')
    def test_run_with_feature_3_full(self, mock_input):
        # Save the original sys.argv
        original_argv = sys.argv
        
        try:
            # Fake the command line arguments
            sys.argv = ['run.py', '--feature', '3']
            
            # Run your script's main code
            run.main()  
        finally:
            # Restore the original argv so it doesn't mess up other tests
            sys.argv = original_argv
            

if __name__ == "__main__":
    unittest.main()
