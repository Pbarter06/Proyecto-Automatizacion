uint8_t ledStatus = 0;

void setInternalLed(uint8_t status) {
    if (ledStatus == status) {
        return;
    }

    ledStatus = status;

    // LED integrado en ESP32-S3: activo en LOW
    if (status) {
        digitalWrite(LED_FUNCIONAMIENTO, LOW);
    } else {
        digitalWrite(LED_FUNCIONAMIENTO, HIGH);
    }
}

// Función para eliminar los primeros n caracteres de una cadena
void eliminarPrimeros(char *cadena, size_t n) {
    size_t len = strlen(cadena);

    if (n >= len) {
        // Si n es mayor o igual que la longitud, la cadena queda vacía
        cadena[0] = '\0';
        return;
    }

    // Desplazar los caracteres hacia la izquierda
    memmove(cadena, cadena + n, len - n + 1); 
    // +1 para incluir el carácter nulo '\0'
}

