# Contributing

Thank you for helping improve this project.

## Development Workflow

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Keep detection, counting, ESP32 communication, and report behavior unchanged unless a task explicitly requires it.
4. Add focused tests for route or integration changes.
5. Run the smoke tests before opening a pull request.

## Code Style

- Keep Flask routes in `app/routes`.
- Keep integrations and helper modules in `app/services`.
- Use environment variables for credentials and deployment-specific settings.
- Do not commit generated folders, logs, caches, local virtual environments, or temporary uploads.

## Pull Request Checklist

- Existing routes and response formats are preserved.
- No secrets or local credentials are committed.
- Temporary and generated files are ignored.
- Documentation is updated when setup or behavior changes.
