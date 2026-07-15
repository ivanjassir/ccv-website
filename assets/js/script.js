const CCV = (() => {
  /* Progressive enhancement: only enable JS-gated reveal animations when JS runs.
     Without this class the content stays fully visible (e.g. iOS Quick Look,
     no-JS previews of the self-contained file). */
  document.documentElement.classList.add('js');

  const nav = document.querySelector('.nav');
  const toggle = document.querySelector('.nav__toggle');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover)').matches;

  toggle?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('.nav__mobile a').forEach((a) =>
    a.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    })
  );

  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Headline word-by-word reveal ---- */
  document.querySelectorAll('[data-split]').forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    if (reduce) return;
    el.innerHTML = words
      .map((w, i) => `<span class="word"><i style="--d:${i * 0.07}s">${w}</i></span>`)
      .join(' ');
  });

  /* ---- Scroll progress bar ---- */
  const bar = document.getElementById('progress');
  const setProgress = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };

  /* ---- Nav shadow ---- */
  const onScroll = () => {
    nav.classList.toggle('nav--scrolled', window.scrollY > 20);
    setProgress();
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- Reveals with stagger ---- */
  if (!reduce && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.querySelectorAll('[data-stagger]').forEach((k, i) => (k.style.transitionDelay = `${i * 70}ms`));
          e.target.classList.add('in');
          obs.unobserve(e.target);
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -8% 0px' }
    );
    document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('in'));
  }

  /* ---- Count-up ---- */
  const animateCount = (el) => {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    const dur = 1500;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const val = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = val + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (!reduce && 'IntersectionObserver' in window) {
    const co = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          animateCount(e.target);
          obs.unobserve(e.target);
        });
      },
      { threshold: 0.6 }
    );
    document.querySelectorAll('[data-count]').forEach((el) => co.observe(el));
  } else {
    document.querySelectorAll('[data-count]').forEach((el) => (el.textContent = el.dataset.count + (el.dataset.suffix || '')));
  }

  if (!reduce && canHover) {
    /* ---- Hero glow parallax ---- */
    const heroBg = document.querySelector('.hero__bg');
    const hero = document.querySelector('.hero');
    if (heroBg && hero) {
      hero.addEventListener('mousemove', (e) => {
        const r = hero.getBoundingClientRect();
        heroBg.style.setProperty('--mx', ((e.clientX - r.left) / r.width) * 100 + '%');
        heroBg.style.setProperty('--my', ((e.clientY - r.top) / r.height) * 100 + '%');
      });
    }

    /* ---- Magnetic buttons ---- */
    document.querySelectorAll('.btn').forEach((btn) => {
      btn.addEventListener('mousemove', (e) => {
        const r = btn.getBoundingClientRect();
        btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.18}px, ${(e.clientY - r.top - r.height / 2) * 0.28}px)`;
      });
      btn.addEventListener('mouseleave', () => (btn.style.transform = ''));
    });

    /* ---- Card 3D tilt + spotlight ---- */
    document.querySelectorAll('[data-tilt]').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width;
        const py = (e.clientY - r.top) / r.height;
        card.style.transform = `perspective(900px) rotateY(${(px - 0.5) * 8}deg) rotateX(${(0.5 - py) * 8}deg) translateY(-6px)`;
        card.style.setProperty('--cx', px * 100 + '%');
        card.style.setProperty('--cy', py * 100 + '%');
      });
      card.addEventListener('mouseleave', () => (card.style.transform = ''));
    });
  }

  async function submit(e) {
    e.preventDefault();
    const form = e.target;
    const note = document.getElementById('formNote');
    const data = new FormData(form);
    const endpoint = form.dataset.endpoint;
    const to = form.dataset.mailto;

    // 1) If a form endpoint is configured (e.g. Formspree / Web3Forms), POST it.
    if (endpoint) {
      note.textContent = 'Enviando…';
      try {
        const res = await fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
        if (res.ok) {
          note.textContent = 'Gracias, hemos recibido su consulta. Le contactaremos pronto.';
          form.reset();
        } else {
          note.textContent = 'No pudimos enviar su consulta. Escríbanos a ' + (to || 'nuestro correo') + '.';
        }
      } catch (err) {
        note.textContent = 'No pudimos enviar su consulta. Escríbanos a ' + (to || 'nuestro correo') + '.';
      }
      return false;
    }

    // 2) Fallback: compose a prefilled email — works with no backend.
    if (to) {
      const subject = 'Consulta web — ' + (data.get('empresa') || data.get('nombre') || 'CCV Grupo');
      const body =
        'Nombre: ' + (data.get('nombre') || '') + '\n' +
        'Correo: ' + (data.get('correo') || '') + '\n' +
        'Empresa: ' + (data.get('empresa') || '') + '\n\n' +
        'Mensaje:\n' + (data.get('mensaje') || '');
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      note.textContent = 'Abriendo su cliente de correo para enviar la consulta…';
    } else {
      note.textContent = 'Gracias, hemos recibido su consulta. Le contactaremos pronto.';
    }
    form.reset();
    return false;
  }
  return { submit };
})();
