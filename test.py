from spider import *

print(category_id_map)
print(tag_id_map)
gen = fetch_by_category("后端", "Python")
for item in gen:
    print(item)
    input("next?")
