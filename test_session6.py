import pytest
import time
import os
import inspect
import glob
import re
import session6
from session6 import add, mul, div, call_counts, docstring_checker, fibonacci_closure

# TEST functions for README CHECK
def test_session6_readme_exists():
    """Test that the README file exists"""
    assert os.path.isfile("README.md"), "README.md file missing!"


def test_session6_readme_500_words():
    """Test that the README file has at least 500 words"""
    readme = open('README.md', 'r', encoding='utf-8').read()
    readme_words = readme.split()
    assert len(readme_words) >= 500, "README.md does not contain at least 500 words"


def test_session6_readme_proper_description():
    """Test that the README file has proper description"""
    README_CONTENT_CHECK_FOR = [
        'docstring_checker',
        'fibonacci_closure',
        'create_counter',
        'add',
        'mul',
        'div',
        'closure',
        'recursive',
    ]
    readme = open('README.md', 'r', encoding='utf-8').read().lower()
    assert all(keyword in readme for keyword in README_CONTENT_CHECK_FOR), "README.md does not properly describe all the functions"


def test_session6_readme_file_for_more_than_10_hashes():
    """Test that the README file contains more than 10 '#' characters"""
    readme = open('README.md', 'r', encoding='utf-8').read()
    assert readme.count('#') > 10, "README.md does not contain more than 10 '#' characters"

def check_indentation():
    lines = inspect.getsource(session6)
    spaces = re.findall(r'\n +.', lines)
    for line in spaces:
        leading_spaces = len(re.sub(r'[^ ]', '', line))
        if leading_spaces % 4 != 0:
            print(f"Line with incorrect indentation: {line.strip()} (Leading spaces: {leading_spaces})")

def test_session6_function_name_had_cap_letter():
    """Test that the function names do not have capital letters"""
    functions = inspect.getmembers(session6, inspect.isfunction)
    for function in functions:
        assert not any(c.isupper() for c in function[0]), f"Function name {function[0]} contains capital letters"

# Test functions FOR COUNTER
def test_add_function_call_count():
    """Test add function call count"""
    call_counts['add'] = 0  # Reset count
    add(1, 2)
    add(3, 4)
    assert call_counts['add'] == 2, "Add function call count should be 2"


def test_mul_function_call_count():
    """Test mul function call count"""
    call_counts['mul'] = 0  # Reset count
    mul(2, 3)
    assert call_counts['mul'] == 1, "Mul function call count should be 1"


def test_div_function_call_count():
    """Test div function call count"""
    call_counts['div'] = 0  # Reset count
    div(4, 2)
    div(10, 5)
    div(9, 0)
    assert call_counts['div'] == 3, "Div function call count should be 3"


def test_function_return_values():
    """Test return values of functions"""
    assert add(1, 1) == 2, "Add function should return correct sum"
    assert mul(2, 3) == 6, "Mul function should return correct product"
    assert div(10, 2) == 5, "Div function should return correct quotient"
    assert div(10, 0) == float('inf'), "Div function should return infinity for division by zero"


def test_call_counts_independence():
    """Test that function call counts are independent"""
    call_counts['add'] = 0
    call_counts['mul'] = 0
    call_counts['div'] = 0
    add(1, 1)
    mul(2, 2)
    div(10, 2)
    assert call_counts['add'] == 1, "Add function call count should be independent"
    assert call_counts['mul'] == 1, "Mul function call count should be independent"
    assert call_counts['div'] == 1, "Div function call count should be independent"


def test_no_side_effects_on_call_counts():
    """Test that call counts are not affected by other function calls"""
    call_counts['add'] = 0
    call_counts['mul'] = 0
    call_counts['div'] = 0
    add(1, 1)
    add(2, 2)
    assert call_counts['add'] == 2, "Add function call count should not be affected by other function calls"
    assert call_counts['mul'] == 0, "Mul function call count should remain 0 if not called"
    assert call_counts['div'] == 0, "Div function call count should remain 0 if not called"

def test_add_with_zero():
    """Test add function with zero"""
    assert add(0, 5) == 5, "Add function with zero failed"
    assert add(5, 0) == 5, "Add function with zero failed"

def test_mul_with_zero():
    """Test mul function with zero"""
    assert mul(0, 5) == 0, "Mul function with zero failed"
    assert mul(5, 0) == 0, "Mul function with zero failed"

def test_div_by_zero():
    """Test div function by zero"""
    assert div(5, 0) == float('inf'), "Div function by zero failed"

def test_div_zero_by_any_number():
    """Test div function zero by any number"""
    assert div(0, 5) == 0, "Div function zero by any number failed"
    
# Test functions for DOC STRING
def test_docstring_checker_long_docstring():
    """Test docstring_checker with a function having a long docstring."""
    @docstring_checker()
    def function_with_long_docstring():
        """
        This is a test function that has a docstring
        longer than fifty characters. It should pass the check.
        """
        pass
    
    result = function_with_long_docstring()
    assert result == "The function 'function_with_long_docstring' has a docstring longer than 50 characters."


def test_docstring_checker_short_docstring():
    """Test docstring_checker with a function having a short docstring."""
    @docstring_checker()
    def function_with_short_docstring():
        """Short docstring."""
        pass
    
    result = function_with_short_docstring()
    assert result == "The function 'function_with_short_docstring' does not have a docstring longer than 50 characters."


def test_docstring_checker_no_docstring():
    """Test docstring_checker with a function having no docstring."""
    @docstring_checker()
    def function_with_no_docstring():
        pass
    
    result = function_with_no_docstring()
    assert result == "The function 'function_with_no_docstring' does not have a docstring longer than 50 characters."
       
# TEST FUNCTIONS FOR FIBONACCI SERIES
def test_fibonacci_efficiency():
    """Test the efficiency of the Fibonacci generator"""
    fib = fibonacci_closure()

    # Generate a large number of Fibonacci numbers
    start_time = time.time()
    fib_numbers = [fib() for _ in range(1000)]
    end_time = time.time()
    
    elapsed_time = end_time - start_time

    # Check if the time taken is reasonable (less than 1 second for 1000 numbers)
    assert elapsed_time < 1, "Fibonacci generator is too slow, possibly using inefficient recursive method"


def test_fibonacci_large_sequence():
    """Test the Fibonacci generator with a large sequence"""
    fib = fibonacci_closure()

    # Generate a large number of Fibonacci numbers
    fib_numbers = [fib() for _ in range(10000)]

    # Check the first few numbers for correctness
    expected_initial_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib_numbers[:10] == expected_initial_sequence, "The initial Fibonacci sequence is incorrect"

    # Check the last few numbers to ensure the sequence is continuous
    assert fib_numbers[-1] == fib_numbers[-2] + fib_numbers[-3], "The last Fibonacci number is incorrect"
    assert fib_numbers[-2] == fib_numbers[-3] + fib_numbers[-4], "The second last Fibonacci number is incorrect"
    assert fib_numbers[-3] == fib_numbers[-4] + fib_numbers[-5], "The third last Fibonacci number is incorrect"

    # Ensure the function performs efficiently
    assert all(fib_numbers[i] == fib_numbers[i - 1] + fib_numbers[i - 2] for i in range(2, 10000)), \
        "The Fibonacci sequence is incorrect at some point"

def test_fibonacci_initial_values():
    """Test the initial values of the Fibonacci sequence"""
    fib = fibonacci_closure()
    assert fib() == 0, "The first Fibonacci number should be 0"
    assert fib() == 1, "The second Fibonacci number should be 1"
