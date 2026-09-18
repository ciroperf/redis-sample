variable "location" {
  description = "Regione Azure dove creare le risorse."
  type        = string
  default     = "westeurope"
}

variable "resource_group_name" {
  description = "Nome del resource group che contiene l'Azure Cache for Redis."
  type        = string
  default     = "rg-redis-sample"
}

variable "redis_cache_name" {
  description = "Nome dell'istanza Azure Cache for Redis (deve essere globalmente univoco)."
  type        = string
  default     = "redis-sample-cache"
}

variable "redis_sku_name" {
  description = "SKU dell'Azure Cache for Redis. Basic e' la piu' economica, senza SLA di alta affidabilita'."
  type        = string
  default     = "Basic"
}

variable "redis_capacity" {
  description = "Dimensione della cache (0-6 per lo SKU Basic: 0 = C0, la piu' piccola)."
  type        = number
  default     = 0
}

variable "postgres_server_name" {
  description = "Nome del server Azure Database for PostgreSQL (deve essere globalmente univoco)."
  type        = string
  default     = "redis-sample-db"
}

variable "postgres_sku_name" {
  description = "SKU del server Postgres. B_Standard_B1ms e' il piano Burstable piu' economico."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgres_database_name" {
  description = "Nome del database applicativo (il catalogo prodotti)."
  type        = string
  default     = "catalog"
}

variable "postgres_admin_username" {
  description = "Utente amministratore del server Postgres."
  type        = string
  default     = "redisample_admin"
}

variable "postgres_admin_password" {
  description = "Password dell'amministratore Postgres. Nessun default: va passata via TF_VAR_postgres_admin_password, mai hardcoded."
  type        = string
  sensitive   = true
}
