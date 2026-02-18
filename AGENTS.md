
# Agentic Coding Guidelines

This document outlines the guidelines for agentic coding operations within this repository. Adhering to these guidelines ensures consistency, maintainability, and efficient collaboration.

## 1. Build, Lint, and Test Commands

This section details the commands used for building, linting, and testing the codebase, particularly focusing on the frontend embeddable chat widget.

### 1.1. Build Commands

-   **Development Build:**
    ```bash
    yarn dev
    ```
    This command starts a development server with hot-reloading for continuous development.

-   **Production Build:**
    ```bash
    yarn build
    ```
    This command builds the project for production, optimizing and minifying CSS and JavaScript assets.

### 1.2. Linting Commands

-   **Code Formatting:**
    ```bash
    yarn lint
    ```
    This command uses Prettier to format the code within the `./src` directory. It respects ignore rules specified in `../.prettierignore` (though this file was not found during analysis).

### 1.3. Test Commands

-   **Running All Tests:**
    No explicit command for running all tests was found in the `package.json` scripts. If tests are managed by Playwright (as suggested by `@playwright/test` dependency in the root `package.json`), typical commands might involve:
    ```bash
    yarn playwright test
    # or potentially:
    npx playwright test
    ```
    *Note: The exact command may vary based on project configuration.*

-   **Running a Single Test:**
    To run a single test, you would typically use the test runner's specific options. For Playwright, this often involves specifying the test file path. For example:
    ```bash
    yarn playwright test tests/path/to/your/testfile.spec.ts
    # or potentially:
    npx playwright test tests/path/to/your/testfile.spec.ts
    ```
    *Note: Replace `tests/path/to/your/testfile.spec.ts` with the actual path to the test file you wish to run.*

    If a different testing framework is in use, consult its documentation for single-test execution commands.

## 2. Code Style Guidelines

This section details the code style conventions, including imports, formatting, types, naming conventions, and error handling.

### 2.1. Imports

-   Imports should be grouped logically (e.g., third-party libraries, local modules).
-   Alphabetical sorting of imports is recommended where applicable.
-   Avoid wildcard imports (`import * as ...`) unless necessary.

### 2.2. Formatting

-   Code formatting is managed by Prettier, as indicated by the `yarn lint` script.
-   The project appears to use standard JavaScript/TypeScript formatting conventions.
-   Consistent use of whitespace (e.g., spaces over tabs, indentation).

### 2.3. Types

-   TypeScript or JSDoc comments should be used to provide type information where beneficial, especially for complex data structures or function signatures.
-   Leverage built-in types and interfaces for clarity and maintainability.

### 2.4. Naming Conventions

-   **Variables and Functions:** Use camelCase (e.g., `myVariable`, `calculateTotal`).
-   **Constants:** Use SCREAMING_SNAKE_CASE for globally recognized constants (e.g., `MAX_RETRIES`).
-   **Classes/Components:** Use PascalCase (e.g., `UserProfile`, `ChatWidget`).
-   Be descriptive with names; avoid overly abbreviated or ambiguous terms.

### 2.5. Error Handling

-   Implement robust error handling using `try...catch` blocks for asynchronous operations or sections prone to failure.
-   Provide meaningful error messages to aid debugging.
-   Consider using custom error types or standardized error objects where appropriate.
-   For API interactions, handle potential network errors, timeouts, and non-2xx responses gracefully.

### 2.6. React Specifics

-   Functional components with Hooks are preferred.
-   Use `useEffect` for side effects, managing dependencies carefully.
-   Utilize `useState` and `useReducer` for state management.
-   Context API or state management libraries (like Redux, Zustand - though not explicitly found) can be used for global state.
-   Consider memoization (`React.memo`, `useMemo`, `useCallback`) to optimize performance for expensive renders or calculations.

## 3. Cursor and Copilot Rules

No specific Cursor rules (`.cursor/rules/` or `.cursorrules`) or Copilot instructions (`.github/copilot-instructions.md`) were found in the scanned locations. If such rules are introduced, they should be documented here.

## 4. General Development Practices

-   Write clear and concise code.
-   Add comments to explain complex logic or non-obvious code sections, focusing on the "why" rather than the "what".
-   Keep functions and components small and focused on a single responsibility.
-   Regularly run `yarn lint` to ensure code style consistency.
-   If tests are implemented, ensure they are run frequently, especially before committing changes.
