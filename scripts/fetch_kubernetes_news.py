#!/usr/bin/env python3

import os
import re
import json
import yaml
import random
import datetime
import requests
from pathlib import Path

# Sources for Kubernetes content
SOURCES = {
    "blogs": [
        {
            "name": "Kubernetes Blog",
            "url": "https://kubernetes.io/blog/",
            "rss": "https://kubernetes.io/feed.xml",
            "type": "official"
        },
        {
            "name": "CNCF Blog",
            "url": "https://www.cncf.io/blog/",
            "rss": "https://www.cncf.io/feed/",
            "type": "official"
        },
        {
            "name": "Google Kubernetes Blog",
            "url": "https://cloud.google.com/blog/products/containers-kubernetes",
            "type": "vendor"
        },
        {
            "name": "AWS Containers Blog",
            "url": "https://aws.amazon.com/blogs/containers/",
            "rss": "https://aws.amazon.com/blogs/containers/feed/",
            "type": "vendor"
        }
    ],
    "github": [
        {
            "name": "Kubernetes",
            "repo": "kubernetes/kubernetes",
            "type": "official"
        },
        {
            "name": "Helm",
            "repo": "helm/helm",
            "type": "official"
        },
        {
            "name": "Istio",
            "repo": "istio/istio",
            "type": "ecosystem"
        }
    ]
}

# GitHub API token (should be stored as an environment variable in production)
def get_github_token():
    return os.environ.get('GITHUB_TOKEN', '')

# Fetch latest releases from GitHub repositories
def fetch_github_releases(repo, limit=5):
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {}
    token = get_github_token()
    if token:
        headers['Authorization'] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        releases = response.json()
        return releases[:limit]
    else:
        print(f"Error fetching releases for {repo}: {response.status_code}")
        return []

# Fetch latest issues and PRs from GitHub repositories
def fetch_github_activity(repo, limit=5):
    # Get recent issues
    issues_url = f"https://api.github.com/repos/{repo}/issues"
    headers = {}
    token = get_github_token()
    if token:
        headers['Authorization'] = f"token {token}"
    
    params = {
        'state': 'all',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': limit
    }
    
    response = requests.get(issues_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching issues for {repo}: {response.status_code}")
        return []

# Parse RSS feeds
def fetch_rss_feed(feed_url, limit=5):
    try:
        import feedparser
        feed = feedparser.parse(feed_url)
        entries = feed.entries[:limit]
        results = []
        
        for entry in entries:
            post = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', entry.get('updated', '')),
                'summary': entry.get('summary', ''),
            }
            results.append(post)
        
        return results
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
        return []

# Scrape blog content when RSS is not available
def scrape_blog(url, limit=5):
    try:
        from bs4 import BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a generic approach; each blog might need specific selectors
        posts = []
        
        # Look for common blog post patterns
        articles = soup.find_all('article') or \
                  soup.find_all('div', class_=re.compile(r'post|article|blog-item'))
        
        for article in articles[:limit]:
            # Try to find title
            title_elem = article.find('h1') or article.find('h2') or article.find('h3')
            if not title_elem:
                continue
            
            title = title_elem.text.strip()
            
            # Try to find link
            link_elem = title_elem.find('a') or article.find('a', class_=re.compile(r'read-more|more-link'))
            link = ''
            if link_elem and 'href' in link_elem.attrs:
                link = link_elem['href']
                # Make relative URLs absolute
                if not link.startswith('http'):
                    if link.startswith('/'):
                        # Get the base URL
                        parsed_url = requests.utils.urlparse(url)
                        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        link = base_url + link
                    else:
                        link = url + ('/' if not url.endswith('/') else '') + link
            
            # Try to find date
            date_elem = article.find('time') or \
                       article.find('span', class_=re.compile(r'date|time|published'))
            
            date = date_elem.text.strip() if date_elem else ''
            
            # Try to find summary
            summary_elem = article.find('p')
            summary = summary_elem.text.strip() if summary_elem else ''
            
            posts.append({
                'title': title,
                'link': link,
                'published': date,
                'summary': summary
            })
        
        return posts
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Generate a news post from the collected blog posts
def generate_news_post(blog_posts):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}-kubernetes-latest-news.md"
    
    content = f"---\ntitle: \"Latest Kubernetes News and Updates\"\ndate: {today}\ncategories:\n  - News\ntags:\n  - kubernetes\n  - news\n  - updates\n---\n\n# Latest Kubernetes News and Updates\n\nStay informed with the latest news, tutorials, and updates from around the Kubernetes ecosystem. Here's a roundup of recent articles from official sources and community contributors.\n\n"
    
    # Group posts by source type
    official_posts = [post for post in blog_posts if post['source_type'] == 'official']
    vendor_posts = [post for post in blog_posts if post['source_type'] == 'vendor']
    
    # Add official posts
    if official_posts:
        content += "## Official Kubernetes Updates\n\n"
        for post in official_posts[:5]:  # Limit to 5 posts
            published = post.get('published', 'Recently')
            summary = post.get('summary', '').strip()
            if len(summary) > 200:
                summary = summary[:200].strip() + "..."
            
            content += f"### [{post['title']}]({post['link']})\n\n"
            content += f"*Published: {published} by {post['source']}*\n\n"
            content += f"{summary}\n\n"
            content += f"[Read more...]({post['link']})\n\n"
    
    # Add vendor posts
    if vendor_posts:
        content += "## Cloud Provider & Vendor Updates\n\n"
        for post in vendor_posts[:5]:  # Limit to 5 posts
            published = post.get('published', 'Recently')
            summary = post.get('summary', '').strip()
            if len(summary) > 200:
                summary = summary[:200].strip() + "..."
            
            content += f"### [{post['title']}]({post['link']})\n\n"
            content += f"*Published: {published} by {post['source']}*\n\n"
            content += f"{summary}\n\n"
            content += f"[Read more...]({post['link']})\n\n"
    
    content += "## Stay Connected\n\nFor more Kubernetes news, follow the [Kubernetes Blog](https://kubernetes.io/blog/) and join the community on [Slack](https://kubernetes.slack.com/)."
    
    return filename, content

