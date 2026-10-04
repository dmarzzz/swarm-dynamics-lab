# =============================================================================
# One root module for everyone. fleet.yml, blueprints.yml and people/ are the
# inputs; each owner applies only their own DigitalOcean servers, with their own
# token and their own local state (workspace = handle, see Taskfile `up`).
#
# Every droplet gets:
#   - a dedicated ed25519 key for root (break-glass, owner only), written to
#     ~/.ssh/<name>_ed25519 on the owner's machine
#   - cloud-init that creates one account per person with access, holding the
#     keys from their people/<handle>.yml, so everyone can ssh in at first boot
#   - a cloud firewall: SSH + the server's `ports`, outbound open
#   - its address in generated/<owner>.json, which the owner commits so the
#     shared Ansible inventory and ssh-config pick it up
#
# After first boot, access changes go through Ansible (`task access`), not here:
# user_data is ignored after create so editing people/ never rebuilds a droplet.
# =============================================================================

locals {
  repo_root  = abspath("${path.root}/..")
  fleet      = try(yamldecode(file("${local.repo_root}/fleet.yml")).servers, {})
  blueprints = yamldecode(file("${local.repo_root}/blueprints.yml")).blueprints

  people = {
    for f in fileset("${local.repo_root}/people", "*.yml") :
    trimsuffix(f, ".yml") => yamldecode(file("${local.repo_root}/people/${f}"))
    if !startswith(f, "_")
  }
  active = [for h, p in local.people : h if try(p.active, true)]

  # Handles that are also stock Ubuntu group names (e.g. `shadow`). useradd refuses to
  # create the user's own group over one of these, so such users get `swarm` as primary.
  system_groups = ["root", "daemon", "bin", "sys", "adm", "tty", "disk", "lp", "mail", "news", "uucp",
    "man", "proxy", "kmem", "dialout", "fax", "voice", "cdrom", "floppy", "tape", "sudo", "audio", "dip",
    "www-data", "backup", "operator", "list", "irc", "src", "shadow", "utmp", "video", "sasl", "plugdev",
  "staff", "games", "users", "nogroup", "systemd-journal", "netdev", "lxd", "docker", "admin", "syslog"]

  servers = {
    for name, s in local.fleet : name => s
    if try(s.owner, "") == var.owner && try(s.provider, "") == "digitalocean"
  }

  access = {
    for name, s in local.servers : name => [
      for h in distinct(concat(
        try(s.access, "all") == "all" ? local.active : tolist(s.access),
        [s.owner],
      )) : h if contains(local.active, h)
    ]
  }
}

resource "tls_private_key" "root" {
  for_each  = local.servers
  algorithm = "ED25519"
}

resource "digitalocean_ssh_key" "root" {
  for_each   = local.servers
  name       = "agentops/${each.key}"
  public_key = tls_private_key.root[each.key].public_key_openssh
}

resource "local_sensitive_file" "root_key" {
  for_each        = local.servers
  filename        = pathexpand("~/.ssh/${each.key}_ed25519")
  content         = tls_private_key.root[each.key].private_key_openssh
  file_permission = "0600"
}

resource "digitalocean_droplet" "this" {
  for_each   = local.servers
  name       = each.key
  image      = var.image
  region     = try(each.value.region, "nyc3")
  size       = try(each.value.size, local.blueprints[each.value.blueprint].size)
  ipv6       = true
  monitoring = true
  backups    = try(each.value.backups, false) # weekly DO droplet backups (+20% of the droplet price)
  ssh_keys   = [digitalocean_ssh_key.root[each.key].id]
  tags       = ["agentops", "owner-${var.owner}", "bp-${each.value.blueprint}"]

  user_data = "#cloud-config\n${yamlencode({
    groups = ["swarm"]
    # "default" keeps DO's root-key handling; then one account per person.
    users = concat(["default"], [
      for h in local.access[each.key] : merge({
        name                = h
        shell               = "/bin/bash"
        groups              = "sudo, swarm"
        sudo                = "ALL=(ALL) NOPASSWD:ALL"
        lock_passwd         = true
        ssh_authorized_keys = local.people[h].ssh_keys
      }, contains(local.system_groups, h) ? { primary_group = "swarm", no_user_group = true } : {})
    ])
  })}"

  lifecycle {
    ignore_changes = [image, user_data]
  }
}

resource "digitalocean_firewall" "this" {
  for_each    = local.servers
  name        = "swarm-${each.key}"
  droplet_ids = [digitalocean_droplet.this[each.key].id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = tostring(try(each.value.ssh_port, 22))
    source_addresses = var.ssh_allowed_cidrs
  }

  dynamic "inbound_rule" {
    for_each = toset([for p in concat(try(each.value.ports, []), try(local.blueprints[each.value.blueprint].ports, [])) : tostring(p)])
    content {
      protocol         = "tcp"
      port_range       = inbound_rule.value
      source_addresses = ["0.0.0.0/0", "::/0"]
    }
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

resource "local_file" "generated" {
  filename = "${local.repo_root}/generated/${var.owner}.json"
  content = jsonencode({
    for name, d in digitalocean_droplet.this : name => {
      ipv4   = d.ipv4_address
      ipv6   = d.ipv6_address
      region = d.region
      size   = d.size
      id     = d.id
    } if contains(keys(local.servers), name)
  })
}
