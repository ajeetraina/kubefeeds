#!/bin/bash

# Script to run the blog locally for development

# Check if Jekyll is installed
if ! command -v jekyll &> /dev/null; then
    echo "Jekyll is not installed. Installing..."
    gem install jekyll bundler
fi

# Install dependencies
bundle install

# Run Jekyll server
bundle exec jekyll serve
