terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.7.0"
}

provider "aws" {
  region = "us-west-2"
  profile = "so"
}

resource "aws_dynamodb_table" "tg-messages-table" {
  name           = "TgMessages"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20

  hash_key       = "UserId"
  range_key      = "UserMessageKey"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "UserMessageKey"
    type = "S"
  }

#   attribute {
#     name = "UserMessageValue"
#     type = "S"
#   }
}