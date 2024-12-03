// Immediately Invoked Function Expression (IIFE) to ensure it runs as soon as the file is loaded
(function applyLocalSavedTheme(){
    const theme = localStorage.getItem("theme-mode");
    setAndLocalSaveTheme(theme);
})();

function themeToggle(){
    let html = document.querySelector("html");
    const attr = "data-bs-theme";    // bootstrap5 attr for theme
    
    // Determine the next theme
    const currentTheme = html.getAttribute(attr) || "light";
    const nextTheme = currentTheme === "light" ? "dark" : "light";

    // Use setAndLocalSaveTheme for switching
    setAndLocalSaveTheme(nextTheme);
}
function setAndLocalSaveTheme(themeMode){
    const themes = ["dark", "light"];
    if (!themes.includes(themeMode)){
        console.warn(`Theme isn't valid; Theme: ${themeMode}`);
        return false;
    }
    let html = document.querySelector("html")   ;
    const attr = "data-bs-theme";    // bootstrap5 attr for theme
    
    html.setAttribute(attr, themeMode);
    localStorage.setItem("theme-mode", themeMode);
}