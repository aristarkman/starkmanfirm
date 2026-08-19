
const NAP = {
  ch: {city:"Cherry Hill", street:"1939 Marlton Pike East, Suite 210", cityline:"Cherry Hill, NJ 08003", tel:"856-424-7277", tel_e:"+18564247277", hours:"Mon–Fri 8:30 am – 5:00 pm", hours_es:"Lun–Vie 8:30 am – 5:00 pm", map:"1939+Marlton+Pike+East+Suite+210,+Cherry+Hill,+NJ+08003"},
  pa: {city:"Perth Amboy", street:"188 Market Street", cityline:"Perth Amboy, NJ 08861", tel:"732-324-2011", tel_e:"+17323242011", hours:"Mon–Fri 9:00 am – 6:00 pm", hours_es:"Lun–Vie 9:00 am – 6:00 pm", map:"188+Market+Street,+Perth+Amboy,+NJ+08861"}
};
const SITE = "https://www.starkmanfirm.com/";
function up(dir){ return dir === "" ? "" : "../".repeat(dir.split("/").filter(Boolean).length); }
function firmGraph(){ return [
{"@type":"LegalService","@id":SITE+"#firm","name":"Starkman Firm","alternateName":["Morris Starkman Law Firm","Starkman Law Firm"],"description":"Personal injury and workers' compensation lawyers serving Cherry Hill, Perth Amboy and all of New Jersey since 1973.","url":SITE,"email":"info@starkmanfirm.com","foundingDate":"1973","knowsLanguage":["en","es"],"areaServed":[{"@type":"State","name":"New Jersey"},{"@type":"City","name":"Cherry Hill"},{"@type":"City","name":"Perth Amboy"},{"@type":"AdministrativeArea","name":"Camden County"},{"@type":"AdministrativeArea","name":"Middlesex County"}],"department":[{"@id":SITE+"cherry-hill-nj/#office"},{"@id":SITE+"perth-amboy-nj/#office"}],"sameAs":["https://maps.app.goo.gl/1fMFFd2nbVpsKjRs8","https://maps.app.goo.gl/VLX8kkEYzsD1N7sQ8"],"founder":{"@id":SITE+"attorneys/#morris"}},
{"@type":"Attorney","@id":SITE+"cherry-hill-nj/#office","name":"Starkman Firm — Cherry Hill","parentOrganization":{"@id":SITE+"#firm"},"telephone":"+1-856-424-7277","email":"info@starkmanfirm.com","url":SITE+"cherry-hill-nj/","hasMap":"https://maps.app.goo.gl/1fMFFd2nbVpsKjRs8","sameAs":["https://maps.app.goo.gl/1fMFFd2nbVpsKjRs8"],"address":{"@type":"PostalAddress","streetAddress":"1939 Marlton Pike East, Suite 210","addressLocality":"Cherry Hill","addressRegion":"NJ","postalCode":"08003","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":39.9068,"longitude":-74.9946},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:30","closes":"17:00"}],"knowsLanguage":["en","es"]},
{"@type":"Attorney","@id":SITE+"perth-amboy-nj/#office","name":"Starkman Firm — Perth Amboy","parentOrganization":{"@id":SITE+"#firm"},"telephone":"+1-732-324-2011","email":"info@starkmanfirm.com","url":SITE+"perth-amboy-nj/","hasMap":"https://maps.app.goo.gl/VLX8kkEYzsD1N7sQ8","sameAs":["https://maps.app.goo.gl/VLX8kkEYzsD1N7sQ8"],"address":{"@type":"PostalAddress","streetAddress":"188 Market Street","addressLocality":"Perth Amboy","addressRegion":"NJ","postalCode":"08861","addressCountry":"US"},"geo":{"@type":"GeoCoordinates","latitude":40.5068,"longitude":-74.2654},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"}],"knowsLanguage":["en","es"]},
{"@type":"Person","@id":SITE+"attorneys/#morris","name":"Morris Starkman","jobTitle":"Founding Attorney","url":SITE+"attorneys/","worksFor":{"@id":SITE+"#firm"},"alumniOf":[{"@type":"CollegeOrUniversity","name":"Rutgers College"},{"@type":"CollegeOrUniversity","name":"Rutgers Law School"}],"knowsAbout":["Personal injury law","Workers' compensation","Municipal court","Real estate closings","Business law"],"description":"Practicing law in Cherry Hill, New Jersey since 1972; founded Starkman Law Firm in 1973."}
]; }
function breadcrumbLD(trail){ return {"@type":"BreadcrumbList","itemListElement":trail.map((t,i)=>({"@type":"ListItem","position":i+1,"name":t[0],"item":SITE+t[1]}))}; }
function faqLD(faqs){ return {"@type":"FAQPage","mainEntity":faqs.map(([q,a])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}))}; }

