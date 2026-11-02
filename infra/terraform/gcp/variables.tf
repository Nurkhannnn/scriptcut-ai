variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type    = string
  default = "us-central1" # e2-micro free tier: us-west1 / us-central1 / us-east1
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "ssh_user" {
  type    = string
  default = "deploy"
}

variable "ssh_public_key" {
  type        = string
  description = "Public key used by CI to deploy"
}

variable "ssh_source_ranges" {
  type        = list(string)
  default     = ["0.0.0.0/0"] # GitHub-hosted runners have no fixed range; restrict if deploying manually
  description = "CIDRs allowed to SSH"
}

variable "billing_account" {
  type        = string
  default     = ""
  description = "Billing account ID for the optional budget alert (empty = skip)"
}

variable "budget_usd" {
  type    = number
  default = 10
}
