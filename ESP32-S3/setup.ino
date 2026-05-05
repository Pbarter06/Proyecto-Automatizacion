void on_setup() {

    pinMode(LED_FUNCIONAMIENTO, OUTPUT);
    pinMode(LED_PALET1_LLENO, OUTPUT);
    pinMode(LED_PALET2_LLENO, OUTPUT);

    pinMode(BUTTON_VACIAR_PALET1, INPUT_PULLUP);
    pinMode(BUTTON_VACIAR_PALET2, INPUT_PULLUP);
    pinMode(AZULEJO_BUENO, INPUT_PULLUP);
    pinMode(AZULEJO_MALO, INPUT_PULLUP);
    pinMode(AZULEJO_DEFECTUOSO, INPUT_PULLUP);

    // Estado inicial LEDs externos: apagados
    digitalWrite(LED_PALET1_LLENO, LOW);
    digitalWrite(LED_PALET2_LLENO, LOW);

    setInternalLed(0);

}