function head(o){
  const u = up(o.dir), canonical = SITE + o.dir, esDir = o.esDir, enDir = o.enDir;
  const alt = (esDir!=null && enDir!=null) ? `<link rel="alternate" hreflang="en-us" href="${SITE+enDir}"><link rel="alternate" hreflang="es-us" href="${SITE+esDir}"><link rel="alternate" hreflang="x-default" href="${SITE+enDir}">` : "";
  const graph = firmGraph().concat(o.extraLD||[]);
  return `<!DOCTYPE html><html lang="${o.lang||'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${o.title}</title><meta name="description" content="${o.desc}"><link rel="canonical" href="${canonical}">${alt}
<meta property="og:type" content="website"><meta property="og:title" content="${o.title}"><meta property="og:description" content="${o.desc}"><meta property="og:url" content="${canonical}"><meta property="og:locale" content="${(o.lang||'en')==='es'?'es_US':'en_US'}">
<meta property="og:image" content="https://www.starkmanfirm.com/assets/og-cover.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="${(o.lang||'en')==='es'?'Los abogados de Starkman Firm':'The attorneys of Starkman Firm'}"><meta property="og:site_name" content="Starkman Firm">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="${o.title}"><meta name="twitter:description" content="${o.desc}"><meta name="twitter:image" content="https://www.starkmanfirm.com/assets/og-cover.jpg">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="geo.region" content="US-NJ"><meta name="geo.placename" content="${o.geo||'Cherry Hill, New Jersey'}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="${u}assets/site.css">
<script type="application/ld+json">${JSON.stringify({"@context":"https://schema.org","@graph":graph})}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NG99FGY5L4"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-NG99FGY5L4');</script>
</head><body>`;
}

function header(o){
  const u = up(o.dir), es = o.lang === "es";
  const nav = es
    ? [["Lesiones personales","es/lesiones-personales/"],["Compensación laboral","es/compensacion-laboral/"],["Resultados","es/resultados/"],["Abogado","es/abogados/"],["Oficinas","es/oficinas/"],["Recursos","es/recursos/"]]
    : [["Personal injury","personal-injury/"],["Workers' comp","workers-compensation/"],["Results","results/"],["Attorney","attorneys/"],["Offices","offices/"],["Resources","resources/"]];
  const navHtml = nav.map(([l,h])=>`<a href="${u}${h}">${l}</a>`).join("");
  const langLink = es ? `<a href="${u}${o.enDir||''}" lang="en" hreflang="en">English</a>` : `<a href="${u}${o.esDir||'es/'}" lang="es" hreflang="es">Español</a>`;
  return `<div class="callbar"><div class="wrap"><span>${es?"¿Lesionado en el trabajo o en la carretera? Consulta gratis — no cobramos si no recuperamos.":"Hurt at work or on the road? Free consultation — no fee unless we recover."}</span><span>Cherry Hill <a href="tel:+18564247277">856-424-7277</a> · Perth Amboy <a href="tel:+17323242011">732-324-2011</a> · ${langLink}</span></div></div>
<header class="site"><div class="wrap"><a class="mark" href="${u}${es?'es/':''}"><img class="lm" src="${rel}assets/logo-mark.png" alt="The Starkman Law Firm" width="376" height="661"><img class="lw" src="${rel}assets/logo-wordmark.svg" alt="" width="884" height="175"></a>
<nav class="main" aria-label="${es?'Principal':'Main'}">${navHtml}${es?'':`<a href="${u}es/" lang="es" hreflang="es">Español</a>`}</nav>
<div style="display:flex;gap:10px"><a class="btn btn-out" href="tel:+18564247277">856-424-7277</a><a class="btn btn-brick" href="${u}${es?'es/consulta-gratis/':'free-case-review/'}">${es?"Consulta gratis":"Book a consult"}</a></div></div></header>`;
}

