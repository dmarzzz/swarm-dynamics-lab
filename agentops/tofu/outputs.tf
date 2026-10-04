output "servers" {
  value = {
    for name, d in digitalocean_droplet.this : name => {
      ip       = d.ipv4_address
      access   = local.access[name]
      root_key = "~/.ssh/${name}_ed25519"
    } if contains(keys(local.access), name)
  }
}
