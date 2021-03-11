import datetime
today = datetime.date.today()
monthago= datetime.datetime.today() - datetime.timedelta(days=30)
print(today)
print(monthago)

from pytrends.request import TrendReq
from japanmap import picture
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# キーワード設定
keyword = "ヤリス"

# Google Trends(トレンド)からデータ取得
pytrends = TrendReq(hl='ja-JP', tz=-540)

kw_list = [keyword]
pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='JP', gprop='')

df = pytrends.interest_by_region(resolution='JP', inc_low_vol=True, inc_geo_code=True)
df['geoCode'] = df['geoCode'].str.replace('JP-', '').astype(int)

# データ作成
# 共通データ作成
cmap = plt.get_cmap('jet')
norm = plt.Normalize(vmin=df[keyword].min(), vmax=df[keyword].max())
# カラーバー用データを作成
mappable = cm.ScalarMappable(cmap=cmap, norm=norm)
mappable._A = []
# 日本地図用データを作成
fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

# 図を描画
# 図のベースを描く
plt.figure(figsize=(10, 8))
# 日本地図を描く
plt.imshow(picture(df[keyword].apply(fcol)));
# カラーバーを描く
plt.colorbar(mappable)

plt.savefig('{}.png'.format(keyword))
plt.show()

