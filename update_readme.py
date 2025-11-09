#!/usr/bin/env python3
"""
GitHub Activity README Updater
Fetches your GitHub activity from the last 30 days and updates your README
"""

import os
import sys
from datetime import datetime, timedelta
import requests
from collections import defaultdict

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')

if not GITHUB_TOKEN or not GITHUB_USERNAME:
    print("Error: GITHUB_TOKEN and GITHUB_USERNAME must be set")
    sys.exit(1)

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_user_events():
    """Fetch recent events for the user"""
    url = f'https://api.github.com/users/{GITHUB_USERNAME}/events'
    events = []
    page = 1
    
    # Fetch multiple pages to get 30 days of data
    while page <= 10:  # Limit to 10 pages (300 events max)
        response = requests.get(f'{url}?page={page}&per_page=30', headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching events: {response.status_code}")
            break
        
        page_events = response.json()
        if not page_events:
            break
            
        events.extend(page_events)
        
        # Check if we've gone back far enough (30 days)
        if page_events:
            oldest_event = datetime.strptime(page_events[-1]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if oldest_event < datetime.utcnow() - timedelta(days=30):
                break
        
        page += 1
    
    return events

def fetch_user_stats():
    """Fetch user's general stats"""
    url = f'https://api.github.com/users/{GITHUB_USERNAME}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}

def analyze_events(events):
    """Analyze events and return statistics"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    stats = {
        'commits': 0,
        'prs_opened': 0,
        'prs_merged': 0,
        'issues_opened': 0,
        'issues_commented': 0,
        'repos_contributed': set(),
        'review_comments': 0,
        'stars_given': 0,
        'repos_created': 0,
        'events_by_day': defaultdict(int)
    }
    
    for event in events:
        event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        
        # Only count events from last 30 days
        if event_date < thirty_days_ago:
            continue
        
        event_type = event['type']
        repo_name = event['repo']['name']
        day_key = event_date.strftime('%Y-%m-%d')
        
        stats['events_by_day'][day_key] += 1
        stats['repos_contributed'].add(repo_name)
        
        if event_type == 'PushEvent':
            stats['commits'] += len(event['payload'].get('commits', []))
        elif event_type == 'PullRequestEvent':
            if event['payload']['action'] == 'opened':
                stats['prs_opened'] += 1
            elif event['payload']['action'] == 'closed' and event['payload']['pull_request'].get('merged'):
                stats['prs_merged'] += 1
        elif event_type == 'IssuesEvent' and event['payload']['action'] == 'opened':
            stats['issues_opened'] += 1
        elif event_type == 'IssueCommentEvent':
            stats['issues_commented'] += 1
        elif event_type == 'PullRequestReviewCommentEvent':
            stats['review_comments'] += 1
        elif event_type == 'WatchEvent':
            stats['stars_given'] += 1
        elif event_type == 'CreateEvent' and event['payload']['ref_type'] == 'repository':
            stats['repos_created'] += 1
    
    stats['repos_contributed'] = len(stats['repos_contributed'])
    return stats

def create_activity_chart(events_by_day):
    """Create a simple text-based activity chart"""
    if not events_by_day:
        return "No activity in the last 30 days"
    
    # Get last 30 days
    today = datetime.utcnow()
    days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
    
    # Determine max for scaling
    max_events = max(events_by_day.values()) if events_by_day else 1
    
    chart_lines = []
    chart_lines.append("```")
    chart_lines.append("Activity over the last 30 days:")
    chart_lines.append("")
    
    # Create bars
    for day in days:
        count = events_by_day.get(day, 0)
        bar_length = int((count / max_events) * 20) if max_events > 0 else 0
        bar = '█' * bar_length
        date_label = datetime.strptime(day, '%Y-%m-%d').strftime('%m/%d')
        chart_lines.append(f"{date_label} │{bar} {count}")
    
    chart_lines.append("```")
    return '\n'.join(chart_lines)

def generate_activity_section(stats):
    """Generate the activity section of the README"""
    chart = create_activity_chart(stats['events_by_day'])
    
    content = [
        "### 🎯 Activity Summary",
        "",
        f"- **{stats['commits']}** commits pushed",
        f"- **{stats['prs_opened']}** pull requests opened",
        f"- **{stats['issues_opened']}** issues opened",
        f"- **{stats['issues_commented']}** issue comments",
        f"- **{stats['review_comments']}** review comments",
        f"- **{stats['repos_contributed']}** repositories contributed to",
        "",
        chart
    ]
    
    return '\n'.join(content)

def generate_stats_section(user_stats, recent_stats):
    """Generate the stats section"""
    content = [
        f"![Followers](https://img.shields.io/badge/Followers-{user_stats.get('followers', 0)}-blue?style=flat-square)",
        f"![Public Repos](https://img.shields.io/badge/Public_Repos-{user_stats.get('public_repos', 0)}-green?style=flat-square)",
        f"![Total Stars](https://img.shields.io/badge/Total_Stars-{user_stats.get('public_gists', 0)}-yellow?style=flat-square)",
        "",
        "### 📈 This Month's Highlights",
        "",
        f"- 🔨 **{recent_stats['commits']}** commits",
        f"- 🔀 **{recent_stats['prs_opened']}** PRs opened",
        f"- ⭐ **{recent_stats['stars_given']}** repositories starred",
        f"- 📦 **{recent_stats['repos_created']}** new repositories created",
    ]
    
    return '\n'.join(content)

def update_readme(activity_content, stats_content):
    """Update the README.md file with new content"""
    readme_path = 'README.md'
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    
    # Update activity section
    activity_start = '<!-- ACTIVITY_START -->'
    activity_end = '<!-- ACTIVITY_END -->'
    activity_section = f"{activity_start}\n{activity_content}\n{activity_end}"
    
    # Update stats section
    stats_start = '<!-- STATS_START -->'
    stats_end = '<!-- STATS_END -->'
    stats_section = f"{stats_start}\n{stats_content}\n{stats_end}"
    
    # Update date
    date_start = '<!-- DATE_START -->'
    date_end = '<!-- DATE_END -->'
    date_section = f"{date_start}{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}{date_end}"
    
    # Replace sections
    import re
    
    readme = re.sub(
        f'{activity_start}.*?{activity_end}',
        activity_section,
        readme,
        flags=re.DOTALL
    )
    
    readme = re.sub(
        f'{stats_start}.*?{stats_end}',
        stats_section,
        readme,
        flags=re.DOTALL
    )
    
    readme = re.sub(
        f'{date_start}.*?{date_end}',
        date_section,
        readme,
        flags=re.DOTALL
    )
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("README.md updated successfully!")

def main():
    print("Fetching GitHub activity...")
    events = fetch_user_events()
    print(f"Found {len(events)} events")
    
    print("Analyzing events...")
    stats = analyze_events(events)
    
    print("Fetching user stats...")
    user_stats = fetch_user_stats()
    
    print("Generating content...")
    activity_content = generate_activity_section(stats)
    stats_content = generate_stats_section(user_stats, stats)
    
    print("Updating README...")
    update_readme(activity_content, stats_content)
    
    print("Done!")

if __name__ == '__main__':
    main()
