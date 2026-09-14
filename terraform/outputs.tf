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
