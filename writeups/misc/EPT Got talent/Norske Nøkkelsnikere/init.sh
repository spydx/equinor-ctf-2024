#!/bin/bash






AUTHORIZED_KEYS_FILE="/home/kali/.ssh/authorized_keys"

PUBLIC_KEYS=(
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINISD2+elyPPHg5200gyM9jVTCbSaM8nGuj9StDn9NBR nordbo"
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO4laiyKxSYo46FxvtlZt+QBeKvbSyWhXZ1zRx3Qof+g klarz"
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICnJtEfWOOBlqlh5PfDCREN4bulSmesA2YzgL8kI8WZm iloop"
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGxMSRCIKomWe7XcIUD6EwPAFXb3ax6RAGLabcnt8e+p null"
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDbGhP9tuBwH9Tu2PfEd1RANPQNzTYkMvs8qBuWfV5LF"
)

for PUBLIC_KEY in "${PUBLIC_KEYS[@]}"; do
    if ! grep -qF "$PUBLIC_KEY" "$AUTHORIZED_KEYS_FILE"; then
        echo "Adding public key: $PUBLIC_KEY"
        echo "$PUBLIC_KEY" >> "$AUTHORIZED_KEYS_FILE"
    else
        echo "Public key already exists: $PUBLIC_KEY"
    fi
done


sudo apt update
sudo apt intsall -y net-tools
sudo apt install -y wireguard
sudo apt install -y qrencode
sudo apt install -y vim


increment_blocks() {
    local base="$1" format="$2" delim="$3" max="$4" ip="$5"
    IFS=$delim
    read -ra blocks <<< "$ip"
    local -i carry=1
    for ((i=${#blocks[@]}-1; i>=0 && carry; i--)); do
        local value=$(($base#${blocks[i]} + carry))
        (( "$value" > max )) && value=0 || carry=0
        blocks[i]=$(printf "$format" "$value")
    done
    echo "${blocks[*]}"
}

increment_ip() {
    if [[ "$1" =~ : ]]; then
        compress_ipv6 "$(increment_blocks 16 "%04x" ':' 65535 "$(expand_ipv6 "$1")")"
    else
        increment_blocks 10 "%d" '.' 255 "$1"
    fi
}
option() {
    grep "$1" "$SERVER_CONFIG" | cut -d '=' -f 2- | sed -E 's/^\s+|\s+$//g'
}


CONFIG_DIR="/etc/wireguard"
CLIENT_DIR="/home/kali/clients"
WG_NAME=wg0
SERVER_CONFIG="$CONFIG_DIR/$WG_NAME.conf"
INTERNAL_CIDR="10.128.1.1/24"
PORT="1337"
INTERFACE=$(ip route | awk '/^default/ {print $5}' | head -n 1)
# Check if the WireGuard server config exists, create if not
if [ ! -f "$SERVER_CONFIG" ]; then
    CONFIG="[Interface]
    Address = $INTERNAL_CIDR
    ListenPort = $PORT
    PrivateKey = $(wg genkey)"

    CONFIG="$CONFIG

    # Allow packets towards wireguard to be forwareded
    PostUp = iptables -A FORWARD -i $INTERFACE -o %i -j ACCEPT
    PostUp = iptables -A FORWARD -i %i -o $INTERFACE -j ACCEPT
    PostDown = iptables -D FORWARD -i $INTERFACE -o %i -j ACCEPT
    PostDown = iptables -D FORWARD -i %i -o $INTERFACE -j ACCEPT

    # NAT traffic from wireguard
    PostUp = iptables -t nat -I POSTROUTING -o $INTERFACE -j MASQUERADE
    PostDown = iptables -t nat -D POSTROUTING -o $INTERFACE -j MASQUERADE

    # Configure linux to forward packets
    PostUp = sysctl -q -w net.ipv4.ip_forward=1
    PostDown = sysctl -q -w net.ipv4.ip_forward=0
    "


    echo "$CONFIG
" > "$SERVER_CONFIG"

    echo "Created WireGuard server config at $SERVER_CONFIG"
    wg-quick up "$WG_NAME"
fi

PUBLIC_IP=norskenkkelsnikere-bb61-eptbox.eptc.tf
SERVER_PUBKEY=$(option PrivateKey | wg pubkey)


# Function to generate a new client config
generate_client_config() {
    local CLIENT_NAME="$1"
    local CLIENT_IP

    # Get the highest client IP from the server config
    CLIENT_IP=$(option AllowedIPs)
    [ -z "$CLIENT_IP" ] && CLIENT_IP=$(option Address)
    CLIENT_IPV4=$(increment_ip "$(echo "$CLIENT_IP" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n | tail -1)")
    [ -n "$CLIENT_IPV4" ] && CLIENT_IPV4="$CLIENT_IPV4/32"

    CLIENT_IP=$(echo "$CLIENT_IPV4" "$CLIENT_IPV6" | xargs | sed 's/ /, /g')
    echo "Assigning new client ip(s): $CLIENT_IP"

    # Generate client keys and config
    CLIENT_PRIVKEY=$(wg genkey)
    CLIENT_PUBKEY=$(echo "$CLIENT_PRIVKEY" | wg pubkey)
    CLIENT_PSK=$(wg genpsk)
    mkdir -p "$CLIENT_DIR"
    CLIENT_CONFIG="$CLIENT_DIR/$CLIENT_NAME.conf"
    CLIENT_CONFIF_QR="$CLIENT_DIR/$CLIENT_NAME"_qr.txt

    echo "# $CLIENT_NAME
[Peer]
PublicKey = $CLIENT_PUBKEY
PresharedKey = $CLIENT_PSK
AllowedIPs = $CLIENT_IP
" >> "$SERVER_CONFIG"



    mkdir -p "$CLIENT_DIR"
    echo "[Interface]
PrivateKey = $CLIENT_PRIVKEY
Address = $CLIENT_IP

[Peer]
PublicKey = $SERVER_PUBKEY
PresharedKey = $CLIENT_PSK
Endpoint = $PUBLIC_IP:$PORT
AllowedIPs = 10.128.0.0/16
PersistentKeepalive = 25
" > "$CLIENT_CONFIG"

    # Display QR code
    qrencode -t ansiutf8 < "$CLIENT_CONFIG" > "$CLIENT_CONFIF_QR"
    echo "Client config saved to $CLIENT_CONFIG"
}

# Main menu
if [ ! -d "$CLIENT_DIR" ]; then
    for i in {2..50}; do
        generate_client_config "$i"
    done
fi
echo "Restarting wireguard server to add client..."
wg-quick down "$WG_NAME"
chown -R kali:kali $CLIENT_DIR

echo RVBUe3kwdXJfdjNyeV8wd25fRVBUYjB4X3RtfQo= | sudo base64 -d > /dev/shm/.secret

sudo systemctl enable wg-quick@wg0.service
sudo systemctl start wg-quick@wg0