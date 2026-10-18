'use strict';
// Preserve links to pages in the previous single-URL reader.
const legacyPage=/^#p(\d+)$/.exec(location.hash);
if(legacyPage){
  const page=Math.max(1,Math.min(16,Number(legacyPage[1])));
  location.replace('episodes/01/#p'+page);
}
