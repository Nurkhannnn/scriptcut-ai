terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_project_service" "compute" {
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_compute_network" "vpc" {
  name                    = "scriptcut-vpc"
  auto_create_subnetworks = true
  depends_on              = [google_project_service.compute]
}

resource "google_compute_firewall" "web" {
  name          = "scriptcut-allow-web"
  network       = google_compute_network.vpc.name
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["scriptcut"]
  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
}

resource "google_compute_firewall" "ssh" {
  name          = "scriptcut-allow-ssh"
  network       = google_compute_network.vpc.name
  source_ranges = var.ssh_source_ranges
  target_tags   = ["scriptcut"]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_compute_instance" "app" {
  name         = "scriptcut-vm"
  machine_type = "e2-micro" # Always Free eligible in us-west1 / us-central1 / us-east1
  zone         = var.zone
  tags         = ["scriptcut"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 30            # free tier: 30 GB standard persistent disk
      type  = "pd-standard" # NOT pd-balanced/pd-ssd (billed)
    }
  }

  network_interface {
    network = google_compute_network.vpc.id
    access_config {}
  }

  metadata = {
    ssh-keys       = "${var.ssh_user}:${var.ssh_public_key}"
    startup-script = file("${path.module}/startup.sh")
  }

  allow_stopping_for_update = true
  depends_on                = [google_project_service.compute]
}

# Optional budget alert so the credit cannot be burned silently
resource "google_billing_budget" "guard" {
  count           = var.billing_account == "" ? 0 : 1
  billing_account = var.billing_account
  display_name    = "scriptcut-budget"
  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.budget_usd)
    }
  }
  threshold_rules {
    threshold_percent = 0.5
  }
  threshold_rules {
    threshold_percent = 0.9
  }
}
