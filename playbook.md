# Laowai reels playbook (living doc - every daily run reads this first)

Edit this file to change strategy; the scheduled task prompt stays stable.

## Goal now
Build the brand + a general community of foreigners in China. Entertain first, product second. Learn from Metricool stats, build up from what works.

## Laowai angle (the tie-back line)
Do NOT default to "group-chat chaos". Rotate and stretch. Pick a DIFFERENT angle than the last 5 reels (see topics.md). Even far-fetched links are welcome if the line is clever and honest.
Angle bank (extend freely):
- "everyone has been the confused laowai" (shared experience)
- wordplay: laowai ma? / "laowai, right?" / 吗 as the question that opens every conversation
- trust & verification (passport-checked profiles, blind ratings) when topic is about scams/trust
- "learn it the hard way vs find it on laowai"
- being seen / being booked: visibility, first impressions, profile = your first meeting
- paperwork & process: who handles the boring part so you do not have to
- locals-and-foreigners bridge: two sides, one conversation
- time zones / distance: people planning China from abroad
- side-hustle / gig life: second income, flexibility
- humor: the brand as the friend who already knows the answer
- culture-swap curiosity: what locals wonder about us vs what we wonder about them
Log the angle used in topics.md so stats can be compared.

## Experiment tagging (required, in topics.md each row)
date | reel# | pillar | topic | angle | hook type | style | voice/captions-only | humor level (0-2) | length | sources

## Humor rules
~1 in 4 reels humor-led, never two in a row, punch at situations and at ourselves, never at people/groups, original art only.

## Inspiration rules
Only save notes (technique, hook, timing, why it works) from reels that meet the bar: strong craft, fresh animation style, or genuinely useful info on social media / content creation / tools. No downloading or re-posting others' content. See inspiration/ folder.

## Performance feedback
performance.md is updated weekly from Metricool. Lean into formats/hooks/angles that win on saves, shares, watch time; retire what flops after 2+ tries.

## Metricool call shape (verified 2026-10-29; overrides the older description in the task prompt)
createScheduledPost takes: blogId (number 7716477), date ("2026-10-29T20:30:00+08:00" - must include the UTC offset), info (object) containing:
text, publicationDate {dateTime:"2026-10-29T20:30:00", timezone:"Asia/Shanghai"}, providers [{network:"instagram"}] or [{network:"tiktok"}], media [raw.githubusercontent URL], autoPublish true,
videoThumbnailUrl (IG reel cover), instagramData {type:"REEL", showReelOnFeed:true, isAiGenerated:false} or {type:"STORY"} (story: media = cover.png, text ""), tiktokData {privacyOption:"PUBLIC_TO_EVERYONE", title, isAigc:false}.
getScheduledPosts takes brandId, fromDate, toDate (ISO with offset, e.g. 2026-10-29T00:00:00+08:00), timezone.
Note: raw.githubusercontent URLs: check with curl -s -o /dev/null -w "%{http_code}" (plain -sI shows the proxy line, not the real status).
Extra reels the owner adds use folder YYYY-MM-DD-b. Reel 2 ("The Nod") is scheduled 2026-10-29 14:30 CST, story 15:30; daily run slot stays 20:30.
## Known toolkit gotcha
paste_scaled used to mutate cached layers when alpha<1 (fixed in toolkit/reel_lib.py): always use the copy-on-alpha version.
Toolkit run: copy toolkit/*.py to /home/claude/reels/, fonts via npm @fontsource (Instrument Serif italic file is instrument-serif-latin-400-italic), see reel_02_the_nod.py for the mascot + layout helpers (rich(), card(), halftone()).
