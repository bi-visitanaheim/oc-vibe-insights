/* Focused deck (Oct. 14, 2026): questions answered for Anaheim, Orange County and the U.S. */
pres.title = 'OC Vibe Insights: Questions answered';
pres.addSection({ title: 'Introduction' });
let s = pres.addSlide({ masterName: 'VA Title', sectionTitle: 'Introduction' });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 0.7, w: 3.0, h: 3.0 / LOGO_AR + 0.3, fill: { color: H.light }, line: { color: H.light }, rectRadius: 0.1, objectName: 'logo-plate' });
s.addImage({ data: LOGO, x: M + 0.15, y: 0.85, w: 2.7, h: 2.7 / LOGO_AR, altText: 'Visit Anaheim' });
s.addText('Questions answered: Anaheim, Orange County and U.S.', { placeholder: 'title' });
s.addText('Average spend, one more night, transportation impact and District 5, each with a short answer, a visual, the method and the reports behind it. Data through September 2026.', { placeholder: 'sub' });
s.addText('Prepared by Visit Anaheim Business Intelligence · October 2026 · Companion to the OC Vibe Insights app and report', ft({ x: M, y: 6.6, w: 11, h: 0.4, fontSize: 12, color: H.white }));
qaCoreSlide('Introduction');
qaIndexSlide('Introduction');
pres.addSection({ title: 'The four core questions' });
AQ.core.forEach(id => { qaSlide('The four core questions', QS[id]); qaDetailSlide('The four core questions', QS[id]); });
pres.addSection({ title: 'More questions answered' });
AQ.order.forEach(t => AQ.items.filter(q => q.topic === t && !AQ.core.includes(q.id) && q.id !== 'reports' && q.id !== 'updates').forEach(q => qaSlide('More questions answered', q)));
pres.addSection({ title: 'Sources and files' });
s = content('Sources and files', 'About the data', 'Limits and differences between sources to keep in mind', '');
bullets(s, D.dq.slice(-3).concat(['Tourism Economics counts a visitor as anyone who stays overnight or travels more than 50 miles; each region is modeled on its own, so city and county totals do not add.',
  'Location data (Azira, Datafy) and card data (Visa) describe visitor mix and rank markets; they are not visitor counts. Compare within each source.',
  'One-more-night values are scenarios that hold spending per day constant; they are not forecasts.']), M, 1.6, W - 2 * M, 4.8, 12);
source(s, 'Visit Anaheim Business Intelligence (Oct. 14, 2026).');
libSlides('Sources and files');
(async () => {
  await pres.writeFile({ fileName: 'OC_Vibe_Questions_Answered.pptx', compression: true });
  await applyTheme('OC_Vibe_Questions_Answered.pptx', THEME);
  console.log('written questions deck');
})();
