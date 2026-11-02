#!/usr/bin/env bash
# Creates all labels + issues for the assignment. Requires: gh auth login (run inside the repo).
set -euo pipefail

for l in "e2e-test:0E8A16" "infra:1D76DB" "deploy:5319E7" "ci-cd:FBCA04" "database:B60205" "docs:0075CA"; do
  gh label create "${l%%:*}" --color "${l##*:}" --force
done

mk() { gh issue create --title "$1" --label "$2" --body "$3"; }

mk "Single multi-stage Dockerfile (frontend static + FastAPI)" infra "Done when: docker build works and one image serves the SPA and /api. Files: Dockerfile, .dockerignore."
mk "Migrate SQLite -> PostgreSQL (SQLAlchemy + Alembic)" database "Done when: alembic upgrade head works and scripts/migrate_sqlite_to_postgres.py copies data (row counts match)."
mk "Docker Compose: app + Postgres with healthchecks" infra "Done when: docker compose up -d --build --wait reports healthy. Files: docker-compose.yml, .env.example."

# One e2e-test issue per feature, from the templates (strip front matter)
for f in .github/ISSUE_TEMPLATE/e2e-0*.md; do
  title=$(grep -m1 '^title:' "$f" | sed 's/^title: *"\(.*\)"$/\1/')
  body=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2' "$f")
  gh issue create --title "$title" --label e2e-test --body "$body"
done

mk "Deploy to Render (Docker + managed Postgres)" deploy "render.yaml + deploy hook. Add live URL and /api/health screenshot."
mk "Deploy to Railway (Docker + Postgres plugin + volume)" deploy "railway.json. Add live URL."
mk "Deploy frontend to Vercel (proxy /api to backend)" deploy "frontend/vercel.json. Note: Vercel cannot run Docker/Compose; only the static frontend is hosted there."
mk "Deploy to AWS with CloudFormation (free tier only)" deploy "infra/aws/scriptcut.yaml: t3.micro/t2.micro, budget alert, no paid add-ons."
mk "Deploy to GCP with Terraform (alternative)" deploy "infra/terraform/gcp: e2-micro, pd-standard, free tier."
mk "CI/CD: unit, integration, E2E, build, auto-deploy on push to main" ci-cd "Workflow: .github/workflows/main.yml"
mk "README: architecture, run, test, deploy instructions" docs "Include live links and platform limitations."
