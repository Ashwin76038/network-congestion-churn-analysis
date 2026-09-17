# GitHub Safety Checklist and Push Commands

## Safety Checklist

- [ ] Confirm `data/raw/` contains only `README.md` before committing.
- [ ] Confirm clean CSV files have no customer names, phone numbers, emails, full addresses, service numbers, or staff names.
- [ ] Confirm no original Excel files are staged.
- [ ] Confirm no old `.pbix` files containing raw data are staged.
- [ ] Build the Power BI file from clean CSV files only.
- [ ] Export dashboard screenshots after the Power BI privacy review.

## Suggested Git Commands

```bash
git init
git status
git add README.md .gitignore requirements.txt data/raw/README.md data/clean data/sample scripts sql notebooks dashboard docs
git status
git commit -m "Build anonymized OLT churn analytics portfolio project"
git branch -M main
git remote add origin https://github.com/<your-username>/olt-churn-analytics.git
git push -u origin main
```

Before running `git add`, check `git status --ignored` to make sure raw source files are ignored.
