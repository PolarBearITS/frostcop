from monitors import discord_utils
url = 'https://discordapp.com/api/webhooks/435954570292756480/fLbreq3dFc_afDOZqtXYnDWDcgpc0mF-RKtUF55vXLKOej4sXCaHJx2Ac7IyzHVpw0hM'
d = discord_utils.Webhook(url, content='asdf')
d.post()