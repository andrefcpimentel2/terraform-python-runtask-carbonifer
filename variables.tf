
locals {
  # Common tags to be assigned to all resources
  common_tags = {
    Name      = var.name
    owner     = var.owner
    terraform = true
    purpose   = var.purpose
  }
}

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "eu-west-2"
}

variable "owner" {
  description = <<EOH
owner to be added to the default tags
EOH
default = "andre"
}

variable "purpose" {
  description = <<EOH
purpose to be added to the default tags
EOH
default = "carbon footprint calculator"
}

variable "name" {
  description = <<EOH
Name to be added to the default tags
EOH
default = "carbonifer_lambda"
}