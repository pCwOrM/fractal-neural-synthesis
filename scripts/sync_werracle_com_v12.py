import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("185.27.133.12", port=1394, username="itouchsy", password="2HRaBof_pHdi{E}S", timeout=15)

sftp = client.open_sftp()
print("Files in /home/itouchsy/werracle.com:", sftp.listdir("/home/itouchsy/werracle.com"))

with sftp.file("/home/itouchsy/werracle.com/index.html", "r") as f:
    content = f.read().decode("utf-8")

old_en = '<div class="row"><div class="k">98.1%<small data-i18n="r7u">recaptured</small></div><div class="v" data-i18n-html="r7">Chainlink SVR empirical value recapture on Base: <b>$186.9k</b> of <b>$190.5k</b> gross collateral recaptured for depositors across 105 multi-call audited liquidations. Median solver margin compressed to <b>-1.55%</b>.</div><a class="verify" href="https://radar.werracle.com" target="_blank" rel="noopener" data-i18n="vr7">Open the radar</a></div>'
new_en = '<div class="row"><div class="k">94.4%<small data-i18n="r7u">recaptured</small></div><div class="v" data-i18n-html="r7">Chainlink SVR empirical value recapture on Base (v1.2): <b>$179.8k</b> of <b>$190.5k</b> gross liquidation incentive recaptured for protocols (<b>98.3%</b> median tx recapture across 105 multi-call tx / 513 liquidations). Median solver margin compressed to <b>+1.26%</b>.</div><a class="verify" href="https://radar.werracle.com" target="_blank" rel="noopener" data-i18n="vr7">Open the radar</a></div>'

old_tr = 'r7u:"geri kazanım", r7:"Base ağında Chainlink SVR ampirik değer geri kazanımı: 105 çoklu çağrılı denetlenmiş tasfiyede <b>190,5 bin $</b> brüt teminatın <b>186,9 bin $\'ı</b> mevduat sahiplerine geri kazandırıldı. Medyan solver marjı <b>-%1,55</b> seviyesine sıkıştı.", vr7:"Radarı açın",'
new_tr = 'r7u:"geri kazanım", r7:"Base ağında Chainlink SVR ampirik değer geri kazanımı (v1.2): 105 çoklu çağrılı işlemde (513 tasfiye) <b>190,5 bin $</b> brüt teşvikin <b>179,8 bin $\'ı</b> protokollere geri kazandırıldı (medyan işlem geri kazanımı <b>%98,3</b>). Medyan solver marjı <b>+%1,26</b> seviyesine sıkıştı.", vr7:"Radarı açın",'

if old_en in content:
    content = content.replace(old_en, new_en, 1)
    print("Updated EN SVR row on werracle.com!")
else:
    print("old_en not found")

if old_tr in content:
    content = content.replace(old_tr, new_tr, 1)
    print("Updated TR SVR row on werracle.com!")
else:
    print("old_tr not found")

with sftp.file("/home/itouchsy/werracle.com/index.html", "w") as f:
    f.write(content.encode("utf-8"))

robots_txt = """User-agent: *
Allow: /

Sitemap: https://werracle.com/sitemap.xml
"""
sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://werracle.com/</loc>
    <lastmod>2026-10-26</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
with sftp.file("/home/itouchsy/werracle.com/robots.txt", "w") as f:
    f.write(robots_txt.encode("utf-8"))
with sftp.file("/home/itouchsy/werracle.com/sitemap.xml", "w") as f:
    f.write(sitemap_xml.encode("utf-8"))
print("Updated robots.txt and sitemap.xml on werracle.com!")

# Also check if werr.io is on the same server!
try:
    print("Checking /home/itouchsy/werr.io:", sftp.listdir("/home/itouchsy/werr.io"))
except Exception as e:
    print("werr.io dir check:", e)

sftp.close()
client.close()
