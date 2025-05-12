# Contributing to KubeFeeds

Thank you for your interest in contributing to KubeFeeds! This document provides guidelines and instructions for contributing to this project.

## How Can I Contribute?

### Expanding the Topic Database

One of the most valuable ways to contribute is by expanding our Kubernetes topic database:

1. Open `scripts/generate_post.py`
2. Locate the `KUBERNETES_TOPICS` list
3. Add new relevant Kubernetes topics
4. Submit a pull request with your changes

### Improving Post Templates

You can enhance the quality of our auto-generated content by improving the templates:

1. Open `scripts/generate_post.py`
2. Locate the `POST_TEMPLATES` dictionary
3. Modify existing templates or add new ones
4. Submit a pull request with your changes

### Adding Example YAML Configurations

Help us provide better examples for Kubernetes resources:

1. Add your well-commented YAML examples to the `examples/` directory
2. Update the `generate_example_yaml` function in `scripts/generate_post.py`
3. Submit a pull request with your changes

### Improving the Website

Enhance the blog appearance and functionality:

1. Modify the Jekyll theme configuration in `_config.yml`
2. Add new pages or improve existing ones in the `_pages/` directory
3. Enhance the site's CSS in `assets/css/`
4. Submit a pull request with your changes

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Setting Up Locally

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/kubefeeds.git
cd kubefeeds

# Install dependencies
bundle install

# Run the site locally
bundle exec jekyll serve
```

### Using Docker

```bash
# Run with Docker
docker-compose up
```

## Commit Message Guidelines

We follow conventional commits for clear communication:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc; no code change
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to the build process or auxiliary tools

Example: `feat: add support for StatefulSet examples`

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## Questions?

If you have any questions about contributing, please open an issue or start a discussion.

---

Thank you for helping improve KubeFeeds!
