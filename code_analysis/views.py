from django.shortcuts import render,redirect
from .forms import CodeSnippetForm
from .models import Analysis,CodeSnippet,CustomAnalysis
import ast
import subprocess
import json
import tempfile
import os
from radon.complexity import cc_visit
import autopep8
import bandit

def perform_ast_analysis(code_snippet):
    ast_errors = []

    try:
        # Attempt to parse the code snippet
        ast.parse(code_snippet)
    except SyntaxError as e:
        # If there's a syntax error, capture the error details
        ast_errors.append({
            'line': e.lineno,
            'message': e.msg
        })

    # Return AST analysis results as a dictionary
    return {'ast_errors': ast_errors}
    

import subprocess
import tempfile
import json

def perform_pylint_analysis(code_snippet):
    pylint_results = []

    # Write code snippet to a temporary file with specified encoding
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py',encoding='utf-8') as temp_file:
        temp_file.write(code_snippet)
        temp_file_path = temp_file.name

    try:
        # Run Pylint
        pylint_command = ['pylint', '--output-format=json', temp_file_path]
        pylint_process = subprocess.Popen(pylint_command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           universal_newlines=True)
        pylint_output, pylint_error = pylint_process.communicate()

        if pylint_process.returncode == 0:
            pylint_data = json.loads(pylint_output)
            pylint_results = pylint_data
        else:
            pylint_results.append({
                'error': 'Pylint encountered an error',
                'output': pylint_output,
                'error_output': pylint_error
            })
    finally:
        # Remove temporary file
        os.unlink(temp_file_path)

    return pylint_results



def perform_radon_analysis(code_snippet):
    from radon.cli import Config
    from radon.complexity import cc_rank, cc_visit

    # Initialize radon_results dictionary
    radon_results = {}

    # Set up Radon configuration
    config = Config(exclude='')

    try:
        # Perform Radon analysis
        results = cc_visit(code_snippet)

        # Extract complexity and rank
        complexity = results[0].complexity  # Complexity value
        rank = cc_rank(complexity)          # Rank (A, B, C, D, E, or F)

        # Store the results in the radon_results dictionary
        radon_results = {
            'complexity': complexity,
            'rank': rank
        }
    except Exception as e:
        # Handle any errors that occur during analysis
        radon_results = {
            'error': str(e)
        }
    
    # Return the radon_results dictionary
    return radon_results

def perform_bandit_analysis(code_snippet):
    bandit_results = {}

    # Create a temporary file to write the code snippet
    temp_file_path = 'temp_code.py'
    with open(temp_file_path, 'w') as file:
        file.write(code_snippet)

    # Run Bandit on the temporary file and capture the output
    bandit_process = subprocess.Popen(['bandit', '--format', 'json', temp_file_path], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bandit_output, bandit_error = bandit_process.communicate()

    # Delete the temporary file
    os.remove(temp_file_path)

    if bandit_process.returncode == 0:
        try:
            # Parse the JSON output from Bandit
            bandit_results = json.loads(bandit_output)
        except json.JSONDecodeError:
            return {'error': 'Error parsing Bandit JSON output'}
    else:
        # Handle the internal Bandit error separately
        return {'error': 'Bandit encountered an error: ' + bandit_error.decode('utf-8').strip()}

    return bandit_results

def format_code_snippet(code_snippet):
    # Format the code snippet using autopep8
    formatted_code = autopep8.fix_code(code_snippet)

    return formatted_code
#     # return autopep8_results

# def perform_ast_visualization(code_snippet):
#     # ... your logic for AST visualization ...
#     return visualization_data 


def submit_code(request):
    form = CodeSnippetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            code_obj = form.save()
            
            format_requested = request.POST.get('format_requested', False)

            # If formatting is requested, format the code snippet
            if format_requested:
                formatted_code = format_code_snippet(code_obj.code_snippet)
            else:
                formatted_code = None

            # Perform AST analysis
            ast_results = perform_ast_analysis(code_obj.code_snippet)

            # Perform Pylint analysis
            pylint_results = perform_pylint_analysis(code_obj.code_snippet)

            # Perform Radon analysis
            radon_results = perform_radon_analysis(code_obj.code_snippet)
            
            # Perform Bandit analysis
            bandit_results = perform_bandit_analysis(code_obj.code_snippet)

            # Perform AST visualization
            # visualization_data = perform_ast_visualization(code_obj.code_snippet)


            # Combine all analysis results into a single dictionary
            analysis_results = {
                'ast': ast_results,
                'pylint': pylint_results,
                'radon': radon_results,
                'bandit': bandit_results,
                # 'visualization': visualization_data
            }

            # Save analysis results
            Analysis.objects.create(
                code_snippet=code_obj,
                analysis_results=analysis_results
            )
            
            CustomAnalysis.objects.create(
                code_snippet=code_obj,
                formatted_code=formatted_code,
                # analysis=analysis_instance,
                analysis_results1={}  # Assuming analysis_results1 is for other analysis results
            )

            # Redirect to the index page
            return render(request, 'index.html', {'form': form, 'analysis_results': analysis_results})  # Replace 'index' with the correct URL name
    return render(request, 'index.html', {'form': form})


# def custom_analysis():