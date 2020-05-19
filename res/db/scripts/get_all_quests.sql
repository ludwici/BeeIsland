select q.id,
       case ?
           when 'ua' then ql.title_ua
           when 'en' then ql.title_en
           else ql.title_ru
           end as title,
       case ?
           when 'ua' then ql.desc_ua
           when 'en' then ql.desc_en
           else ql.desc_ru
           end as description,
       q.icon_x,
       q.icon_y
from quest q,
     quest_locale ql
where q.id = ql.id;