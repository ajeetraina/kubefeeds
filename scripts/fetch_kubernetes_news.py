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
        },
        {
            "name": "Microsoft AKS Blog",
            "url": "https://techcommunity.microsoft.com/t5/azure-kubernetes-service-aks/bg-p/AzureKubernetesServiceBlog",
            "type": "vendor"
        },
        {
            "name": "Red Hat OpenShift Blog",
            "url": "https://www.openshift.com/blog",
            "rss": "https://www.openshift.com/blog/feed",
            "type": "vendor"
        },
        {
            "name": "Kubernetes Podcast",
            "url": "https://kubernetespodcast.com/",
            "rss": "https://kubernetespodcast.com/feeds/audio.xml",
            "type": "community"
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
        },
        {
            "name": "Argo CD",
            "repo": "argoproj/argo-cd",
            "type": "ecosystem"
        },
        {
            "name": "Prometheus",
            "repo": "prometheus/prometheus",
            "type": "ecosystem"
        },
        {
            "name": "Knative",
            "repo": "knative/serving",
            "type": "ecosystem"
        }
    ],
    "community": [
        {
            "name": "Kubernetes Slack",
            "url": "https://kubernetes.slack.com/",
            "type": "community"
        },
        {
            "name": "Kubernetes Forums",
            "url": "https://discuss.kubernetes.io/",
            "type": "community"
        },
        {
            "name": "CNCF Calendar",
            "url": "https://www.cncf.io/calendar/",
            "type": "events"
        },
        {
            "name": "KubeCon + CloudNativeCon",
            "url": "https://www.cncf.io/kubecon-cloudnativecon-events/",
            "type": "events"
        }
    ],
    "documentation": [
        {
            "name": "Kubernetes Docs",
            "url": "https://kubernetes.io/docs/",
            "type": "official"
        },
        {
            "name": "Kubernetes GitHub Issues",
            "url": "https://github.com/kubernetes/kubernetes/issues",
            "type": "official"
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
                  soup.find_all('div', class_=re.compile(r'post|article|blog-item')) or \
                  soup.find_all('div', class_=re.compile(r'entry')) or \
                  soup.select('.post, .article, .blog-entry')
        
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
                       article.find('span', class_=re.compile(r'date|time|published')) or \
                       article.find('div', class_=re.compile(r'date|time|published'))
            
            date = date_elem.text.strip() if date_elem else ''
            
            # Try to find summary
            summary_elem = article.find('p') or article.find('div', class_=re.compile(r'summary|excerpt|description'))
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
