terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}
provider "azurerm" {
  features {}

  subscription_id = "27d13b5e-2698-472d-a869-93da20c061d5"
  tenant_id       = "bce8dd2e-d150-45ed-95fc-3ab94970431d"

}

resource "azurerm_resource_group" "rg" {
  name     = "rg-terraform-az204"
  location = "East Us"
  tags = {
    environment = "dev"
  }
}

resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = "medical-records-db-tf"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }
  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
  depends_on = [
    azurerm_resource_group.rg
  ]
}

resource "azurerm_cosmosdb_sql_database" "cosmosdb_sql" {
  name                = "lipid-profiles"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmosdb.name
  throughput          = 400
}

resource "azurerm_cosmosdb_sql_container" "cosmosdb_sql_container" {
  name                  = "Items"
  resource_group_name   = azurerm_resource_group.rg.name
  account_name          = azurerm_cosmosdb_account.cosmosdb.name
  database_name         = azurerm_cosmosdb_sql_database.cosmosdb_sql.name
  partition_key_path    = "/id"
  throughput            = 400
  partition_key_version = 1
  indexing_policy {
    indexing_mode = "consistent"
    included_path {
      path = "/*"
    }
    excluded_path {
      path = "/\"_etag\"/?"
    }
  }
}