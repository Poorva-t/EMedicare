// Multilingual Translations
const translations = {
  en: {
    dashboard: "Dashboard",
    logout: "Logout",
    book: "Book Appointment",
    cancel: "Cancel",
    join: "Join Consultation",
    welcome: "Welcome back",
  },
  es: {
    dashboard: "Panel de control",
    logout: "Cerrar Sesión",
    book: "Reservar Cita",
    cancel: "Cancelar",
    join: "Unirse a la Consulta",
    welcome: "Bienvenido de nuevo",
  }
};

let currentLang = 'en';

function toggleLang() {
  currentLang = currentLang === 'en' ? 'es' : 'en';
  document.getElementById('langToggleBtn').innerText = currentLang === 'en' ? 'ES' : 'EN';
  applyTranslations();
  showToast("Language changed to " + (currentLang === 'en' ? 'English' : 'Español'));
}

function applyTranslations() {
  document.querySelectorAll('[data-lang-key]').forEach(el => {
    const key = el.getAttribute('data-lang-key');
    if (translations[currentLang] && translations[currentLang][key]) {
      el.innerText = translations[currentLang][key];
    }
  });
}

document.addEventListener('DOMContentLoaded', applyTranslations);

// UI Helpers (Loader & Toasts)
function showLoader() {
  const loader = document.getElementById('global-loader');
  if(loader) loader.classList.remove('hidden');
}

function hideLoader() {
  const loader = document.getElementById('global-loader');
  if(loader) loader.classList.add('hidden');
}

function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerText = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

// Auth Helpers
function getToken() {
  const t = localStorage.getItem('token');
  // strict check to avoid bugs where "undefined" is saved as a literal string
  if (t === 'undefined' || t === 'null') return null;
  return t; 
}

function setAuth(token, user) {
  if (token) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  }
}

function getUser() {
  const u = localStorage.getItem('user');
  if (u === 'undefined' || u === 'null') return null;
  return u ? JSON.parse(u) : null;
}

function logout() {
  localStorage.clear();
  window.location.href = '/';
}

// API Wrapper
async function apiCall(endpoint, method = 'GET', body = null) {
  showLoader();
  try {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(endpoint, options);
    
    hideLoader();

    if (res.status === 401) {
      showToast("Session expired or Invalid Auth. Please login again.", "error");
      localStorage.clear();
      setTimeout(() => { window.location.href = '/'; }, 1500);
      throw new Error("Unauthorized");
    }

    if (!res.ok) {
      let err;
      try {
        err = await res.json();
      } catch (e) {
        throw new Error("API Error");
      }
      throw new Error(err.detail || "API Error");
    }
    
    // Some routes might return pure text or no body (e.g. 204), handle safely
    const contentType = res.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return res.json();
    } else {
      return await res.text();
    }
  } catch (error) {
    hideLoader();
    throw error;
  }
}
