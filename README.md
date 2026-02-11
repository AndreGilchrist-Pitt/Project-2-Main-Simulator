# Project-2-Main-Simulator

## Branches

### **main**

- Production/stable branch containing tested and approved code
- All code here should be fully functional and tested
- Direct commits are discouraged; use pull requests from Development

### **Development**

- Active development branch for new features and changes
- All new work should be done here first
- Test your changes before merging to main

## Workflow

1. **Start Development**: Switch to the `Development` branch
2. **Make Changes**: Implement features, bug fixes, or improvements
3. **Test**: Run unit tests to ensure functionality
4. **Commit**: Commit changes to `Development` branch
5. **Merge**: Once stable and tested, create a pull request to merge into `main`
6. **Review**: Review changes before merging to production

## Directory Structure

### Path Configuration

The `Paths/paths.py` file defines centralized path constants for the project:

- `PROJECT_ROOT`: Root directory of the project
- `SRC_DIR`: Source code directory (`Src/`)
- `UTILS_DIR`: Utilities directory (`Src/Utils/`)
- `CLASSES_DIR`: Classes directory (`Src/Utils/Classes/`)
- `CLASS_DIAGRAMS_DIR`: Class diagrams directory (`Src/Utils/ClassDiagrams/`)
- `UNITTEST_DIR`: Unit test directory (`UnitTest/`)
- `UNITTEST_CLASSES_DIR`: Unit test classes directory (`UnitTest/Classes/`)

Use these path constants in your code to ensure consistent file paths across the project.
