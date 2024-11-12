import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import Backend from "i18next-http-backend";
import { initReactI18next } from "react-i18next";
import namespaces from "./namespaces.json";

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .use(Backend)
  .init({
    react: {
      useSuspense: true,
    },
    // fallbackLng: "en",
    // lng: "ru",
    debug: true,
    ns: namespaces,
    backend: {
      loadPath: "./locales/{{lng}}/{{ns}}.json",
    },
    fallbackLng: "en",
    detection: {
      order: [
        "querystring",
        "cookie",
        "localStorage",
        "sessionStorage",
        "navigator",
        "htmlTag",
        "path",
        "subdomain",
      ],
      caches: ["localStorage"],
      cookieMinutes: 10080,
      lookupQuerystring: "lng",
      lookupCookie: "server_language",
      lookupLocalStorage: "i18nextLng",
      lookupSessionStorage: "i18nextLng",
      excludeCacheFor: ["cimode"],
    },
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