function footer(o){
  const u = up(o.dir), es = o.lang === "es";
  const links = es
    ? [["Accidentes de auto y camión","es/lesiones-personales/accidentes-de-auto/"],["Resbalones y caídas","es/lesiones-personales/caidas/"],["Compensación laboral","es/compensacion-laboral/"],["Lesiones de construcción","es/compensacion-laboral/lesiones-de-construccion/"],["English","./"]]
    : [["Car & truck accidents","personal-injury/car-accidents/"],["Slip & fall","personal-injury/slip-and-fall/"],["Workers' compensation","workers-compensation/"],["Construction injuries","workers-compensation/construction-injuries/"],["Español","es/"]];
  const office = (k,es) => { const n = NAP[k]; return `<div class="col"><h4>${n.city}</h4><address style="font-style:normal;line-height:1.65">${n.street}<br>${n.cityline}</address><a href="tel:${n.tel_e}">${n.tel}</a><span style="color:var(--muted);font-size:14px">${es?n.hours_es:n.hours}</span></div>`; };
  return `<footer class="site"><div class="wrap"><div class="cols">
<div class="col"><a class="mark" href="${u}${es?'es/':''}" style="margin-bottom:6px"><img class="lm" src="${rel}assets/logo-mark.png" alt="The Starkman Law Firm" width="376" height="661"><img class="lw" src="${rel}assets/logo-wordmark.svg" alt="" width="884" height="175"></a><p style="margin:0;color:var(--muted)">${es?"Lesiones personales y compensación laboral en Nueva Jersey desde 1973.":"Personal injury and workers' compensation for New Jersey since 1973."}</p><a href="mailto:info@starkmanfirm.com">info@starkmanfirm.com</a></div>
${office("ch",es)}${office("pa",es)}
<div class="col"><h4>${es?"Práctica":"Practice"}</h4>${links.map(([l,h])=>`<a href="${u}${h==='./'?'':h}">${l}</a>`).join("")}<a href="${u}${es?'es/accesibilidad/':'accessibility/'}">${es?"Accesibilidad":"Accessibility"}</a></div>
</div>
<p class="fine" style="margin-top:34px;padding-top:20px;border-top:1px solid var(--line)">© 2026 Starkman Firm. ${es?"Publicidad de abogados. Los resultados anteriores no garantizan un resultado similar. Este sitio es información general, no asesoría legal.":"Attorney advertising. Prior results do not guarantee a similar outcome. This website is general information, not legal advice."}</p>
</div></footer></body></html>`;
}

function crumbs(o, trail){ const u = up(o.dir); return `<div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb">${trail.map((t,i)=> i===trail.length-1 ? `<span>${t[0]}</span>` : `<a href="${u}${t[1]}">${t[0]}</a> <span style="opacity:.5">/</span> `).join("")}</nav></div>`; }

function pagehero(o, trail, h1, lead, ctas){
  return `<div class="pagehero">${crumbs(o,trail)}<div class="wrap" style="display:flex;flex-direction:column;gap:20px;padding-top:26px">
<h1>${h1}</h1><p>${lead}</p>${ctas||""}</div></div>`;
}

function ctaRow(o){ const es = o.lang==="es"; const u = up(o.dir); const pa = /perth-amboy/.test(o.dir); const n = pa ? NAP.pa : NAP.ch; return `<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-brick btn-lg" href="tel:${n.tel_e}">${es?"Llame al":"Call"} ${n.tel}</a><a class="btn btn-out-w btn-lg" href="${u}${es?'es/consulta-gratis/':'free-case-review/'}">${es?"Consulta gratis":"Book a free consult"}</a></div>`; }

function faqBlock(faqs, heading){ return `<section class="faq"><div class="wrap" style="max-width:880px"><div class="sechead"><h2 class="sec">${heading}</h2></div><div style="margin-top:26px">${faqs.map(([q,a])=>`<details><summary>${q}</summary><p>${a}</p></details>`).join("")}</div></div></section>`; }

