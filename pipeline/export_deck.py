"""Refresh deck_data.json from content.py (keeps logo, image and other static keys)."""
import json, content as C
d = json.load(open('deck_data.json'))
d.update(main=C.DATA_EXTRA['main'], sections=C.SECTIONS, takeaways=C.TAKEAWAYS, recs=C.RECS, dq=C.DQ, sources=[list(x) for x in C.SOURCES], costar_sales='234.2M', register=__import__('ocv_content').REGISTER, recs_t=__import__('logic_content').RECS_T)
json.dump(d, open('deck_data.json', 'w'), ensure_ascii=False, default=str)
print('deck_data refreshed', len(d['sections']))
