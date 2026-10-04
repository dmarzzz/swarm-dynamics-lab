terraform {
  required_version = ">= 1.6"
  required_providers {
    digitalocean = { source = "digitalocean/digitalocean", version = "~> 2.40" }
    tls          = { source = "hashicorp/tls", version = "~> 4.0" }
    local        = { source = "hashicorp/local", version = "~> 2.5" }
  }
}

# Token from DIGITALOCEAN_TOKEN (.env). Each owner uses their own account.
provider "digitalocean" {}
