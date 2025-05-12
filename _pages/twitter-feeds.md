---
title: "Kubernetes Twitter Feeds"
layout: categories-sidebar
permalink: /twitter/
excerpt: "Latest tweets from the Kubernetes community"
header:
  overlay_color: "#0d47a1"
  overlay_filter: "0.5"
---

# Latest from the Kubernetes Community

Stay up-to-date with the latest tweets from the Kubernetes community. This page aggregates tweets from official Kubernetes accounts, cloud providers, and community members.

<div class="twitter-grid">
  <div class="twitter-column">
    <h2><i class="fab fa-twitter"></i> @kubernetesio</h2>
    {% include twitter-feed.html handle="kubernetesio" %}
  </div>
  
  <div class="twitter-column">
    <h2><i class="fab fa-twitter"></i> @CloudNativeFdn</h2>
    {% include twitter-feed.html handle="CloudNativeFdn" %}
  </div>
  
  <div class="twitter-column">
    <h2><i class="fab fa-twitter"></i> @thenewstack</h2>
    {% include twitter-feed.html handle="thenewstack" %}
  </div>
</div>

<style>
.twitter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  grid-gap: 20px;
  margin-top: 30px;
}

.twitter-column h2 {
  margin-bottom: 15px;
  font-size: 1.3em;
  color: #326CE5;
}

.twitter-column h2 i {
  color: #1DA1F2;
  margin-right: 8px;
}

@media (max-width: 768px) {
  .twitter-grid {
    grid-template-columns: 1fr;
  }
}
</style>