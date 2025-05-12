# KubeFeeds

Automated Kubernetes blog posts and updates.

## About

KubeFeeds is an automated blog that regularly generates and posts content about various Kubernetes topics. The blog is powered by GitHub Pages with Jekyll and uses GitHub Actions for automated content generation and publishing.

## Features

- Automated blog post generation using GitHub Actions
- Regular posting schedule (twice per week)
- Content focused on Kubernetes topics
- Minimal Mistakes Jekyll theme

## How it Works

1. A GitHub Action runs on a schedule (Mondays and Thursdays)
2. The action executes the `scripts/generate_post.py` script
3. The script selects a random Kubernetes topic and generates a post
4. The post is committed to the repository
5. GitHub Pages automatically builds and publishes the site

## Local Development

### Prerequisites

- Ruby and Bundler
- Jekyll

### Setup

```bash
# Clone the repository
git clone https://github.com/ajeetraina/kubefeeds.git
cd kubefeeds

# Install dependencies
bundle install

# Run the site locally
bundle exec jekyll serve
```

Alternatively, you can use Docker:

```bash
docker-compose up
```

### Manual Post Generation

You can manually generate a new post locally:

```bash
# Install Python dependencies
pip install requests pyyaml

# Generate a new post
python scripts/generate_post.py
```

## Customization

### Modifying Topics

Edit the `KUBERNETES_TOPICS` list in `scripts/generate_post.py` to add or remove topics.

### Changing Post Templates

Modify the `POST_TEMPLATES` dictionary in `scripts/generate_post.py` to change the structure and format of generated posts.

### Adjusting the Schedule

Edit the cron schedule in `.github/workflows/generate-post.yml` to change how frequently posts are generated.

## Enabling GitHub Pages

1. Go to the repository settings
2. Navigate to Pages
3. Set the source to 'GitHub Actions'

## License

MIT
