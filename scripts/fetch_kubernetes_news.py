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