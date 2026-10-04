variable "owner" {
  description = "Your handle (people/<owner>.yml). Only fleet.yml servers with this owner are managed. Set by the Taskfile from AGENTOPS_ME."
  type        = string
}

variable "ssh_allowed_cidrs" {
  description = "Who may reach port 22. Keys are the real gate; narrow this if you like."
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}

variable "image" {
  type    = string
  default = "ubuntu-24-04-x64"
}
