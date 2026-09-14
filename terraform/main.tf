# Provisioning Azure Cache for Redis per i test di benchmark.

terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
}

# Tier Basic: nessuna alta affidabilita', la piu' economica adatta a un
# confronto di performance con/senza cache (non per produzione).
resource "azurerm_redis_cache" "this" {
  name                = var.redis_cache_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  capacity            = var.redis_capacity
  family              = "C"
  sku_name            = var.redis_sku_name
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
}
