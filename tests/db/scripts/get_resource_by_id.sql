select r.id,
       case ?
           when 'ua' then rl.name_ua
           when 'en' then rl.name_en
           else rl.name_ru
           end as name,
       case ?
           when 'ua' then rl.desc_ua
           when 'en' then rl.desc_en
           else rl.desc_ru
           end as desc,
       r.max_count
from resource r,
     resource_locale rl
where r.id = rl.id
  and r.id = ?;