output "redis_hostname" {
  description = "Hostname dell'istanza Azure Cache for Redis."
  value       = azurerm_redis_cache.this.hostname
}

output "redis_ssl_port" {
  description = "Porta SSL su cui e' esposta l'istanza Redis."
  value       = azurerm_redis_cache.this.ssl_port
}

output "redis_primary_access_key" {
  description = "Chiave primaria di accesso all'istanza Redis."
  value       = azurerm_redis_cache.this.primary_access_key
  sensitive   = true
}

output "postgres_fqdn" {
  description = "Hostname completo del server Azure Database for PostgreSQL."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}

output "postgres_database_name" {
  description = "Nome del database applicativo (il catalogo prodotti)."
  value       = azurerm_postgresql_flexible_server_database.catalog.name
}

output "postgres_admin_username" {
  description = "Utente amministratore del server Postgres."
  value       = var.postgres_admin_username
}
