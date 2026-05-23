/**
 * DomIQ Pro Max — Main JavaScript
 * Premium interactions, animations, utilities
 */

'use strict';

// ── Global utilities (also defined in base.html for chat widget) ──
window.getCsrfToken = function() {
  return document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || 
    document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
};

window.showToast = window.showToast || function(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const colors = { success: '#10B981', error: '#EF4444', info: '#38BDF8', warning: '#F59E0B' };
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.style.borderLeft = `3px solid ${colors[type]}`;
  toast.innerHTML = `<span>${icons[type]}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
};

window.escapeHtml = function(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
};

// ── Scroll Reveal ──
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('revealed');
        }, i * 50);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });
  
  document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
}

// ── Navbar scroll effect ──
function initNavbar() {
  const nav = document.getElementById('main-nav');
  if (!nav) return;
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      nav.style.background = 'rgba(2,6,23,0.97)';
      nav.style.borderBottomColor = 'rgba(37,99,235,0.2)';
    } else {
      nav.style.background = 'rgba(2,6,23,0.8)';
      nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
    }
  }, { passive: true });
}

// ── Smooth page transitions ──
function initPageTransitions() {
  document.querySelectorAll('a[href^="/"]').forEach(link => {
    if (link.getAttribute('target') === '_blank') return;
    link.addEventListener('click', (e) => {
      // Don't animate for download links or anchor links
      if (link.getAttribute('download') || link.getAttribute('href').startsWith('#')) return;
    });
  });
}

// ── Form auto-resize textareas ──
function initTextareas() {
  document.querySelectorAll('textarea').forEach(textarea => {
    textarea.style.height = 'auto';
    textarea.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 200) + 'px';
    });
  });
}

// ── Range input styling ──
function initRangeInputs() {
  document.querySelectorAll('input[type="range"]').forEach(input => {
    function updateTrack() {
      const val = (input.value - input.min) / (input.max - input.min) * 100;
      input.style.setProperty('--track-progress', val + '%');
    }
    input.addEventListener('input', updateTrack);
    updateTrack();
  });
}

// ── Copy to clipboard ──
window.copyToClipboard = function(text, message = 'Nusxa olindi!') {
  navigator.clipboard.writeText(text).then(() => {
    showToast(message, 'success', 2000);
  }).catch(() => {
    // Fallback
    const el = document.createElement('textarea');
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    showToast(message, 'success', 2000);
  });
};

// ── Format numbers ──
window.formatNumber = function(num) {
  return parseInt(num).toLocaleString('uz-UZ');
};

window.formatMoney = function(num) {
  return parseInt(num).toLocaleString('uz-UZ') + ' so\'m';
};

// ── Keyboard shortcuts ──
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Close modals with Escape
    if (e.key === 'Escape') {
      document.querySelectorAll('[id$="-modal"]').forEach(modal => {
        modal.classList.add('hidden');
      });
      // Close chat panel
      const chatPanel = document.getElementById('chat-panel');
      if (chatPanel && !chatPanel.classList.contains('hidden')) {
        chatPanel.classList.add('hidden');
      }
    }
    
    // Ctrl/Cmd + K — focus search (if any)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const search = document.querySelector('input[type="search"], input[placeholder*="Qidirish"]');
      if (search) search.focus();
    }
  });
}

// ── Lazy load images ──
function initLazyLoad() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      }
    });
  });
  
  document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
}

// ── Tooltip system ──
function initTooltips() {
  document.querySelectorAll('[data-tooltip]').forEach(el => {
    let tooltip;
    
    el.addEventListener('mouseenter', () => {
      tooltip = document.createElement('div');
      tooltip.textContent = el.dataset.tooltip;
      tooltip.style.cssText = `
        position: fixed; z-index: 9999; background: var(--bg-2); color: var(--text);
        border: 1px solid var(--card-border); border-radius: 8px; padding: 6px 12px;
        font-size: 0.8rem; pointer-events: none; white-space: nowrap;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      `;
      document.body.appendChild(tooltip);
    });
    
    el.addEventListener('mousemove', (e) => {
      if (tooltip) {
        tooltip.style.left = (e.clientX + 10) + 'px';
        tooltip.style.top = (e.clientY - 30) + 'px';
      }
    });
    
    el.addEventListener('mouseleave', () => {
      if (tooltip) { tooltip.remove(); tooltip = null; }
    });
  });
}

// ── Ripple effect for buttons ──
function initRipple() {
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.cssText = `
        position: absolute; border-radius: 50%;
        width: ${size}px; height: ${size}px;
        left: ${e.clientX - rect.left - size/2}px;
        top: ${e.clientY - rect.top - size/2}px;
        background: rgba(255,255,255,0.2);
        transform: scale(0);
        animation: ripple-anim 0.5s linear;
        pointer-events: none;
      `;
      
      if (getComputedStyle(this).position === 'static') {
        this.style.position = 'relative';
      }
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 500);
    });
  });
  
  const style = document.createElement('style');
  style.textContent = '@keyframes ripple-anim { to { transform: scale(2); opacity: 0; } }';
  document.head.appendChild(style);
}

// ── Number counter animation ──
window.animateCounter = function(el, target, duration = 1500) {
  const start = 0;
  const startTime = performance.now();
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (target - start) * eased);
    el.textContent = formatNumber(current);
    
    if (progress < 1) requestAnimationFrame(update);
  }
  
  requestAnimationFrame(update);
};

// ── Project progress bar animation ──
function initProgressBars() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const width = bar.dataset.width || bar.style.width;
        bar.style.width = '0';
        setTimeout(() => { bar.style.width = width; }, 100);
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.5 });
  
  document.querySelectorAll('.progress-bar-fill[data-width]').forEach(bar => observer.observe(bar));
}

// ── Mobile touch optimization ──
function initMobileOptimizations() {
  // Avoid 300ms tap delay on modern browsers (already handled by viewport meta)
  // touchend + click kombinatsiyasi double event chiqarishi mumkin, shu uchun olib tashlandı
  document.documentElement.style.touchAction = 'manipulation';
}

// ── Init all ──
document.addEventListener('DOMContentLoaded', () => {
  initScrollReveal();
  initNavbar();
  initPageTransitions();
  initTextareas();
  initRangeInputs();
  initKeyboardShortcuts();
  initLazyLoad();
  initTooltips();
  initRipple();
  initProgressBars();
  
  // Mobile only
  if ('ontouchstart' in window) {
    initMobileOptimizations();
  }
  
  console.log('%c🏠 DomIQ Pro Max', 'color:#38BDF8;font-size:1.2rem;font-weight:bold;');
  console.log('%cAI-powered renovation platform', 'color:#94A3B8;');
});

// ── Service Worker (for offline support) ──
if ('serviceWorker' in navigator && location.hostname !== 'localhost') {
  window.addEventListener('load', () => {
    // navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
