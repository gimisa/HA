#!/bin/bash

# --- CONFIGURATION ---
# this script publish to mosquitto server on HA1 
BROKER="127.0.0.1"
USER="user"
PASS="pass"
SENSOR=$1
TOPIC="courriel/hydroquebec/${SENSOR}_filesize"

# --- LOGIQUE DE RESET ---
# Permet de remettre les compteurs à zéro via la commande : ./alerte_hq_mqtt.sh reset
if [ "$SENSOR" == "reset" ]; then
    mosquitto_pub -h $BROKER -u "$USER" -P "$PASS" -t "courriel/hydroquebec/hq06_filesize" -m "0" -r
    mosquitto_pub -h $BROKER -u "$USER" -P "$PASS" -t "courriel/hydroquebec/hq16_filesize" -m "0" -r
    mosquitto_pub -h $BROKER -u "$USER" -P "$PASS" -t "courriel/hydroquebec/hq26_filesize" -m "0" -r
    echo "Tous les senseurs ont été remis à 0."
    exit 0
fi

# --- LOGIQUE D'INCRÉMENTATION (+1) ---
# On récupère la valeur actuelle pour ajouter 1, ce qui force le trigger dans HA
CURRENT_VAL=$(mosquitto_sub -h $BROKER -u "$USER" -P "$PASS" -t "$TOPIC" -C 1 -W 1 2>/dev/null)

if [[ ! "$CURRENT_VAL" =~ ^[0-9]+$ ]]; then
    CURRENT_VAL=0
fi

NEW_VAL=$((CURRENT_VAL + 1))

# Publication MQTT avec le flag RETAIN pour la résilience
mosquitto_pub -h $BROKER -u "$USER" -P "$PASS" -t "$TOPIC" -m "$NEW_VAL" -r

# --- AFFICHAGE DE STATUT ---
echo ">>> TRANSMISSION MQTT : $SENSOR"

if [ "$SENSOR" == "hq06" ]; then
    echo "Envoi alerte MATIN vers HA..."
elif [ "$SENSOR" == "hq16" ]; then
    echo "Envoi alerte SOIR vers HA..."
elif [ "$SENSOR" == "hq26" ]; then
    echo "Envoi alerte DOUBLE vers HA..."
fi
