# ScriptCut AI

Edit a video by editing its transcript: delete text, cut the video, export an MP4.

- **Backend:** FastAPI + SQLAlchemy + Alembic, PostgreSQL, ffmpeg
- **Frontend:** React + Vite, built to static files and served by FastAPI (one Docker image)
- **Tests:** pytest (unit + integration), Vitest, Playwright E2E
- **CI/CD:** GitHub Actions (`.github/workflows/main.yml`)

## Run locally

```bash
cp .env.example .env
docker compose up -d --build --wait
open http://localhost:8000          # health: /api/health
```

## Tests

```bash
# backend (needs Postgres + ffmpeg)
cd backend && pip install -r requirements-dev.txt
export DATABASE_URL=postgresql+psycopg2://scriptcut:scriptcut@localhost:5432/scriptcut
alembic upgrade head && pytest

# frontend
cd frontend && npm install && npm run test:unit

# E2E (stack must be running; needs ffmpeg on the host)
cd e2e && npm install && npx playwright install --with-deps chromium && npx playwright test
```

One E2E spec per feature (each has a GitHub issue labelled `e2e-test`):
`01-project-creation`, `02-text-editing-sync`, `03-video-cut`, `04-export`.

## SQLite -> PostgreSQL

Schema is managed by Alembic (`backend/alembic`). To copy existing data:

```bash
python scripts/migrate_sqlite_to_postgres.py sqlite:///./old.db postgresql+psycopg2://USER:PW@HOST/DB
```

## Deployment

| Target | Files | Notes |
|---|---|---|
| Render | `render.yaml` | Builds the Dockerfile + managed Postgres. Render does not execute `docker-compose.yml`. |
| Railway | `railway.json` | Dockerfile + Postgres plugin; set `DATABASE_URL=${{Postgres.DATABASE_URL}}`, mount a volume at `/data/media`. |
| Vercel | `frontend/vercel.json` | Vercel cannot run Docker/Compose: only the static frontend is hosted, `/api` is proxied to the Render backend. |
| AWS | `infra/aws/scriptcut.yaml` | CloudFormation: one free-tier EC2 running `docker-compose.prod.yml` + budget alert. |
| GCP | `infra/terraform/gcp` | Terraform: one Always-Free `e2-micro` VM + optional budget alert. |

```bash
# AWS
aws cloudformation deploy --stack-name scriptcut --template-file infra/aws/scriptcut.yaml \
  --parameter-overrides KeyName=<key> AlertEmail=<mail> SshCidr=<ip>/32
# GCP
cd infra/terraform/gcp && cp terraform.tfvars.example terraform.tfvars && terraform init && terraform apply
```

Tear down when finished (`aws cloudformation delete-stack --stack-name scriptcut` / `terraform destroy`).

## CI/CD

On every push/PR: unit tests -> integration tests -> E2E (Playwright against `docker compose`).
On push to `main`: build and push the image to GHCR, then deploy to every target enabled by a repository variable.

| Variable (Settings > Variables) | Secrets needed |
|---|---|
| `DEPLOY_RENDER=true` | `RENDER_DEPLOY_HOOK_URL` |
| `DEPLOY_RAILWAY=true`, `RAILWAY_SERVICE` | `RAILWAY_TOKEN` |
| `DEPLOY_VERCEL=true` | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |
| `DEPLOY_VM=true` (AWS or GCP VM) | `VM_HOST`, `VM_USER` (`ec2-user` on AWS, `deploy` on GCP), `VM_SSH_PRIVATE_KEY`, `POSTGRES_PASSWORD` |

## Known limitations

- Transcription is a deterministic stub (`TRANSCRIBE_PROVIDER=stub`); plug a real provider into `backend/app/services/transcribe.py`.
- Free PaaS tiers have ephemeral disks: uploaded media is lost on restart. Use a volume or object storage for real use.
- VM deployments serve plain HTTP; put Caddy/Cloudflare in front for TLS.
- Cuts run in a FastAPI background task; use a worker queue for heavy load.
