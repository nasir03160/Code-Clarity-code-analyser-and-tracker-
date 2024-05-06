from django.test import TestCase

# Create your tests here.
# Example code snippet with Pylint and AST errors
def test_function(x):
    for i in range(10):
        print(i)
    return x

test_function(5  # Missing closing parenthesis