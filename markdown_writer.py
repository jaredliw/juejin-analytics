"""Write markdown file, present data."""
from datetime import datetime

from mdutils import MdUtils

from __init__ import category_id_map
from analytics import df

file = MdUtils(file_name='README.md')

file.new_header(1, "掘金数据分析")
file.write("[![Update data](https://github.com/jaredliw/juejin-analytics/actions/workflows/update-data.yml/badge.svg)]"
           "(https://github.com/jaredliw/juejin-analytics/actions/workflows/update-data.yml)", wrap_width=0)
file.write(f"上次更新时间： {str(datetime.now())}", wrap_width=0)

file.new_header(2, "数据分析")
content = []
for key in category_id_map.keys():
    content.append(f"{key + ' ' if key[-1].isupper() or key[-1].islower() or key[-1].isdigit() else key}文章 "
                   f"{df['article_id'][df['category_id'] == category_id_map[key]].count()} 篇")
file.new_line(f"此仓库包含 **{df['article_id'].count()} 篇文章**，其中{'，'.join(content)}。", wrap_width=0)

file.new_header(3, "Top 10 热门文章")
needed_cols = ["article_id", "title", "category_id", "view_count", "collect_count", "digg_count", "comment_count",
               "score"]
header = ["文章标题", "阅读数", "评论数", "点赞数", "收藏数", "热度值"]
for key in category_id_map.keys():
    file.new_header(4, key)
    top10 = df[df["category_id"] == category_id_map[key]][needed_cols]
    top10 = top10.sort_values("score", ascending=False)[:10]
    table_content = []
    for _, cols in top10.iterrows():
        table_content.append(f"[{cols['title']}](https://juejin.cn/post/{cols['article_id']})".replace("|", r"\|"))
        table_content.append(cols["view_count"])
        table_content.append(cols["collect_count"])
        table_content.append(cols["digg_count"])
        table_content.append(cols["comment_count"])
        table_content.append(f"{cols['score']:.2f}")
    print(key)
    print(top10)
    print(header + table_content)
    print()
    file.new_table(len(header), 11, header + table_content)

file.create_md_file()
