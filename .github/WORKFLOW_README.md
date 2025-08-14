
# Automated Testing and GitHub Workflows

To ensure the stability and reliability of our Python game project, we implemented automated testing and GitHub workflows as part of our development process.  
Here is the [Test file.](https://github.com/lkomenski/Soft204-Python-Final-Project--Snake-Game-Mod/blob/main/.github/test_basics.py)  
Here is the [Workflow.](https://github.com/lkomenski/Soft204-Python-Final-Project--Snake-Game-Mod/blob/main/.github/workflows/python-app.yml)  

## Purpose of Automated Tests 
Automated tests are designed to verify the core gameplay logic — such as collision detection, score updates, and direction changes. These tests serve two key purposes:

# Validate Essential Game Mechanics 
We pre-identified critical functions that define how the game operates. By writing tests for these components, we ensure they behave as expected under various conditions.

# Prevent Breaking Changes
As team members contribute new features or edits, automated tests run in the background to confirm that existing functionality remains intact. If a change disrupts core logic, the test will fail and alert us before the code is merged.

## Role of GitHub Workflows 
GitHub workflows automate the process of running tests, checking code style, and reporting test coverage. Every time someone pushes code or opens a pull request to the main branch, the workflow:

Installs project dependencies
Runs all test files in the tests/ directory using pytest
Generates a coverage report using coverage
Checks code style using PyLint
This automation ensures that all contributions meet our quality standards and that the game remains functional throughout development.

## Benefits 
# Confidence in Code Quality 
We can merge changes knowing they’ve passed all checks.

# Efficient Collaboration 
Team members don’t need to manually test each change.

# Professional Development Practices 
Our setup mirrors real-world software engineering workflows.

By integrating automated testing and GitHub workflows, we created a robust and maintainable project that supports teamwork and continuous improvement.