function officesBlock(o, heading, lead){
  const es = o.lang==="es", u = up(o.dir);
  const one = (k, dirEn, dirEs, blurb) => { const n = NAP[k]; return `<div class="office"><iframe class="mapframe" loading="lazy" title="Map — ${n.city} office" src="https://maps.google.com/maps?q=${n.map}&z=15&output=embed"></iframe><div class="body"><h3>${n.city}</h3><address>${n.street}<br>${n.cityline}</address><p class="meta">${es?n.hours_es:n.hours}</p><p style="margin:0;color:var(--muted);font-size:16px">${blurb}</p><div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-ink" href="tel:${n.tel_e}">${es?"Llame al":"Call"} ${n.tel}</a><a class="btn btn-out" href="${u}${es?dirEs:dirEn}">${es?"Detalles":"Office details"}</a></div></div></div>`; };
  return `<section><div class="wrap"><div class="sechead"><h2 class="sec">${heading}</h2><p class="lead">${lead}</p></div><div class="offices">
${one("ch","cherry-hill-nj/","es/cherry-hill-nj/", es?"Sobre la Ruta 70, a minutos del Cherry Hill Mall. Servimos los condados de Camden, Burlington y Gloucester.":"On Route 70, minutes from the Cherry Hill Mall. Serving Camden, Burlington and Gloucester counties.")}
${one("pa","perth-amboy-nj/","es/perth-amboy-nj/", es?"En el centro de Perth Amboy, cerca del City Hall. Servimos los condados de Middlesex, Union, Monmouth y Ocean.":"Downtown Perth Amboy, near City Hall. Serving Middlesex, Union, Monmouth and Ocean counties.")}
</div></div></section>`;
}

function bigCta(o){
  const es = o.lang==="es", u = up(o.dir);
  return `<section class="cta"><div class="wrap grid">
<div style="display:flex;flex-direction:column;gap:20px"><span class="kicker">${es?"Revisión gratuita":"Free case review"}</span>
<h2 class="sec" style="color:#fff">${es?"Cuéntenos qué pasó. Le diremos qué haríamos nosotros.":"Tell us what happened. We'll tell you what we would do."}</h2>
<p class="lead" style="color:#C8D2DC">${es?"Una conversación real, no un centro de llamadas. Si no somos el bufete indicado para su caso, se lo diremos.":"A real conversation, not a call center. If we are not the right firm for your case, we will say so."}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-brick btn-lg" href="tel:+18564247277">Cherry Hill · 856-424-7277</a><a class="btn btn-out-w btn-lg" href="tel:+17323242011">Perth Amboy · 732-324-2011</a></div>
<p class="fine" style="color:#A9B7C4">${es?'O escriba a <a href="mailto:info@starkmanfirm.com" style="color:#F0B49F">info@starkmanfirm.com</a>. Contactar al bufete no crea una relación abogado–cliente, y la información enviada antes de que aceptemos representarlo no es confidencial.':'Or email <a href="mailto:info@starkmanfirm.com" style="color:#F0B49F">info@starkmanfirm.com</a>. Contacting the firm does not create an attorney–client relationship, and information sent before we agree to represent you is not confidential.'}</p></div>
<form class="form" action="#" method="post"><h3>${es?"Revisión gratuita":"Free case review"}</h3>
<label>${es?"Nombre":"Name"}<input name="name" placeholder="${es?"Nombre completo":"Full name"}" required></label>
<label>${es?"Teléfono":"Phone"}<input name="phone" type="tel" placeholder="(856) 555-0100" required></label>
<label>${es?"Correo electrónico":"Email"}<input name="email" type="email" placeholder="${es?"usted@ejemplo.com":"you@example.com"}"></label>
<label>${es?"¿Qué tipo de caso?":"What kind of case?"}<select name="type"><option>${es?"Accidente de auto o camión":"Car or truck accident"}</option><option>${es?"Compensación laboral":"Workers' compensation"}</option><option>${es?"Resbalón o caída":"Slip, trip or fall"}</option><option>${es?"Lesión de construcción":"Construction injury"}</option><option>${es?"Todavía no estoy seguro":"Not sure yet"}</option></select></label>
<label>${es?"¿Qué pasó?":"What happened?"}<textarea name="detail" rows="4" placeholder="${es?"Unas frases son suficientes.":"A few sentences is plenty."}"></textarea></label>
<button class="btn btn-brick btn-lg" type="submit">${es?"Solicitar mi revisión gratuita":"Request my free review"}</button>
<p class="fine">${es?"Respondemos el mismo día hábil. Se habla español.":"We respond the same business day. Se habla español."}</p></form>
</div></section>`;
}
