# Provisioning di Azure Database for PostgreSQL: la sorgente dati "vera"
# che le API mettono in cache (vedi app/db.py e db/seed.sql).

# Tier Burstable B1ms: il piano base piu' economico, adatto a un confronto
# di performance con/senza cache (non per produzione).
resource "azurerm_postgresql_flexible_server" "this" {
  name                = var.postgres_server_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  version    = "16"
  sku_name   = var.postgres_sku_name
  storage_mb = 32768

  administrator_login    = var.postgres_admin_username
  administrator_password = var.postgres_admin_password

  # Nessuna alta affidabilita': coerente con lo scopo demo di questo repo.
  zone = "1"
}

resource "azurerm_postgresql_flexible_server_database" "catalog" {
  name      = var.postgres_database_name
  server_id = azurerm_postgresql_flexible_server.this.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Consente alle risorse Azure (incluso l'API se deployata su Azure) di
# raggiungere il server. Per connettersi da locale va aperta anche la
# propria IP pubblica in azurerm_postgresql_flexible_server_firewall_rule.
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.this.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