# Generate a post about GitHub releases
def generate_releases_post(releases):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}-kubernetes-ecosystem-releases.md"
    
    content = f"---\ntitle: \"Latest Kubernetes Ecosystem Releases\"\ndate: {today}\ncategories:\n  - Releases\ntags:\n  - kubernetes\n  - releases\n  - github\n---\n\n# Latest Kubernetes Ecosystem Releases\n\nStay informed about the latest releases from the Kubernetes ecosystem. This post covers recent releases from core Kubernetes components and popular tools.\n\n"
    
    # Process each repository's releases
    for repo_info in SOURCES['github']:
        repo_releases = []
        for release in releases:
            if release.get('repo') == repo_info['repo']:
                repo_releases.append(release)
        
        if repo_releases:
            content += f"## {repo_info['name']} ({repo_info['repo']})\n\n"
            
            for release in repo_releases[:3]:  # Limit to 3 releases per repo
                release_date = release['published_at'].split('T')[0] if 'T' in release['published_at'] else release['published_at']
                release_notes = release.get('body', '').strip()
                # Extract first 200 chars for summary
                release_summary = release_notes[:200].strip()
                if len(release_notes) > 200:
                    release_summary += "..."
                
                content += f"### [{release['tag']}]({release['url']})\n\n"
                content += f"*Released: {release_date}*\n\n"
                content += f"{release_summary}\n\n"
                content += f"[View full release notes]({release['url']})\n\n"
    
    content += "## Stay Updated\n\nFor more release information, follow the GitHub repositories of your favorite Kubernetes tools and components."
    
    return filename, content

# Main function to generate blog posts from fetched content
def main():
    print("Fetching content from Kubernetes sources...")
    
    # Create posts directory if it doesn't exist
    posts_dir = Path("_posts")
    posts_dir.mkdir(exist_ok=True)
    
    # Fetch blog content
    blog_posts = []
    for blog in SOURCES['blogs']:
        print(f"Fetching content from {blog['name']}...")
        if 'rss' in blog:
            posts = fetch_rss_feed(blog['rss'], 5)
        else:
            posts = scrape_blog(blog['url'], 5)
        
        for post in posts:
            post['source'] = blog['name']
            post['source_type'] = blog['type']
            blog_posts.append(post)
    
    # Fetch GitHub releases
    releases = []
    for repo_info in SOURCES['github']:
        print(f"Fetching releases from {repo_info['repo']}...")
        repo_releases = fetch_github_releases(repo_info['repo'], 3)
        for release in repo_releases:
            releases.append({
                'repo': repo_info['repo'],
                'tag': release['tag_name'],
                'url': release['html_url'],
                'published_at': release['published_at'],
                'body': release.get('body', ''),
                'type': repo_info['type']
            })
    
    # Generate news post
    if blog_posts:
        filename, content = generate_news_post(blog_posts)
        post_path = posts_dir / filename
        with open(post_path, 'w') as f:
            f.write(content)
        print(f"Generated blog post: {filename}")
    
    # Generate releases post
    if releases:
        filename, content = generate_releases_post(releases)
        post_path = posts_dir / filename
        with open(post_path, 'w') as f:
            f.write(content)
        print(f"Generated releases post: {filename}")

if __name__ == "__main__":
    main()
