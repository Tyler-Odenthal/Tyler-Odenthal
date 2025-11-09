# GitHub Activity README Setup Guide

This setup will automatically update your GitHub profile README with your recent activity stats.

## 🚀 Quick Start

### 1. Create a Profile Repository

If you haven't already, create a repository with the same name as your GitHub username. For example, if your username is `johndoe`, create a repository named `johndoe`.

This repository is special - GitHub will display its README.md on your profile page!

### 2. Add Files to Your Repository

Copy these files to your profile repository:

```
your-username/
├── .github/
│   └── workflows/
│       └── update-activity.yml
├── README.md
└── update_readme.py
```

### 3. Customize Your README

Edit `README.md` to personalize it. You can add:
- A header with your name and bio
- Links to your social media
- Your skills and interests
- Projects you're working on

**Important:** Keep these comment markers in your README - they're used to update the activity sections:
- `<!-- ACTIVITY_START -->` and `<!-- ACTIVITY_END -->`
- `<!-- STATS_START -->` and `<!-- STATS_END -->`
- `<!-- DATE_START -->` and `<!-- DATE_END -->`

### 4. Enable GitHub Actions

1. Go to your repository settings
2. Navigate to "Actions" → "General"
3. Under "Workflow permissions", select "Read and write permissions"
4. Click "Save"

### 5. Run the Action

You can either:
- **Wait for automatic update:** The action runs daily at midnight UTC
- **Manual trigger:** Go to "Actions" tab → "Update GitHub Activity" → "Run workflow"

## 📊 What Gets Tracked?

The script tracks your activity over the last 30 days:

- 🔨 **Commits** - All commits you've pushed
- 🔀 **Pull Requests** - PRs you've opened and merged
- 🐛 **Issues** - Issues you've opened
- 💬 **Comments** - Comments on issues and PRs
- 👀 **Reviews** - Code review comments
- 📦 **Repositories** - Repos you've contributed to
- ⭐ **Stars** - Repositories you've starred

## 🎨 Customization Options

### Change Update Frequency

Edit `.github/workflows/update-activity.yml` and modify the cron schedule:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Run every 6 hours
  # or
  - cron: '0 12 * * *'   # Run daily at noon UTC
```

### Modify Activity Window

Edit `update_readme.py` and change the timedelta:

```python
thirty_days_ago = datetime.utcnow() - timedelta(days=30)  # Change 30 to your preferred days
```

### Customize the Display

You can modify the `generate_activity_section()` and `generate_stats_section()` functions in `update_readme.py` to change:
- Which stats are displayed
- The format and styling
- The chart appearance

### Add More Badges

Add shields.io badges to your README for visual appeal:

```markdown
![Profile Views](https://komarev.com/ghpvc/?username=your-username&color=blue)
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=your-username)
```

## 🔧 Troubleshooting

### Action Fails with "Permission Denied"

Make sure you've enabled "Read and write permissions" for GitHub Actions in your repository settings.

### No Activity Showing

- Check that your GitHub username is correct
- Verify you have public activity on GitHub
- Try running the workflow manually to see error messages

### Stats Not Updating

- Check the Actions tab for error logs
- Ensure the README.md has the correct comment markers
- Verify the workflow has proper permissions

## 🌟 Advanced Features

### Add More Statistics

You can extend `analyze_events()` to track additional events:

```python
elif event_type == 'ForkEvent':
    stats['forks_created'] += 1
elif event_type == 'ReleaseEvent':
    stats['releases_published'] += 1
```

### Create Contribution Graphs

Consider integrating with services like:
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)
- [GitHub Profile Trophy](https://github.com/ryo-ma/github-profile-trophy)
- [GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats)

### Add Language Statistics

Fetch and display your most-used programming languages using the GitHub API's language statistics endpoint.

## 📝 Example README Structure

```markdown
# Hi, I'm [Your Name] 👋

## About Me
Brief bio about yourself...

## 🛠️ Technologies & Tools
- Languages: Python, JavaScript, etc.
- Frameworks: React, Django, etc.

## 📊 Recent Activity (Last 30 Days)
<!-- ACTIVITY_START -->
<!-- ACTIVITY_END -->

## 🔥 Contribution Stats
<!-- STATS_START -->
<!-- STATS_END -->

## 📫 How to reach me
- Email: your.email@example.com
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)

---
*Last updated: <!-- DATE_START --><!-- DATE_END -->*
```

## 🤝 Contributing

Feel free to fork this project and customize it to your needs! If you have improvements or bug fixes, consider sharing them back.

## 📄 License

This project is open source and available for anyone to use and modify.

---

**Happy coding! 🚀**
