import os
import requests
import json
import time
import uuid

print("Options:")
print("1. Save tokens to a file")
print("2. Send tokens to a webhook")
option = input("Choose an option (1 or 2): ")

def send_discord_webhook(token):
    discord_msg_link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
    image_url = "https://cdn.discordapp.com/attachments/1187112012203966556/1187112851761025185/file-AvjLiO9yZwHmHGpTLF9IVvJ8.png?ex=6595b3ff&is=65833eff&hm=b7f97dba58d823a6f0e93c84461b66aec770500e45f8a7c2c749ae35bb6ac11b&"
    webhook_url = "Your_Webhook_Url"
    payload = {
        "embeds": [
            {
                "title": "Discord Nitro Promo",
                "description": f"[Click Here for Link]({discord_msg_link})\n```{discord_msg_link}```\nRemember you need to not have used a promo for 12 months to use this",
                "color": 0x3498db,
                "thumbnail": {"url": image_url}
            }
        ]
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    if response.status_code != 204:
        print(f"Error sending webhook: {response.status_code}")
        print(response.text)


def save_to_file(token):
    filename = "config/tokens.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a") as file:
        file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")

while True:
    random_partner_user_id = str(uuid.uuid4())
    url = "https://api.discord.gx.games/v1/direct-fulfillment"
    payload = {"partnerUserId": random_partner_user_id}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json().get("token")

        if option == "1":
            save_to_file(token)
            print(f"Token saved to 'config/tokens.txt' as a link")

        elif option == "2":
            send_discord_webhook(token)
            print(f"Token sent to Discord webhook")

        else:
            print("Invalid option. Please choose 1 or 2.")

    elif response.status_code == 429:
        print("Rate limit exceeded")
        time.sleep(10)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
