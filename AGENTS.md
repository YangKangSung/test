
# Agentic Coding Guidelines

This document outlines the guidelines for agentic coding operations within this repository. Adhering to these guidelines ensures consistency, maintainability, and efficient collaboration.

## Project Structure

The main project is located in `anythingllm/anythingllm-embed/`. This is an embeddable chat widget for AnythingLLM built with React, Vite, and Tailwind CSS.

```
anythingllm-embed/
├── src/
│   ├── components/     # React components (index.jsx pattern)
│   ├── hooks/         # Custom React hooks
│   ├── models/       # API services and business logic
│   ├── utils/        # Utility functions
│   ├── assets/       # Static assets
│   ├── App.jsx       # Main app component
│   └── main.jsx      # Entry point
├── index.html        # Development HTML template
├── vite.config.js    # Vite configuration
└── tailwind.config.js
```

## 1. Build, Lint, and Test Commands

All commands should be run from `anythingllm/anythingllm-embed/` directory.

### 1.1. Build Commands

-   **Development Build:**
    ```bash
    cd anythingllm/anythingllm-embed
    yarn dev
    ```
    This command starts a development server with hot-reloading for continuous development. Opens on port 3080.

-   **Production Build:**
    ```bash
    cd anythingllm/anythingllm-embed
    yarn build
    ```
    This command builds the project for production, optimizing and minifying CSS and JavaScript assets. Output goes to `dist/`.

-   **Build for Publish:**
    ```bash
    cd anythingllm/anythingllm-embed
    yarn build:publish
    ```
    Builds and copies output to the main frontend's public embed directory.

### 1.2. Linting Commands

-   **Code Formatting:**
    ```bash
    cd anythingllm/anythingllm-embed
    yarn lint
    ```
    This command uses Prettier to format the code within the `./src` directory. It respects ignore rules specified in `../.prettierignore`.

### 1.3. Test Commands

-   **Running Tests:**
    This project uses Playwright (installed at root level). Tests should be placed in a `tests/` directory at the project root.
    ```bash
    # From root directory
    yarn playwright test
    # or
    npx playwright test
    ```

-   **Running a Single Test:**
    ```bash
    yarn playwright test tests/path/to/your/testfile.spec.ts
    # or
    npx playwright test tests/path/to/your/testfile.spec.ts
    ```

## 2. Code Style Guidelines

This section details the code style conventions, including imports, formatting, types, naming conventions, and error handling.

### 2.1. Imports

-   Imports should be grouped logically (e.g., third-party libraries, local modules).
-   Use the `@` alias for internal imports (maps to `src/` directory):
    ```javascript
    import useGetScriptAttributes from "@/hooks/useScriptAttributes";
    import Head from "@/components/Head";
    ```
-   Avoid wildcard imports (`import * as ...`) unless necessary.
-   Sort imports alphabetically within groups.

### 2.2. Formatting

-   Code formatting is managed by Prettier via `yarn lint`.
-   Use 2 spaces for indentation.
-   Use semicolons in JavaScript.
-   Use single quotes for strings.

### 2.3. Tailwind CSS

-   This project uses Tailwind CSS with a custom prefix `allm-` to avoid conflicts with host page styles.
-   **Always use the `allm-` prefix** for all Tailwind classes:
    ```jsx
    <div className="allm-flex allm-flex-col allm-bg-white allm-p-4">
      <button className="allm-text-white allm-bg-blue-500">Click</button>
    </div>
    ```
-   Do not use unprefixed Tailwind classes - they will not work.
-   Preflight is disabled in `tailwind.config.js`.

### 2.4. Types

-   TypeScript is used with JSDoc comments for type information where beneficial.
-   Leverage built-in types and interfaces for clarity and maintainability.
-   Use PropTypes or TypeScript for component props documentation.

### 2.5. Naming Conventions

-   **Variables and Functions:** Use camelCase (e.g., `myVariable`, `calculateTotal`, `useEffect`).
-   **Constants:** Use SCREAMING_SNAKE_CASE for globally recognized constants (e.g., `DEFAULT_SETTINGS`, `MAX_RETRIES`).
-   **React Components:** Use PascalCase (e.g., `ChatWindow`, `OpenButton`).
-   **Files:** Use kebab-case for non-component files (e.g., `chat-service.js`, `use-script-attributes.js`).
-   **Component Folders:** Use index.jsx pattern (e.g., `ChatWindow/index.jsx`).
-   Be descriptive with names; avoid overly abbreviated or ambiguous terms.

### 2.6. React Patterns

-   Use functional components with Hooks exclusively.
-   Use `useEffect` for side effects, managing dependencies carefully.
-   Use `useState` and `useReducer` for state management.
-   Use default exports for components.
-   Consider memoization (`React.memo`, `useMemo`, `useCallback`) to optimize performance for expensive renders.
-   Define custom hooks in `src/hooks/` with `use` prefix (e.g., `useSessionId`, `useOpen`).

### 2.7. Error Handling

-   Implement robust error handling using `try...catch` blocks for asynchronous operations or sections prone to failure.
-   Provide meaningful error messages to aid debugging.
-   Use `console.error()` for logging errors (as seen in the codebase).
-   Consider using custom error types or standardized error objects where appropriate.
-   For API interactions, handle potential network errors, timeouts, and non-2xx responses gracefully.
-   Example pattern from codebase:
    ```javascript
    .catch((e) => {
      console.error(e);
      return []; // Return safe fallback
    });
    ```

## 3. Cursor and Copilot Rules

No specific Cursor rules (`.cursor/rules/` or `.cursorrules`) or Copilot instructions (`.github/copilot-instructions.md`) were found in the scanned locations. If such rules are introduced, they should be documented here.

## 4. General Development Practices

-   Write clear and concise code.
-   Add comments to explain complex logic or non-obvious code sections, focusing on the "why" rather than the "what".
-   Keep functions and components small and focused on a single responsibility.
-   Regularly run `yarn lint` to ensure code style consistency.
-   When testing, ensure tests are run frequently, especially before committing changes.
-   Follow the existing component structure (index.jsx pattern with folder-based components).
-   Use the `@` import alias for internal modules instead of relative paths when possible.
