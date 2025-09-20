# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This repository is currently in its initial state with minimal content:
- Contains a Google Cloud Platform service account JSON file (`dr-murzoglu-doktora.json`)
- No source code or build configuration files present yet

## Important Security Note

The repository contains a service account key file (`dr-murzoglu-doktora.json`) with sensitive credentials. When working with this repository:
- Never commit changes to the service account file
- Consider adding it to `.gitignore` to prevent accidental exposure
- Use environment variables or secure secret management for production deployments

## Future Development

When code is added to this repository, update this file with:
- Build and run commands specific to the chosen technology stack
- Testing commands and frameworks
- Project-specific architecture details
- Development workflow instructions