# KubeFeeds: The Kubernetes Knowledge Hub

<p align="center">
  <img src="https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.png" alt="KubeFeeds Logo" width="200"/>
  <br>
  <em>Automated Kubernetes insights delivered to your feed</em>
</p>

<p align="center">
  <a href="https://github.com/ajeetraina/kubefeeds/actions/workflows/jekyll-gh-pages.yml">
    <img src="https://github.com/ajeetraina/kubefeeds/actions/workflows/jekyll-gh-pages.yml/badge.svg" alt="Build Status">
  </a>
  <a href="https://github.com/ajeetraina/kubefeeds/actions/workflows/generate-post.yml">
    <img src="https://github.com/ajeetraina/kubefeeds/actions/workflows/generate-post.yml/badge.svg" alt="Content Generation">
  </a>
  <a href="https://github.com/ajeetraina/kubefeeds/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ajeetraina/kubefeeds" alt="License">
  </a>
</p>

## ? About KubeFeeds

KubeFeeds is a cutting-edge automated content platform dedicated to Kubernetes enthusiasts, practitioners, and learners. We deliver regular, high-quality content covering the entire Kubernetes ecosystem - from fundamentals to advanced concepts, best practices to troubleshooting guides.

Powered by GitHub Pages with Jekyll and leveraging GitHub Actions for content generation, KubeFeeds provides a steady stream of valuable Kubernetes insights, tutorials, and tips to help you navigate the cloud native landscape.

## ? Content Categories

- **Guides** - Comprehensive explanations of Kubernetes concepts
- **Tutorials** - Step-by-step instructions for implementing features
- **Tips** - Best practices and optimization techniques
- **News & Updates** - Latest developments in the Kubernetes ecosystem

## ? Why KubeFeeds?

- **Always Fresh** - Regular content updates twice a week
- **Comprehensive Coverage** - From basics to advanced topics
- **Practical Examples** - Real-world YAML configurations included
- **Community-Oriented** - Open source and community-driven

## ? How It Works

KubeFeeds employs a sophisticated automated publishing pipeline:

1. Our intelligent content engine selects relevant Kubernetes topics
2. Detailed, structured content is generated with practical examples
3. Content is committed to the repository via GitHub Actions
4. Jekyll builds and deploys the site to GitHub Pages
5. New content is regularly pushed to your feed

## ? Visit Our Blog

Explore our content at [https://ajeetraina.github.io/kubefeeds/](https://ajeetraina.github.io/kubefeeds/)

## ? Contributing

We welcome contributions! Here's how you can help improve KubeFeeds:

- **Add Topics**: Expand our topic database in `scripts/generate_post.py`
- **Improve Templates**: Enhance our post templates with better structures
- **Fix Issues**: Help address any bugs or improvements
- **Share Content**: Spread the word about KubeFeeds

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## ?? Development Setup

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/ajeetraina/kubefeeds.git
cd kubefeeds

# Run with Docker
docker-compose up
```

### Traditional Setup

```bash
# Install dependencies
bundle install

# Run Jekyll locally
bundle exec jekyll serve
```

### Generate a Post Manually

```bash
# Install Python dependencies
pip install requests pyyaml

# Generate a post
python scripts/generate_post.py
```

## ? Content Schedule

New content is published automatically:
- Every Monday at 12:00 UTC
- Every Thursday at 12:00 UTC

## ? Connect With Us

- Create an [Issue](https://github.com/ajeetraina/kubefeeds/issues)
- Start a [Discussion](https://github.com/ajeetraina/kubefeeds/discussions)
- Star this repository to show your support

## ? License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ? Star KubeFeeds

If you find KubeFeeds useful, consider giving it a star on GitHub. It helps others discover this resource!

---

<p align="center">
  <em>Keeping the Kubernetes community informed and educated</em>
</p>
