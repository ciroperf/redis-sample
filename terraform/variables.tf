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
