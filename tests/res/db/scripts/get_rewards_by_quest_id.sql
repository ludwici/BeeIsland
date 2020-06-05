select qr.resource_id,
       case ?
           when 'ua' then rl.name_ua
           when 'en' then rl.name_en
           else rl.name_ru
           end as name,
       qr.amount,
       qr.quest_id
from quest_rewards qr,
     resource_locale rl
where qr.resource_id = rl.id
  and quest_id = ?;